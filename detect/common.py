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
iou_threshold = 0.3

# 用于判断具体类别的模型数量
num_model = 4

# 用于填写需要精确检测的种类数目,注意这个地方可能需要加入背景一类
num_detect = 6

# # 权重字典，需要自定义
# weight_dict = {
#     0: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# }
#
# # model_config路径，目前是co-detr会使用
# config_path = [
#     '',
#     # '/mnt/workspace/Co-detr/work_dirs/swin-b/gc/swinb-GC.py',
#     # "/mnt/workspace/Co-detr/work_dirs/codetr_r50_size/codetr_r101_size.py",
#     # "/mnt/workspace/Co-detr/work_dirs/swin-b/deroi/swinb-deroi.py"
# ]
#
# # model路径
# models_path = [
#     # "/mnt/workspace/Co-detr/work_dirs/yolo/yolov8n.pt",
#     "C:/Users/zzx123/Desktop/work/竞赛/服务外包/模型/小权重/best.pt",
#     # "/mnt/workspace/Co-detr/work_dirs/swin-b/gc/best_bbox_mAP_epoch_3.pth",
#     # "/mnt/workspace/Co-detr/work_dirs/codetr_r50_size/best_bbox_mAP_epoch_12.pth",
#     # "/mnt/workspace/Co-detr/work_dirs/swin-b/deroi/best_bbox_mAP_epoch_4.pth"
# ]

# 权重字典，需要自定义
weight_dict = {
    0: [0.23669170839797177, 0.2043425930038816, 0.2579645212330585, 0.25916971456176713, 0.14830078793580795, 0.25],
    1: [0.24177602500996623, 0.2505591284505211, 0.2662320889936099, 0.25024286557361036, 0.3245360961945535, 0.25],
    2: [0.25698695992452675, 0.2652949616001609, 0.23601820539956264, 0.2461956380068944, 0.2431197782282009, 0.25],
    3: [0.26454530666753523, 0.2798033169454364, 0.23978518437376897, 0.24439178185772814, 0.2840433376414377, 0.25]
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
output_file = "common.txt"

# 检测的文件夹路径
folder_path = "F:/ffwb/we_data/data_xml/ori_val_rotate"

# 类别信息
model_classes = ['good', 'broke', 'lose', 'uncovered', 'circle']

# 储存中间信息的文件夹
temp_dir = './temp/'

# 测试的目标文件夹
# test_dir = "/mnt/workspace/temp/images/val"
test_dir = "F:/ffwb/we_data/data_xml/ori_val_rotate"

# 测试使用的目标框文件夹，注意是voc格式的信息，全部放在一个文件夹下
# xml_dir = "/mnt/workspace/xml_data/Annotations"
xml_dir = "F:/ffwb/we_data/data_xml/ori_val_rotate"


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