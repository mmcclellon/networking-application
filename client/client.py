import socket
import json
import threading
import time
import getpass

HOST = 'localhost'
PORT = 5001

HEARTBEAT_INTERVAL = 10
HEARTBEAT_TIMEOUT = 5

# Connect to SOLD! server
def start_client():
    stop_event = threading.Event()
    send_lock = threading.Lock()
    heartbeat_lock = threading.Lock()

    last_ping = [None]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print('Connected to SOLD! server')

        def send_message(message):
            message_json = json.dumps(message) + "\n"

            with send_lock:
                client.sendall(message_json.encode("utf-8"))
        
        def receive_message():
            try:
                with client.makefile("r", encoding="utf-8") as reader:  
                    while not stop_event.is_set():
                        response = reader.readline()

                        if not response:
                            print("\nServer disconnected")
                            break

                        data = json.loads(response)

                        if data.get("type") == "PONG":
                            with heartbeat_lock:
                                last_ping[0] = None
                            print("\nHeartbeat received: PONG")

                        else:
                            print("\nServer response:", data)

            except (OSError, ConnectionError, ValueError) as error:
                if not stop_event.is_set():
                    print("\nConnection error:", error)
            
            finally:
                stop_event.set()

        def send_heartbeat():
            while not stop_event.wait(HEARTBEAT_INTERVAL):

                with heartbeat_lock:
                    if last_ping[0] is not None:
                        continue

                    last_ping[0] = time.monotonic()

                try:
                    send_message({"type": "PING"})
                    print("\nHeartbeat sent: PING")
                
                except OSError:
                    print("\nUnable to send heartbeat.")
                    stop_event.set()
                    break
                
                if stop_event.wait(HEARTBEAT_TIMEOUT):
                    break

                with heartbeat_lock:
                    timed_out = (last_ping[0] is not None and time.monotonic() - last_ping[0] >= HEARTBEAT_TIMEOUT)

                if timed_out:
                    print("\nHeartbeat timed out. Server is unresponsive")
                    stop_event.set()
                    break
                
        receiver_thread = threading.Thread(target=receive_message, daemon=True)

        heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)

        receiver_thread.start()
        heartbeat_thread.start()

        try:
            while not stop_event.is_set():
                command = input('Enter command (REGISTER, LOGIN, PING, LOGOUT OR QUIT): ').strip().upper()

                if command == 'QUIT':
                    print('Disconnecting from the server...')
                    break
                
                if stop_event.is_set():
                    break

                
                message = {"type": command}
                if command in ('REGISTER', 'LOGIN'):
                    message["username"] = input('Username: ').strip()
                    message["password"] = getpass.getpass('Password: ')

                try:
                    send_message(message)
                except OSError:
                    print('Unable to send message.')
                    break
        except (KeyboardInterrupt, EOFError):
            print("\nClient stopping")
        
        finally:
            stop_event.set()

            try:
                client.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            
    print("Disconnected from SOLD! server.")

if __name__ == '__main__':
    start_client()