import queue
import time


class Lock:
    """
        多线程锁or信号量
        0：正常状态
        1：读取
        2：写入
    """
    # 用于多线程
    def __init__(self):
        self.ste = 0

    def state(self):
        return self.ste

    def resume(self):
        self.ste = 0

    def read(self):
        while not self.check_state(1):
            time.sleep(0.1)
        self.ste = 1

    def write(self):
        while not self.check_state(2):
            time.sleep(0.1)
        self.ste = 2

    # 状态检测，只允许读读
    def check_state(self, o):
        if self.ste == 0 or (self.ste == 1 and o == 1):
            return True
        return False


# 基础的多线程数据
# class BasicData:
#     def __init__(self):
#         self.data = None
#         self.sig = Signal()


class BasicData:
    def __init__(self, data):
        self.data = data
        self.lock = Lock()

    def update(self, data):
        self.lock.write()
        self.data = data
        self.lock.resume()

    def get(self):
        self.lock.read()
        data = self.data
        self.lock.resume()
        return data


class ClientTable:
    def __init__(self):
        self.data = {}
        self.empty_queue = queue.Queue()

    def update(self, ip, glist):
        if not self.data.get(ip):
            self.data[ip] = BasicData(glist)
        else:
            self.data[ip].update(glist)
        for gid in glist:
            self.empty_queue.put((ip, gid))

    def get_table(self, ip):
        data = self.data.get(ip)
        if data:
            return data.get()
        else:
            return data

    def get_empty(self):
        if self.empty_queue.empty():
            return None
        return self.empty_queue.get()
