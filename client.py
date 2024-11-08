import threading
import socket

# checking if the user provided address and port
    
host = 'localhost'#input("Host IP: ")
port = 25565 #int(input('Port: '))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

username = input('Choose an Username: ')

room_id = input("Room-ID: ")
if not room_id:
    room_id='0'
# Recieve message from server
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "/<@username>/":
                client.send(username.encode('utf-8'))
            elif message == "/<@room_id>/":
                client.send(room_id.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

# send message to server
def client_send():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()