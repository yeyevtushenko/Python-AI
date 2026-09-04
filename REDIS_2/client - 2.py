import redis
import socket
import threading

redis_client = redis.StrictRedis(host='192.168.56.56', port=6379, db=0)

channel = 'channel1'

server_address = ('localhost', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

def listen_for_server_messages():
    while True:
        try:
            server_message = client_socket.recv(1024).decode()
            if not server_message:
                break
            print(f"Received from server: {server_message}")
        except ConnectionError:
            break

message_listener_thread = threading.Thread(target=listen_for_server_messages)
message_listener_thread.daemon = True
message_listener_thread.start()

while True:
    message = input("Enter a message (or 'exit' to quit): ")

    if message == 'exit':
        break

    redis_client.publish(channel, message)

redis_client.close()

client_socket.close()