import socket
import threading
import json

from database.database import init_db, create_user, get_user
from server.auth import new_salt, hash_password, verify_password, is_valid_username, is_valid_password

HOST = "0.0.0.0"
PORT = 5001


# Every message type the server understands
KNOWN_MESSAGES = {'PING', 'REGISTER', 'LOGIN', 'LOGOUT'}

# Message types allowed BEFORE logging in. Everything else requires LOGIN first.
PUBLIC_MESSAGES = {'PING', 'REGISTER', 'LOGIN'}

# Usernames that are logged in right now. Shared by all client threads,
# so always hold online_users_lock while reading or changing it.
online_users = set()
online_users_lock = threading.Lock()

def failure(message_type, code, text):
    # Builds a failure reply
    return {"type": message_type, "code": code, "message": text}

def get_credentials(request):
    # Returns (username, password), or (None, None) if either is missing, empty, or not a string
    username = request.get('username')
    password = request.get('password')

    if not isinstance(username, str) or not isinstance(password, str) or not username or not password:
        return None, None

    return username, password

def handle_register(request):
    username, password = get_credentials(request)

    if username is None:
        return failure('REGISTER_FAILED', 'MISSING_FIELDS', 'username and password are required')

    if not is_valid_username(username):
        return failure('REGISTER_FAILED', 'INVALID_USERNAME', 'Username must be 3-20 letters, digits or underscores')

    if not is_valid_password(password):
        return failure('REGISTER_FAILED', 'WEAK_PASSWORD', 'Password must be 8-128 characters')

    salt = new_salt()
    password_hash = hash_password(password, salt)

    # Stored as hex text. create_user returns False if the username is taken.
    if not create_user(username, password_hash.hex(), salt.hex()):
        return failure('REGISTER_FAILED', 'USERNAME_TAKEN', 'That username is already taken')

    return {"type": "REGISTER_SUCCESS", "username": username}

def handle_login(request, current_user):
    # Returns (response, username). username is None if the login failed.
    if current_user is not None:
        return failure('LOGIN_FAILED', 'ALREADY_LOGGED_IN', f'You are already logged in as {current_user}'), None

    username, password = get_credentials(request)

    if username is None:
        return failure('LOGIN_FAILED', 'MISSING_FIELDS', 'username and password are required'), None

    user = get_user(username)

    # Same reply for "no such user" and "wrong password", so nobody can probe which usernames exist
    if user is None or not verify_password(password, user['salt'], user['password_hash']):
        return failure('LOGIN_FAILED', 'INVALID_CREDENTIALS', 'Invalid username or password'), None

    username = user['username']  # use the spelling stored in the database

    with online_users_lock:
        if username in online_users:
            return failure('LOGIN_FAILED', 'ALREADY_LOGGED_IN', f'{username} is already logged in on another client'), None
        online_users.add(username)

    return {"type": "LOGIN_SUCCESS", "username": username}, username

def process_request(request, current_user, address):
    # Works out the reply to one message.
    # Returns response, current_user, close_connection
    if not isinstance(request, dict):
        return failure('ERROR', 'INVALID_JSON', 'Message must be a JSON object'), current_user, False

    message_type = request.get('type')

    if not isinstance(message_type, str) or message_type not in KNOWN_MESSAGES:
        return failure('ERROR', 'UNKNOWN_TYPE', 'Unknown message type'), current_user, False

    if current_user is None and message_type not in PUBLIC_MESSAGES:
        return failure('ERROR', 'NOT_AUTHENTICATED', 'You must LOGIN first'), current_user, False

    if message_type == 'PING':
        return {"type": "PONG"}, current_user, False

    if message_type == 'REGISTER':
        response = handle_register(request)
        print(f'[{address[0]}] REGISTER {request.get("username")!r} -> {response.get("code", "OK")}')
        return response, current_user, False

    if message_type == 'LOGIN':
        response, username = handle_login(request, current_user)
        if username is not None:
            current_user = username
        print(f'[{address[0]}] LOGIN {request.get("username")!r} -> {response.get("code", "OK")}')
        return response, current_user, False

    # LOGOUT: reply GOODBYE, then handle_client closes the connection
    print(f'[{address[0]}] LOGOUT {current_user!r}')
    return {"type": "GOODBYE"}, current_user, True


def handle_client(connection, address):
    # Handles messages from one connected client
    print(f'Connected: {address}')
    current_user = None #username of the currently logged in user (None = not logged in)

    with connection:
        with connection.makefile("r", encoding="utf-8", errors="replace") as reader:
            while True:
                try:
                    message = reader.readline()

                    if not message:
                        break
                    request = json.loads(message)

                    response, current_user, close_connection = process_request(request, current_user, address)


                    response_json = json.dumps(response) + "\n"
                    connection.sendall(response_json.encode("utf-8"))

                    if close_connection:
                        break

                except json.JSONDecodeError:
                    response = {"type":"ERROR","message":"Invalid JSON", "message":"Invalid JSON"}
                    try:
                        connection.sendall((json.dumps(response) + "\n").encode("utf-8"))
                    except OSError:
                        break
                except (ConnectionError, OSError):
                    print(f'Connection lost: {address}')
                    break
                except Exception as error:
                    print(f'Error handling message from {address}: {error!r}')
                    response = {"type":"ERROR", "code":"SERVER_ERROR", "message":"Server could not process that message"}
                    try:
                        connection.sendall((json.dumps(response) + "\n").encode("utf-8"))
                    except OSError:
                        break

        if current_user is not None:
            with online_users_lock:
                online_users.discard(current_user)
            

        print(f'Disconnected: {address}')

def start_server():
    init_db() #create and start tcp server
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