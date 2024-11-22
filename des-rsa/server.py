import socket
import threading
import time
import des
import rsa
import json

HOST = '127.0.0.1'
PORT = 65432

secret_key = '1234567890ABCDEF'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f'Server listening on {HOST}:{PORT}')

clients = []
client_ids = []
indexed_clients = {}
client_public_keys = {}

def encrypt_des_key(des_key, receiver_id):
    # Enkripsi kunci DES dengan menggunakan public key RSA klien penerima
    public_key = rsa.PublicKey.load_pkcs1(client_public_keys[receiver_id].encode('utf-8'))
    encrypted_key = rsa.encrypt(des_key.encode('utf-8'), public_key)
    return encrypted_key

def handle_client(client_socket, client_address):
    # Receive client ID
    client_id = client_socket.recv(1024).decode('utf-8')
    client_ids.append(int(client_id))  # Add the client ID to the list
    indexed_clients[int(client_id)] = client_socket
    print(f'Client {client_id} registered')

    # Receive client public key
    client_public_key = json.loads(client_socket.recv(1024).decode('utf-8'))
    client_public_keys[int(client_id)] = client_public_key
    print(f'Client {client_id} public key: {client_public_key}')

    while True:
        try:
            args = client_socket.recv(1024).decode('utf-8')
            print(f'Received: {client_id} {args}')
            if args == 'CHECK':
                check_client_id = int(client_socket.recv(1024).decode('utf-8'))
                if check_client_id in client_ids:
                    response = 'VALID'
                    print("Client ID valid")
                else:
                    response = 'INVALID'
                    print("Client ID invalid")
                print(response)
                client_socket.send(response.encode('utf-8'))
                client_socket.send(response.encode('utf-8'))
            
            elif args == 'SEND':
                print("Received send message from client")
                client_socket.send('OK'.encode('utf-8'))
                client_socket.send('OK'.encode('utf-8'))

                # Receive encrypted message
                receiver_id = client_socket.recv(1024).decode('utf-8')
                receiver_id = int(receiver_id)
                print(f'Receiver ID: {receiver_id}')
                client_socket.send('OK'.encode('utf-8'))
                client_socket.send('OK'.encode('utf-8'))
                encrypted_message = client_socket.recv(1024).decode('latin-1')
                print(f'Encrypted message: {encrypted_message}')
                client_socket.send('OK'.encode('utf-8'))
                client_socket.send('OK'.encode('utf-8'))
                encrypted_secret_key = client_socket.recv(1024).decode('latin-1')
                print(f'Encrypted secret key: {encrypted_secret_key}')
                client_socket.send('OK'.encode('utf-8'))
                client_socket.send('OK'.encode('utf-8'))
            
                time.sleep(0.1)
                
                # Send message to client
                indexed_clients[receiver_id].send('RECEIVE'.encode('utf-8'))
                status = indexed_clients[receiver_id].recv(1024).decode('utf-8')
                print(status)
                indexed_clients[receiver_id].send(str(client_id).encode('utf-8'))
                status = indexed_clients[receiver_id].recv(1024).decode('utf-8')
                print(status)
                indexed_clients[receiver_id].send(encrypted_message.encode('latin-1'))
                status = indexed_clients[receiver_id].recv(1024).decode('utf-8')
                print(status)
                indexed_clients[receiver_id].send(encrypted_secret_key.encode('latin-1'))
                print('Message sent to receiving clients')
            
            else:
                time.sleep(0.1)
        except Exception as e:
            print(e)
            clients.remove(client_socket)
            client_socket.close()
            break

# Send messages to all clients
def broadcast(encrypted_message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(encrypted_message.encode('latin-1'))

while True:
    client_socket, client_address = server_socket.accept()
    print(f'Connected to {client_address}')
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()