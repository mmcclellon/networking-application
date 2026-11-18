import socket
import json

HOST = 'localhost'
PORT = 5001

def start_client():
    # Connect to SOLD! server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print('Connected to SOLD! server')

        message = {"type":"PING"}

        message_json = json.dumps(message) + "\n"

        client.sendall(message_json.encode("utf-8"))


        with client.makefile("r", encoding="utf-8") as reader:
            response = reader.readline()
        
        if response:
            response_data = json.loads(response)
            print("Server response:", response_data)
        else:
            print("server closed the connection.")

if __name__ == '__main__':
    start_client()
