import sys
import threading
import socket

#checking if user provided ip and port
if len(sys.argv) < 3:
    print("Usage: <script> <address> <port> [(room_ids])")
    exit()
    
host = str(sys.argv[1])
port = int(sys.argv[2])

ROOMS = {0:[[],[]]} #{Room-ID:[[client],[username]]}

# checking if user provided Room IDs, and creating the room
if len(sys.argv) > 3:
    room_ids = eval(sys.argv[3])
    for i in room_ids:
        ROOMS[int(i)]

# initializing a Internet(AF_INET), TCP(SOCK_STREAM) server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port)) # binding the server to the provided ip and pord

server.listen() # listening for incomming connections

#Function to send messages to clients in specified room
def broadcast(message,room_id):
    for client in ROOMS[room_id][0]:
        client.send(message)

# Function to handle clients ie recieving messages and sending them, and disconnecting users
def handle_client(client,room_id):
    while True:
        try:
            message = client.recv(1024) # recieving message from client (upto 1024 bytes)
            broadcast(message,room_id)
        except:    # To remove client from chatroom if the client disconnects or some error occurs
            index = ROOMS[room_id][0].index(client)
            ROOMS[room_id][0].remove(client)
            client.close() # closing the connection
            username = ROOMS[room_id][1][index]
            broadcast(f'{username} has left the chat room!'.encode('utf-8'),room_id)
            ROOMS[room_id][1].remove(username)
            break

# Function to establish connection with clients
def receive():
    while True:
        print('Server is running and listening ...')
        conn, address = server.accept() # accepting the connection from clients
        print(f'connection is established with {str(address)}')
        conn.send('/<@username>/'.encode('utf-8')) # asking for username
        username = conn.recv(1024) # recieving username (upto 1024 bytes)
        conn.send('/<@room_id>/'.encode('utf-8')) # asking for Room ID
        room_id = int(conn.recv(512)) # recieving Room ID (upto 512 bytes)
        if room_id != 0 and room_id not in room_ids:
            conn.send(f'There is no chatroom with the ID: {str(room_id)}, Connecting to Chatroom-0'.encode('utf-8'))
            room_id = 0
        ROOMS[room_id][1].append(username)
        ROOMS[room_id][0].append(conn)
        print(f'The usernames of this client is {username}'.encode('utf-8'))
        broadcast(f'{username} has connected to the chat room'.encode('utf-8'),room_id)
        conn.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(conn,room_id)) # running handle_client() for each user on separate threads
        thread.start()


if __name__ == "__main__":
    receive()