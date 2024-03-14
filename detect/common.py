import os

message2num = {
    "SUCCESS_DETECT": 0,
    "FAILED_DETECT": 1,
}

# 用于将错误代码装换为输出文字
num2message = {
    0: "success output",
    1: "had some error in detect",
    2: "input model data's num is different to model num in common.py"
}

# 用于判断是否正确的阈值
right_threshold = 0

# 用于判断两个框是否重叠的阈值
iou_threshold = 0.5

# 用于判断具体类别的模型数量
num_model = 4

# 用于填写需要精确检测的种类数目,注意这个地方可能需要加入背景一类
num_detect = 6

# 权重字典，需要自定义
weight_dict = {
    0: [0.2685499058380414, 0.271915843162257, 0.25936242649334573, 0.27060653188180406, 0.2730593607305936, 0.25],
    1: [0.2708097928436911, 0.2731909467644246, 0.25564840606623335, 0.2786936236391913, 0.2045662100456621, 0.25],
    2: [0.2576271186440678, 0.2693656359579216, 0.255338904363974, 0.2724727838258165, 0.19817351598173516, 0.25],
    3: [0.20301318267419963, 0.1855275741153969, 0.22965026307644693, 0.17822706065318816, 0.3242009132420091, 0.25]
}

# model_config路径，目前是co-detr会使用
config_path = [
    '',
    '/mnt/workspace/Co-detr/work_dirs/swin-b/gc/swinb-GC.py',
    "/mnt/workspace/Co-detr/work_dirs/codetr_r50_size/codetr_r101_size.py",
    "/mnt/workspace/Co-detr/work_dirs/swin-b/deroi/swinb-deroi.py"
]

# model路径
models_path = [
    "/mnt/workspace/Co-detr/work_dirs/yolo/yolov8n.pt",
    "/mnt/workspace/Co-detr/work_dirs/swin-b/gc/best_bbox_mAP_epoch_3.pth",
    "/mnt/workspace/Co-detr/work_dirs/codetr_r50_size/best_bbox_mAP_epoch_12.pth",
    "/mnt/workspace/Co-detr/work_dirs/swin-b/deroi/best_bbox_mAP_epoch_4.pth"
]

# 输出文件的路径
output_file = "test_fastrcnn.txt"

# 检测的文件夹路径
folder_path = "C:\\Users\\zzx123\\Desktop\\work\\temp"

# 类别信息
model_classes = ['good', 'broke', 'lose', 'uncovered', 'circle']

# 储存中间信息的文件夹
temp_dir = './temp/'

# 测试的目标文件夹
test_dir = "/mnt/workspace/temp/images/val"

# 测试使用的目标框文件夹，注意是voc格式的信息，全部放在一个文件夹下
xml_dir = "/mnt/workspace/xml_data/Annotations"


# 程序错误退出的函数
def error_return(eid: int):
    print(num2message.get(eid))
    exit(0)


# 读取文件夹内照片
def read_jpg_files(_folder_path):
    jpg_files = []
    for filename in os.listdir(_folder_path):
        if filename.endswith('.jpg'):
            file_path = os.path.join(_folder_path, filename)
            jpg_files.append(file_path)
    return jpg_files


# 从xml文件中读取目标框
def read_box_from_xml(xml_path):
    import xml.dom.minidom
    from .receive import Result
    class2num = {model_classes[i]: i for i in range(5)}
    dom = xml.dom.minidom.parse(xml_path)
    root = dom.documentElement
    ans_set = []
    for id in range(len(root.getElementsByTagName("name"))):
        type = root.getElementsByTagName("name")[id].firstChild.data
        xmin = float(root.getElementsByTagName("xmin")[id].firstChild.data)
        ymin = float(root.getElementsByTagName("ymin")[id].firstChild.data)
        xmax = float(root.getElementsByTagName("xmax")[id].firstChild.data)
        ymax = float(root.getElementsByTagName("ymax")[id].firstChild.data)
        typeId = class2num[type]
        ans_set.append(Result(0, typeId, 0, xmin, xmax, ymin, ymax))
    return ans_set