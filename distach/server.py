import json
import queue
import socket
import struct
import pickle
import threading
import os
import time

import cv2

import distach.structs as structs
import distach.config as config
import distach.message as message
import detect.common as comm
from detect.confirm import confirm
from concurrent.futures import ThreadPoolExecutor


class Server:
    def __init__(self):
        self.client_table = structs.ClientTable()
        self.ans_table = None
        self.time_table = structs.TimeTable()
        self.work_space = structs.BasicData((0, 0))
        self.source = None
        self.receive_client = threading.Thread(
            target=self.top_thread,
            args=(config.prepare_port, "算力机入口已监听", self.receive_client_work)
        )
        self.receive_task = threading.Thread(
            target=self.top_thread,
            args=(config.task_port, "任务入口已监听", self.distribute_center, 1)
        )
        self.receive_result = threading.Thread(
            target=self.top_thread,
            args=(config.result_port, "结果入口已监听", self.receive_result_work, 4)
        )

    def __call__(self):
        self.start()

    def get_pickle_data(self, conn):
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
        return data

    def get_json_data(self, conn):
        return json.loads(conn.recv(1024).decode('utf-8'))

    def top_thread(self, port, ss, work, max_workers=2):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
            listen_socket.bind((socket.gethostname(), port))
            listen_socket.listen(10)
            print(ss)
            with ThreadPoolExecutor(max_workers) as thd_pool:
                while True:
                    client_conn, ip = listen_socket.accept()
                    thd_pool.submit(work, client_conn, ip)

    def receive_client_work(self, conn, ip):
        # 反序列化数据
        data = self.get_pickle_data(conn)
        self.client_table.update(ip[0], data["glist"])

        msg = message.server_status_back()()
        # print("发送回报")
        conn.sendall(msg.encode('utf-8'))
        print(f'添加ip为{ip[0]}的算力机，可使用gpus为{data["glist"]}')

    def distribute_center(self, conn, ip):
        print("接受任务")
        data = self.get_json_data(conn)
        # 如果答案表不为空，说明服务器之前的任务还未完成
        if self.ans_table:
            conn.sendall(message.server_status_back(1002)().encode('ut-8'))
            conn.close()
            return

        if data.get("mode") == 'detect':
            files = os.listdir(data.get("source"))
            self.ans_table = structs.AnsTable(files, comm.num_model)
            self.source = (data["source"], files)
            threading.Thread(
                target=self.distribute_work
            ).start()
            threading.Thread(
                target=self.test_output_work
            ).start()

    def distribute_work(self):
        count, now = config.task_per_gpu, None
        for iid, file in enumerate(self.source[1]):
            img = cv2.imread(os.path.join(self.source[0], file))
            for mid in range(comm.num_model):
                if count >= config.task_per_gpu:
                    now = self.client_table.get_free()
                    while now is None:
                        time.sleep(0.5)
                        now = self.client_table.get_free()
                    count = 0
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((now[0], config.client_port))
                    data = message.server_detect_data(img, iid, mid, now[1])()
                    client_socket.sendall(struct.pack("L", len(data)))
                    client_socket.sendall(data)
                    count += 1
                    self.time_table.update((iid, mid))
                    ws = self.work_space.get()
                    self.work_space.update((ws[0], ws[1]+1))
                    client_socket.close()
        print("任务分发结束")

    def receive_result_work(self, conn, ip):
        if not self.ans_table:
            return

        data = self.get_pickle_data(conn)

        if data["status"] != 200:
            return

        self.ans_table.update(self.source[1][data["iid"]], data["mid"], data["data"])
        self.client_table.update(ip[0], data["glist"])

    def test_output_work(self):
        print("故障检测准备")
        while self.ans_table is None:
            time.sleep(10)

        print("故障检测开始")
        count, now = config.task_per_gpu, None
        begin, _ = self.work_space.get()
        while begin < (len(self.source[1]) * comm.num_model):
            begin, end = self.work_space.get()
            while begin < (len(self.source[1]) * comm.num_model) \
                and self.ans_table.get(self.source[1][begin // comm.num_model], begin % comm.num_model) is not None:
                begin += 1
            self.work_space.update((begin, end))

            for index in range(begin, end):
                iid, mid = index // comm.num_model, index % comm.num_model
                if self.time_table.check((iid, mid)):
                    if count >= config.task_per_gpu:
                        now = self.client_table.get_free()
                        while now is None:
                            time.sleep(0.5)
                            now = self.client_table.get_free()
                        count = 0
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((now[0], config.client_port))
                        data = message.server_detect_data(
                            cv2.imread(os.path.join(self.source[0], self.source[1][iid])), iid, mid, now[1]
                        )()
                        client_socket.sendall(struct.pack("L", len(data)))
                        client_socket.sendall(data)
                        count += 1
                        self.time_table.update((iid, mid))
                        client_socket.close()

            time.sleep(config.overtime_second)

        for file in self.source[1]:
            results = []
            for single in self.ans_table.gets(file):
                for result in single:
                    results.append(result)
            confirm(file, results)

        self.ans_table = None
        self.time_table = structs.TimeTable()
        self.work_space = structs.BasicData((0, 0))
        self.source = None
        print('输出到文件')

    def start(self):
        self.receive_client.start()
        self.receive_task.start()
        self.receive_result.start()

