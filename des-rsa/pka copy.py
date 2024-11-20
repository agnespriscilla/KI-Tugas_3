import socket

# PKA stores server public keys
public_keys = {}

pka_host = "127.0.0.1"
pka_port = 65433

def register_public_key(client_id, public_key):
    public_keys[client_id] = public_key

def pka_program():
    pka_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pka_socket.bind((pka_host, pka_port))
    pka_socket.listen(5)
    print("Public Key Authority is running...")

    while True:
        conn, addr = pka_socket.accept()
        print(f"Connection from {addr}")

        # Handle registration or query
        request = conn.recv(1024).decode()
        if request.startswith("REGISTER"):
            _, client_id, public_key = request.split(" ", 2)
            public_keys[client_id] = public_key
            conn.send(b"Public key registered successfully.")
            print(f"Registered public key for client {client_id}: {public_key}")
        elif request.startswith("QUERY"):
            _, client_id = request.split(" ")
            if client_id in public_keys:
                conn.send(public_keys[client_id].encode())
                print(f"Sent public key for client {client_id}: {public_keys[client_id]}")
            else:
                conn.send(b"Client ID not found.")
        conn.close()

if __name__ == "__main__":
    pka_program()
