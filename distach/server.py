import socket
import struct
import pickle
import threading

import distach.structs as structs
import distach.config as config
import distach.message as message


from concurrent.futures import ThreadPoolExecutor


class Server:
    def __init__(self):
        self.client_table = structs.ClientTable()
        self.receive_client = threading.Thread(target=self.receive_client_thread)

    def __call__(self):
        self.start()

    def receive_client_thread(self, max_workers=2):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
            listen_socket.bind((socket.gethostname(), config.prepare_port))
            listen_socket.listen(4)
            print("\n算力机添加模块启动")
            with ThreadPoolExecutor(max_workers) as thd_pool:
                while True:
                    client_conn, _ = listen_socket.accept()
                    thd_pool.submit(self.receive_client_work, client_conn, listen_socket)

    def receive_client_work(self, conn):
        # 接收数据长度信息
        data_size = struct.unpack("L", conn.recv(4))[0]
        # 接收数据
        data = b""
        while len(data) < data_size:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet

        # 反序列化数据
        data = pickle.loads(data)
        self.client_table.update(data["ip"], data["glist"])

        msg = message.server_status_back()()
        # print("发送回报")
        conn.sendall(msg.encode('utf-8'))
        print(f'添加ip为{data["ip"]}的算力机，可使用gpus为{data["glist"]}')

    def start(self):
        self.receive_client.start()
