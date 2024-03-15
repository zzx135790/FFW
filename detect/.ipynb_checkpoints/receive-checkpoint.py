from io import StringIO
class Result:
    # mid:模型编号， cls:类别id
    def __init__(self, mid=0, cls=0, score=0, xmin=0, xmax=0, ymin=0, ymax=0):
        self.mid = int(mid)
        self.cls = int(cls)
        self.score = score
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax


# 空对象，用于重定向子线程的输出
class DevNull(StringIO):
    def write(self, msg):
        pass
