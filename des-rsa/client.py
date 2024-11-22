import des
import rsa
import socket
import threading
import time
import sys
import json
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432
pka_host = "127.0.0.1"
pka_port = 65433

clientID = 0
secret_key = '1234567890ABCDEF'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Dictionary to store messages
messages = {}

def register_with_pka(client_id, public_key):
    pka_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pka_socket.connect((pka_host, pka_port))
    pka_socket.send(f"REGISTER {client_id}".encode())
    response = pka_socket.recv(1024).decode()
    pka_socket.send(json.dumps(public_key).encode())
    response = pka_socket.recv(1024).decode()
    print("Registered with PKA:", response)
    pka_socket.close()

def query_pka(client_id):
    pka_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pka_socket.connect((pka_host, pka_port))
    pka_socket.send(f"QUERY {client_id}".encode())
    public_key_data = json.loads(pka_socket.recv(1024).decode())
    pka_socket.close()
    if public_key_data == "Client ID not found.":
        raise Exception("Client public key not found.")
    return public_key_data

# Check if client exists
def check_client(id):
    client_socket.send("CHECK".encode('utf-8'))
    time.sleep(0.1)
    client_socket.send(id.encode('utf-8'))
    print("Pengecekkan apakah ID client valid...")
    response = client_socket.recv(1024).decode('utf-8')
    return response

# Receive messages
def receive_messages(clientID, private_key):
    while True:
        try:
            # Receive and decrypt message
            args = client_socket.recv(1024).decode('latin-1')
            if args == "RECEIVE":
                client_socket.send('OK'.encode('utf-8'))
                client_socket.send('OK'.encode('utf-8'))
                sender_id = int(client_socket.recv(1024).decode('utf-8'))
                if sender_id == clientID:
                    client_socket.send('ABORT'.encode('utf-8'))
                    client_socket.send('ABORT'.encode('utf-8'))
                    continue
                client_socket.send('OK'.encode('utf-8'))
                client_socket.send('OK'.encode('utf-8'))
                encrypted_message = client_socket.recv(1024).decode('latin-1')
                client_socket.send('OK'.encode('utf-8'))
                client_socket.send('OK'.encode('utf-8'))
                encrypted_secret_key = client_socket.recv(1024).decode('latin-1')

                # Decrypt the secret key using RSA
                sender_public_key = query_pka(int(sender_id))
                decrypted_secret_key = rsa.decrypt(int(encrypted_secret_key), private_key)
                decrypted_secret_key = rsa.decrypt_public(decrypted_secret_key, sender_public_key)
                decrypted_secret_key = rsa.int_to_hex(decrypted_secret_key)

                # Decrypt the message
                encrypted_message = des.bin2text(encrypted_message)
                message = des.decrypt(encrypted_message, des.make_rk(decrypted_secret_key))
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = current_time + ': ' + message
                if sender_id not in messages:
                    messages[sender_id] = []
                messages[sender_id].append(message)
            else:
                time.sleep(0.1)
                
        except Exception as e:
            print(e)
            print("Error! Disconnected from the server.")
            client_socket.close()
            return

# View received messages
def view_received_messages():
    sender_id = input("Masukkan ID Client pengirim: ")
    response = check_client(sender_id)
    sender_id = int(sender_id)
    if response == "VALID":
        if sender_id in messages:
            for message in messages[sender_id]:
                print(message)
        else:
            print("Tidak ada pesan yang diterima.")
    else:
        print("ID client tidak valid.")

# Send messages
def send_messages(clientID, private_key):
    receiver_id = input("Masukkan ID Client yang ingin dituju: ")
    if(int(receiver_id) == clientID):
        print("Anda tidak dapat mengirim pesan ke diri sendiri.")
    else:
        response = check_client(receiver_id)
        if response == "VALID":
            message = input("Masukkan pesan: ")
            encrypted_message = des.encrypt(message, des.make_rk(secret_key))
            
            # Encrypt the secret key
            target_public_key = query_pka(int(receiver_id))
            print(f"Target public key: {target_public_key}")
            encrypted_secret_key = rsa.encrypt_private(int(secret_key,16), private_key)
            encrypted_secret_key = rsa.encrypt(encrypted_secret_key, target_public_key)

            client_socket.send("SEND".encode('utf-8'))
            status = client_socket.recv(1024).decode('utf-8')
            print(status)
            client_socket.send(receiver_id.encode('utf-8'))
            status = client_socket.recv(1024).decode('utf-8')
            print(status)
            client_socket.send(encrypted_message.encode('latin-1'))
            status = client_socket.recv(1024).decode('utf-8')
            print(status)
            client_socket.send(str(encrypted_secret_key).encode('utf-8')) # replace with the encrypted DES secret key
            status = client_socket.recv(1024).decode('utf-8')
            print(status)
            print(f'Client {receiver_id} public key: {target_public_key}')
        else:
            print("ID client tidak valid.")

def main_menu(clientID):
    while clientID < 1 or clientID > 10:
        clientID = int(input("Input your client ID (1-10): "))
        if clientID >= 1 and clientID <= 10:
            break
        else:
            print("Client ID must be between 1 and 10.")
    
    # Generate RSA keys
    public_key, private_key = rsa.generate_keys()

    # Send public key to PKA and Server and ClientID to Server
    client_socket.send(str(clientID).encode('utf-8'))
    client_socket.send(json.dumps(public_key).encode('utf-8'))
    register_with_pka(clientID, public_key)

    # Start thread for receiving messages
    cid_for_thread = (clientID,private_key,)
    threading.Thread(target=receive_messages, args=(cid_for_thread)).start()
    client_socket.send(str(clientID).encode('utf-8'))

    while True:
        print("Menu Tugas 3 RSA: (Ketik angka untuk memilih opsi)")
        print("1. Kirim Pesan")
        print("2. Lihat Pesan")
        print("3. Lihat Public Key")
        print("4. Lihat Private Key")
        print("5. Keluar")

        choice = input("Pilih opsi: ")

        if choice == "1":
            send_messages(clientID, private_key)
            continue
        elif choice == "2":
            view_received_messages()
            continue
        elif choice == "3":
            print(f"Public Key: {public_key}")
            continue
        elif choice == "4":
            print(f"Private Key: {private_key}")
            continue
        elif choice == "5":
            client_socket.close()
            sys.exit()
            return
        else:
            print("Opsi tidak valid. Silakan pilih opsi yang tersedia.")
            continue

main_menu(clientID)