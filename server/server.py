import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5001

def handle_client(connection, address):
    # Handles messages from one connected client
    print(f'Connected: {address}')

    with connection:
        with connection.makefile("r", encoding="utf-8") as reader:
            while True:
                try:
                    message = reader.readline()

                    if not message:
                        break
                    request = json.loads(message)

                    message_type = request.get('type')

                    if message_type == 'PING':
                        response = {"type":"PONG"}
                    else:
                        response = {"type":"ERROR", "message":"Unknown message type"}

                    response_json = json.dumps(response) + "\n"
                    connection.sendall(response_json.encode("utf-8"))

                except json.JSONDecodeError:
                    response = {"type":"ERROR","message":"Invalid JSON"}
                    try:
                        connection.sendall((json.dumps(response) + "\n").encode("utf-8"))
                    except OSError:
                        break
                except (ConnectionError, OSError):
                    print(f'Connection lost: {address}')
                    break

        print(f'Disconnected: {address}')

def start_server():
    # Create & start TCP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server.bind((HOST, PORT))

        server.listen(5)

        print(f'SOLD! server starting on port {PORT}')

        while True:
            connection, address = server.accept()

            client_thread = threading.Thread(
                target=handle_client,
                args=(connection, address),
                daemon=True
            )

            client_thread.start()

if __name__ == '__main__':
    start_server()