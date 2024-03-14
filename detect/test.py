from .confirm import overlop
from .receive import Result
from .common import model_classes
import os
import xml.dom.minidom


def test_model(file):
    class2num = {model_classes[i]: i for i in range(5)}
    # 读取包含边界框信息的文档
    with open(file, 'r') as file:
        lines = file.readlines()

    # 存储每个图像的边界框信息
    image_boxes = {}

    # 遍历文档中的每一行
    for line in lines:
        # 将行分割成各个部分
        parts = line.strip().split()

        # 提取信息
        image_filename = parts[0]
        category_id = int(float(parts[1]))
        xmin, ymin, xmax, ymax = map(float, parts[2:6])

        # 构建图像的完整路径
        image_path = image_filename

        # 如果图像尚未在字典中，将其添加
        if image_path not in image_boxes:
            image_boxes[image_path] = []

        # 将边界框信息添加到图像的边界框列表中
        image_boxes[image_path].append(
            Result(0, category_id, 0, xmin, xmax, ymin, ymax)
        )

    #
    TP = 0
    FP = 0
    FN = 0
    # 处理每个图像
    for image_name, boxes in image_boxes.items():
        xmlDir = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train_xmls"
        xml_path = os.path.join(xmlDir, os.path.splitext(image_name)[0] + ".xml")
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
        for result in boxes:
            pre_flag = False
            for right in ans_set:
                if overlop(result, right, 0.5):
                    if right.cls == result.cls:
                        TP += 1
                        pre_flag = True
                        break
            if not pre_flag:
                FP += 1

    # val_set = read_jpg_files("C:\\Users\\zzx123\\Desktop\\work\\temp")
    for filename in os.listdir("C:\\Users\\zzx123\\Desktop\\work\\temp"):
        xmlDir = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train_xmls"
        xml_path = os.path.join(xmlDir, os.path.splitext(filename)[0] + ".xml")
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

        for right in ans_set:
            Iou_flag = False
            for result in image_boxes.get(filename, []):
                if overlop(result, right, 0.5):
                    Iou_flag = True
                    break
            if not Iou_flag:
                FN += 1

    precision = TP / (TP + FP)
    recall = TP / (TP+FN)
    print('\nTP=' + str(TP))
    print('FP=' + str(FP))
    print('FN=' + str(FN))
    print('precision=' + str(precision))
    print('recall=' + str(recall))

