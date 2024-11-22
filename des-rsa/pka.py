import socket
import json

# PKA stores server public keys
public_keys = {}

pka_host = "127.0.0.1"
pka_port = 65433

def register_public_key(client_id, public_key):
    public_keys[client_id] = public_key
    print(f"Registered public key for client {client_id}: {public_key}")

def handle_request(conn):
    # Handle incoming request to register or query public key
    request = conn.recv(1024).decode()
    print(f"Received request: {request}")
    
    if request.startswith("REGISTER"):
        handle_register(conn, request)
    elif request.startswith("QUERY"):
        handle_query(conn, request)
    else:
        conn.send(b"Invalid request.")

def handle_register(conn, request):
    # Handle public key registration
    _, client_id= request.split(" ", 2)
    conn.send("OK".encode())
    public_key = json.loads(conn.recv(1024).decode())
    register_public_key(client_id, public_key)
    conn.send(b"Public key registered successfully.")

def handle_query(conn, request):
    # Handle public key query
    _, client_id = request.split(" ")
    if client_id in public_keys:
        conn.send(json.dumps(public_keys[client_id]).encode())
        print(f"Sent public key for client {client_id}: {public_keys[client_id]}")
    else:
        conn.send(b"Client ID not found.")
        print(f"Client ID {client_id} not found in public key database.")

def pka_program():
    # Main server loop for handling public key registrations and queries
    pka_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        pka_socket.bind((pka_host, pka_port))
        pka_socket.listen(5)
        print("Public Key Authority is running...")

        while True:
            conn, addr = pka_socket.accept()
            print(f"Connection from {addr}")
            try: 
                handle_request(conn)
            except Exception as e:
                print(f"Error handling request: {e}")
                conn.send(b"Error handling your request.")
            finally:
                conn.close()
    except Exception as e:
        print(f"Error starting server: {e}")
    finally:
        pka_socket.close()
        conn.close()

if __name__ == "__main__":
    pka_program()
