import socket
import threading

def handle_client(client, address):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"Received message from {address}: {message}")
                broadcast(message)
        except Exception as e:
            print(f"Error handling message from {address}: {e}")
            clients.remove(client)
            client.close()
            broadcast(f"{address} has disconnected.")
            break

def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            clients.remove(client)
            client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server.listen()
    print("Server started. Waiting for connections...")

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        clients.append(client)
        threading.Thread(target=handle_client, args=(client, address)).start()

if __name__ == "__main__":
    clients = []
    start_server()
