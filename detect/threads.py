import threading
from mmdet.apis import inference_detector
from .common import num_detect
from .receive import Result


class YoloThread(threading.Thread):
    def __init__(self, thread_name, mid, model, pic_path):
        # 注意：一定要显式的调用父类的初始化函数。
        super(YoloThread, self).__init__(name=thread_name)
        self.results = None
        self.pic_path = pic_path
        self.model = model
        self.mid = mid

    def run(self):
        yolo_results = self.model(self.pic_path)
        xyxy = yolo_results[0].boxes.xyxy.cpu().numpy()
        cls = yolo_results[0].boxes.cls.cpu().numpy()
        conf = yolo_results[0].boxes.conf.cpu().numpy()
        self.results = []
        for i in range(len(cls)):
            self.results.append(Result(self.mid, cls[i]-1, conf[i], xyxy[i][0], xyxy[i][2], xyxy[i][1], xyxy[i][3]))

    def stop(self):
        self._stop_event.set()


class CodetrThread(threading.Thread):
    def __init__(self, thread_name, mid, model, pic_path):
        # 注意：一定要显式的调用父类的初始化函数。
        super(CodetrThread, self).__init__(name=thread_name)
        self.results = None
        self.pic_path = pic_path
        self.model = model
        self.mid = mid

    def run(self):
        results = inference_detector(self.model, self.pic_path)
        self.results = []
        for single_sort in range(num_detect - 1):
            for detect in results[single_sort]:
                self.results.append(Result(self.mid, single_sort, detect[4], detect[0], detect[2], detect[1], detect[3]))

    def stop(self):
        self._stop_event.set()


class Signal:
    # 用于多线程
    def __init__(self):
        self.thrd = []
        self.ste = 0

    def state(self):
        return self.ste

    def change_state(self):
        self.ste ^= 1

    def push(self, state):
        self.thrd.append(state)

    def clear(self):
        self.__init__()

    def __len__(self):
        return len(self.thrd)