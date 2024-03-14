import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image


def draw_bbox_from_xml(xml_folder, output_folder):
    # 遍历文件夹中的所有XML文件
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(xml_folder, xml_file)
            # 打开XML文件
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # 推断图像路径
            image_name = os.path.splitext(xml_file)[0] + '.jpg'
            image_path = os.path.join(xml_folder, image_name)

            # 打开图像文件
            image = Image.open(image_path)

            # 绘制图像
            fig, ax = plt.subplots(1)
            ax.imshow(image)

            # 解析XML并绘制边界框
            for obj in root.findall('object'):
                name = obj.find('name').text
                xmin = int(obj.find('bndbox/xmin').text)
                ymin = int(obj.find('bndbox/ymin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymax = int(obj.find('bndbox/ymax').text)

                # 绘制边界框
                rect = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                         linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)

                # 添加信息框
                ax.text(xmin, ymin - 2, name, fontsize=8, color='r', ha='center')

            # 保存绘制好的图片到指定文件夹
            output_path = os.path.join(output_folder, os.path.basename(image_path))
            plt.savefig(output_path)
            plt.close()


# 调用函数
xml_folder = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train_xmls"  # 包含XML文件的文件夹路径
output_folder = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\draw"  # 保存绘制好的图片的文件夹路径
draw_bbox_from_xml(xml_folder, output_folder)
