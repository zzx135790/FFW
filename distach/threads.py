import detect.threads as thd


class Client_yolo(thd.YoloThread):
    def __init__(self, thread_name, mid, model, img, gid=0):
        # 注意：一定要显式的调用父类的初始化函数。
        super(Client_yolo, self).__init__(thread_name=thread_name, mid=mid, model=model, pic_path='', gid=gid)
        self.pic = img


class Client_mmd(thd.CodetrThread):
    def __init__(self, thread_name, mid, model, img):
        # 注意：一定要显式的调用父类的初始化函数。
        super(Client_mmd, self).__init__(thread_name=thread_name, mid=mid, model=model, pic_path='')
        self.pic = img

