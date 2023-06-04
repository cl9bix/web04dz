import socket
import json
import datetime

def save_to_json(data):
    with open('storage/data.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

def handle_request(request):
    try:
        data = json.loads(request)
        timestamp = str(datetime.datetime.now())
        data = {timestamp: data}
        save_to_json(data)
        return "Data saved successfully."
    except json.JSONDecodeError:
        return "Invalid JSON format."

def run_server(ip, port):
    def handle(sock: socket.socket, address: str):
        print(f'Connection established {address}')
        while True:
            received = sock.recv(1024)
            if not received:
                break
            data = received.decode()
            print(f'Data received: {data}')
            response = handle_request(data)
            sock.send(response.encode())
        print(f'Socket connection closed {address}')
        sock.close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)
    print(f'Start echo server {server_socket.getsockname()}')
    while True:
        new_sock, address = server_socket.accept()
        handle(new_sock, address)

if __name__ == '__main__':
    run_server('localhost', 5000)
