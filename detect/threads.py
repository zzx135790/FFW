import threading
import cv2
from mmdet.apis import inference_detector
from .common import num_detect
from .receive import Result
from .tta import tta_in, tta_out


class YoloThread(threading.Thread):
    def __init__(self, thread_name, mid, model, pic_path):
        # 注意：一定要显式的调用父类的初始化函数。
        super(YoloThread, self).__init__(name=thread_name)
        self.results = None
        self.pic = cv2.imread(pic_path)
        self.model = model
        self.mid = mid

    def run(self):
        self.results = []
        h, w = self.pic.shape[:2]
        yolo_results = self.model(tta_in(self.pic), verbose=False)
        for yolo_result in yolo_results:
            xyxy = yolo_result.boxes.xyxy.cpu().numpy()
            cls = yolo_result.boxes.cls.cpu().numpy()
            conf = yolo_result.boxes.conf.cpu().numpy()
            temp_ans = []
            for i in range(len(cls)):
                temp_ans.append(
                    Result(self.mid, cls[i] - 1, conf[i], xyxy[i][0], xyxy[i][2], xyxy[i][1], xyxy[i][3],
                           (xyxy[i][2] - xyxy[i][0]) * (xyxy[i][3] - xyxy[i][1]) / (w * h))
                )
            self.results.append(temp_ans)
        self.results = tta_out(self.results, w, h)

    def stop(self):
        self._stop_event.set()


class CodetrThread(threading.Thread):
    def __init__(self, thread_name, mid, model, pic_path):

        # 注意：一定要显式的调用父类的初始化函数。
        super(CodetrThread, self).__init__(name=thread_name)
        self.results = None
        self.pic = cv2.imread(pic_path)
        self.model = model
        self.mid = mid
        self.threshold = 0.1

    def run(self):
        results = inference_detector(self.model, tta_in(self.pic))
        self.results = []
        w, h = self.pic.shape[:2]
        for page in results:
            temp_ans = []
            for single_sort in range(num_detect - 1):
                for detect in page[single_sort]:
                    if detect[4] > self.threshold:
                        temp_ans.append(
                            Result(self.mid, single_sort, detect[4], detect[0], detect[2], detect[1], detect[3],
                                   (detect[2] - detect[0]) * (detect[3] - detect[1]) / (w * h))
                        )
            self.results.append(temp_ans)
        self.results = tta_out(self.results, w, h)

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
