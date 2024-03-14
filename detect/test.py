from .confirm import overlop, confirm
from .receive import Result
from .common import model_classes, xml_dir, read_box_from_xml, num_detect
import matplotlib.pyplot as plt
import numpy as np
import os



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
    tp = 0
    fp = 0
    fn = 0
    # 处理每个图像
    for image_name, boxes in image_boxes.items():
        xml_path = os.path.join(xml_dir, os.path.splitext(image_name)[0] + ".xml")
        ans_set = read_box_from_xml(xml_path)
        for result in boxes:
            pre_flag = False
            for right in ans_set:
                if overlop(result, right, 0.5):
                    if right.cls == result.cls:
                        tp += 1
                        pre_flag = True
                        break
            if not pre_flag:
                fp += 1

    # val_set = read_jpg_files("C:\\Users\\zzx123\\Desktop\\work\\temp")
    for filename in os.listdir("C:\\Users\\zzx123\\Desktop\\work\\temp"):
        xml_path = os.path.join(xml_dir, os.path.splitext(image_name)[0] + ".xml")
        ans_set = read_box_from_xml(xml_path)
        for right in ans_set:
            iou_flag = False
            for result in image_boxes.get(filename, []):
                if overlop(result, right, 0.5):
                    iou_flag = True
                    break
            if not iou_flag:
                fn += 1

    precision = tp / (tp + fp)
    recall = tp / (tp+fn)
    print('\ntp=' + str(tp))
    print('fp=' + str(fp))
    print('fn=' + str(fn))
    print('precision=' + str(precision))
    print('recall=' + str(recall))


# 计算整体的mAP
def get_map(all_resutls:[]):
    pr_result = [[(0.0, 1.0)] for i in range(num_detect)]
    fig = plt.figure(figsize=(4, 4), dpi=400)
    plt.xlabel('precision')
    plt.ylabel('recall')
    plt.grid(True)
    for score in np.arange(0, 1, 0.05):
        tp = {cid: 0 for cid in range(num_detect)}
        fp = {cid: 0 for cid in range(num_detect)}
        fn = {cid: 0 for cid in range(num_detect)}
        for result in all_resutls:
            xml_path = os.path.join(xml_dir, os.path.splitext(result[0])[0] + ".xml")
            ans_set = read_box_from_xml(xml_path)
            for box in result[1]:
                if box.score < score or box.cls == 5:
                    continue
                pre_flag = False
                for right_box in ans_set:
                    if overlop(box, right_box, 0.5) and right_box.cls == box.cls:
                        tp[box.cls] += 1
                        tp[5] += 1
                        pre_flag = True
                        break
                if not pre_flag:
                    fp[box.cls] += 1
                    fp[5] += 1

            for right_box in ans_set:
                iou_flag = False
                for box in result[1]:
                    if box.score > score and box.cls != 5 and overlop(box, right_box, 0.5):
                        iou_flag = True
                        break
                if not iou_flag:
                    fn[right_box.cls] += 1
                    fn[5] += 1
        for cid in range(num_detect):
            if tp[cid]+fn[cid] == 0:
                recall = 0
            else:
                recall = tp[cid]/(tp[cid]+fn[cid])

            if tp[cid]+fp[cid] == 0:
                precision = 0
            else:
                precision = tp[cid]/(tp[cid]+fp[cid])

            pr_result[cid].append((recall, precision))

    for cid in range(num_detect):
        ap = 0
        pr_result[cid] = sorted(pr_result[cid], key=lambda x: (x[0], -x[1]))
        pr_result[cid].append((1.0, 0))
        for i in range(1, len(pr_result[cid])):
            ap += pr_result[cid][i][1] * (pr_result[cid][i][0] - pr_result[cid][i-1][0])
        if cid == 5:
            print(f"mAP= {ap}")
            title = "mAP"
        else:
            print(f"{model_classes[cid]} ap= {ap}")
            title = model_classes[cid]
        x = [pt[0] for pt in pr_result[cid]]
        y = [pt[1] for pt in pr_result[cid]]
        plt.plot(x, y, label=title)
    plt.legend()
    plt.show()
    fig.savefig("pr.jpg")

