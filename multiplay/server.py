import socket
import time

HOST = ''
PORT = 22222

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024).decode('utf-8')
            print(f'데이터:{data}')

            if len(data) == 0:
                conn.sendall(f"종료".encode('utf-8'))
                break

            conn.sendall(data.encode('utf-8'))

            time.sleep(1)