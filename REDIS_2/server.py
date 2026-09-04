import threading
import redis
import socket

redis_client = redis.StrictRedis(host='192.168.56.56', port=6379, db=0)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

connected_clients = []


def listen_for_messages():
    redis_client = redis.StrictRedis(host='192.168.56.56', port=6379, db=0)

    pubsub = redis_client.pubsub()

    pubsub.subscribe('channel1')

    for message in pubsub.listen():
        if message['type'] == 'message':
            channel = message['channel'].decode('utf-8')
            data = message['data'].decode('utf-8')
            print(f"Received message on channel '{channel}': {data}")
            redis_client.lpush('chat_messages', data.encode())

            for client_socket in connected_clients:
                try:
                    print('Sent')
                    client_socket.send(data.encode())
                except:
                    print('Error')
                    connected_clients.remove(client_socket)


message_thread = threading.Thread(target=listen_for_messages)
message_thread.start()

while True:
    client_socket, addr = server_socket.accept()
    print('Connected to ', addr)

    connected_clients.append(client_socket)

server_socket.close()