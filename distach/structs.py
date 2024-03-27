from datetime import datetime
import queue
import distach.config as config
import threading


class BasicData:
    def __init__(self, data):
        self.data = data
        self.lock = threading.Lock()

    def update(self, data):
        with self.lock:
            self.data = data

    def get(self):
        with self.lock:
            data = self.data
        return data


class ClientTable:
    def __init__(self):
        self.data = {}
        self.empty_queue = queue.Queue()

    def update(self, ip, glist):
        if self.data.get(ip) is None:
            self.data[ip] = BasicData(glist)
        else:
            self.data[ip].update(glist)
        for gid in glist:
            self.empty_queue.put((ip, gid))

    def get_table(self, ip):
        data = self.data.get(ip)
        if data is not None:
            return data.get()
        else:
            return data

    def get_free(self):
        if self.empty_queue.empty():
            return None
        return self.empty_queue.get()


class AnsTable:
    def __init__(self, files, num):
        self.ans = {}
        self.num = num
        for file in files:
            for index in range(num):
                self.ans[(file, index)] = BasicData(None)

    def update(self, file, index, data):
        self.ans[(file, index)].update(data)

    def get(self, file, index):
        return self.ans[(file, index)].get()

    def gets(self, file):
        return [self.ans[(file, index)].get() for index in range(self.num)]

    def check(self, file):
        for index in range(self.num):
            if self.ans[(file, index)] is None:
                return False
        return True


class TimeTable:
    def __init__(self):
        self.time_table = {}

    def update(self, index):
        if self.time_table.get(index):
            self.time_table[index].update(datetime.now().timestamp())
        else:
            self.time_table[index] = BasicData(datetime.now().timestamp())

    def check(self, index):
        if datetime.now().timestamp() - self.time_table.get(index).get() >= config.overtime_second:
            return True
        return False

    def clear(self):
        self.time_table = {}
