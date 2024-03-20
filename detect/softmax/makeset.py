import random
import torch
from torchvision import transforms
from torch.utils.data import Dataset
from torch import tensor
import os
from detect.common import model_classes, num_model, num_detect
from .tempfile import train_data, val_data, train_set, val_set, train_xml_dir


class MyDataset(Dataset):
    def __init__(self, file_name):
        self.data = []
        self.labels = []
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                # 将行分割成各个部分
                parts = line.strip().split()
                self.data.append(torch.reshape(torch.Tensor(list(map(float, parts[0:num_detect*num_model]))), [-1, num_detect, num_model]))
                self.labels.append(int(parts[num_model*num_detect]))
        self.data = torch.stack(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.labels[idx]

    def __len__(self):
        return self.data.shape[0]


def mk_set():
    from detect.confirm import overlop
    from detect.receive import Result
    import xml.dom.minidom
    read_files = [train_data, val_data]

    for mode in range(2):
        class2num = {model_classes[i]: i for i in range(5)}

        if not os.path.exists(os.path.dirname(train_set)):
            try:
                os.makedirs(os.path.dirname(train_set))
            except OSError as exc:  # 防止并发创建目录时出错
                if exc.errno != os.errno.EEXIST:
                    raise

        # 读取包含边界框信息的文档
        with open(read_files[mode], 'r') as file:
            lines = file.readlines()

        # 存储每个图像的边界框信息
        image_boxes = {}

        # 储存输出信息
        output_list = []

        # 遍历文档中的每一行
        for line in lines:
            # 将行分割成各个部分
            parts = line.strip().split()

            # 提取信息
            image_filename = parts[0]
            xmin, ymin, xmax, ymax = map(float, parts[1:5])
            featrues = parts[5:6 + num_detect * num_model]

            # 如果图像尚未在字典中，将其添加
            if image_filename not in image_boxes:
                image_boxes[image_filename] = []

            # 将边界框信息添加到图像的边界框列表中
            image_boxes[image_filename].append(
                (Result(0, 0, 0, xmin, xmax, ymin, ymax), featrues)
            )

        for image_name, boxes in image_boxes.items():
            xml_path = os.path.join(train_xml_dir, image_name[:image_name.rindex(".")] + ".xml")
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
                hit_flag = True
                for right in ans_set:
                    if overlop(result[0], right, 0.5):
                        hit_flag = False
                        result[1].append(str(right.cls))
                        output_list.append(result[1])
                        break
                if hit_flag:
                    result[1].append('5')
                    output_list.append(result[1])

        if not mode:
            file_name = train_set
            # if os.path.exists(train_data):
            #     os.remove(train_data)
            #     print(f"文件 {train_data} 已被删除, train数据集即将建立")
        else:
            file_name = val_set
            # if os.path.exists(val_data):
            #     os.remove(val_data)
            #     print(f"文件 {val_data} 已被删除, val数据集即将建立")

        with open(file_name, 'w') as output_file:
            for output_result in output_list:
                ss = ''
                for i in map(lambda x: x + ' ', output_result):
                    ss += i
                ss += '\n'
                output_file.write(ss)


def cln_set():
    read_files = [train_set, val_set]
    for mode in range(2):
        with open(read_files[mode], 'r') as file:
            lines = file.readlines()

        # 存储每个图像的边界框信息
        image_boxes = {i: 0 for i in range(6)}
        output_list = []
        cls_ratio = [0, 0, 0, 0.5, 0.25, 0.98]

        print("Before balance:")
        # 遍历文档中的每一行
        for line in lines:
            parts = line.strip().split()
            cls = int(parts[num_model * num_detect])
            image_boxes[cls] += 1
            # num_dont = float(parts[num_model*(num_detect-1)]) + float(parts[num_model*(num_detect-1)+1]) + float(parts[num_model*(num_detect-1)+2]) + float(parts[num_model*(num_detect-1)+3])
            if cls == 4 and random.random() >= cls_ratio[4]:
                output_list.append(line)
                output_list.append(line)
            elif cls == 0 and random.random() < cls_ratio[0]:
                pass
            elif cls == 3 and random.random() < cls_ratio[3]:
                pass
            elif cls == 5 and random.random() < cls_ratio[5]:
                if float(parts[num_model*(num_detect-1)]) + float(parts[num_model*(num_detect-1)+1]) + float(parts[num_model*(num_detect-1)+2]) + float(parts[num_model*(num_detect-1)+3]) > 2:
                    pass
            else:
                output_list.append(line)

        for i, j in image_boxes.items():
            print(i, j)

        # 输出均衡后的数目
        print("After balance:")
        image_boxes = {i: 0 for i in range(6)}
        for line in output_list:
            parts = line.strip().split()
            image_boxes[int(parts[num_model*num_detect])] += 1
        for i, j in image_boxes.items():
            print(i, j)

        with open(read_files[mode], 'w') as output_file:
            for line in output_list:
                output_file.write(line)
