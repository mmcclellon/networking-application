import socket
import json

HOST = 'localhost'
PORT = 5001

def start_client():
    # Connect to SOLD! server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print('Connected to SOLD! server')

        with client.makefile("r", encoding="utf-8") as reader:
            while True:
                command = input('Enter command (PING or QUIT): ').strip().upper()

                if command == 'QUIT':
                    print('Disconnecting from the server')
                    break

                message = {"type": command}
                message_json = json.dumps(message) + "\n"

                client.sendall(message_json.encode("utf-8"))

                response = reader.readline()

                if not response:
                    print("Server closed the connection.")
                    break
                
                response_data = json.loads(response)
                print("Server response:", response_data)
                
    print("Disconnected from SOLD! server.")

if __name__ == '__main__':
    start_client()
