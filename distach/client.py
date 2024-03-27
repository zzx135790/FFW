import json
import pickle
import socket
import struct
import threading
import time
import GPUtil

import distach.message as message
import distach.config as config

from mmdet.apis import init_detector
from ultralytics import YOLO
from concurrent.futures import ThreadPoolExecutor


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.detect_thd = threading.Thread(
            target=self.start
        )
        self.tid = 0

    def __call__(self):
        self.detect_thd.start()
        while True:
            threading.Thread(target=self.prepare).start()
            time.sleep(500)

    def prepare(self):
        try:
            self.client_socket.connect((config.server_ip, config.prepare_port))
            print("调度节点连接成功")

            # 向服务器发送消息
            msg = message.client_prepare()()
            self.client_socket.sendall(struct.pack("L", len(msg)))
            self.client_socket.sendall(msg)
            print("算力机准备中")

            # 等待并接收服务器的响应
            response = json.loads(self.client_socket.recv(1024).decode("utf-8"))
            if response["status"] == 200:
                print("算力机已准备")
                self.client_socket.close()
            else:
                # 没有接收到响应，或响应不正确，继续等待
                time.sleep(5)
        except Exception as e:
            print("发生错误：", e)
            self.client_socket.close()

    def start(self):
        self.listen_socket.bind((socket.gethostname(), config.client_port))
        self.listen_socket.listen(4)
        print("算力机准备工作")
        with ThreadPoolExecutor(1) as thd_pool:
            while True:
                # 接受客户端连接
                client_socket, client_address = self.listen_socket.accept()
                # 接收数据长度信息
                data_size = struct.unpack("L", client_socket.recv(4))[0]
                # 接收数据
                data = b""
                while len(data) < data_size:
                    packet = client_socket.recv(4096)
                    if not packet:
                        break
                    data += packet
                # 反序列化数据
                data = pickle.loads(data)
                thd_pool.submit(
                    self.client_detect, data["mid"], data["gid"], data["img"], data["iid"], self.tid
                )
                self.tid += 1

    def client_detect(self, mid, gid, img, iid, tid):
        from detect.common import config_path, models_path
        import distach.threads as threads
        # gpus = GPUtil.getGPUs()
        # if gpus[gid].load > 0.8:
        #     return

        if config_path[mid] == '':
            model = YOLO(models_path[mid])
            thd = threads.Client_yolo(f"yolo {tid}", mid, model, img, gid)
        else:
            model = init_detector(config_path[mid], models_path[mid], device=f'cuda:{gid}')
            thd = threads.Client_mmd(f'mmd {tid}', mid, model, img)
        del model
        thd.start()
        thd.join()
        single_results = []
        for single in thd.results:
            single_results.append(single)
        data = message.client_result(iid, mid, single_results)()
        print(f'结果为：{single_results[0].cls}')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((config.server_ip, config.result_port))
            s.sendall(struct.pack("L", len(data)))
            s.sendall(data)
            s.close()
