import GPUtil
import pickle
import socket


def get_free_gpus():
    gpus = GPUtil.getGPUs()
    free_gpus = [gpu.id for gpu in gpus if gpu.load < 0.1]  # 假设GPU负载低于10%即视为空闲
    return free_gpus


def get_local_ip():
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不需要真的连接，所以目标地址随便写一个即可
        # 但是端口号不要写成80等常用端口，以免被占用
        s.connect(('8.8.8.8', 7687))
        # 获取本地接口的IP地址
        ip = s.getsockname()[0]
    finally:
        # 无论如何都关闭socket
        s.close()
    return ip


class base_msg:
    def __init__(self):
        self.message = {}

    def __call__(self):
        return pickle.dumps(self.message)


class client_prepare(base_msg):
    def __init__(self):
        self.message = {
            "ip": get_local_ip(),
            "glist": get_free_gpus()
        }


class client_result(base_msg):
    def __init__(self, iid, mid, data):
        self.message = {
            "iid": iid,
            "mid": mid,
            "data": data,
            "ip": get_local_ip(),
            "glist": get_free_gpus()
        }


class server_status_back(base_msg):
    def __init__(self, status):
        self.message = {
            "status": status
        }


class server_detect_data(base_msg):
    def __init__(self, img, iid, mid, gid):
        self.message = {
            "img": img,
            "id": iid,
            "mid": mid,
            "gid": gid
        }
