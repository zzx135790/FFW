class Result:
    # mid:模型编号， cls:类别id
    def __init__(self, mid=0, cls=0, score=0, xmin=0, xmax=0, ymin=0, ymax=0):
        self.mid = mid
        self.cls = cls
        self.score = score
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

