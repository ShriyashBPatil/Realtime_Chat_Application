import socket
import threading

print("Server Configuration")

HOST = input("Enter the Address to Host Server: ")
PORT = int(input("Enter Port to the Server: "))
LISTENER_LIMIT = int(input("Connection Limit: "))
active_clients = [] 

def listen_for_messages(client, username):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"The message send from client {username} is empty")



def send_message_to_client(client, message):

    client.sendall(message.encode())

def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

def client_handler(client):

    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER~" + f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


def main():


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
       
        server.bind((HOST, PORT))
        print(f"Initiated Server on {HOST}:{PORT}")
        print("Clients can now Connect to Server")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    server.listen(LISTENER_LIMIT)

   
    while 1:

        client, address = server.accept()
        print(f"Successfully Connected to {address[0]}:{address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()