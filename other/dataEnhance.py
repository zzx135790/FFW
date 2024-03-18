from PIL import Image, ImageEnhance
import xml.dom.minidom
import os

from PIL import Image, ImageEnhance
import random
from PIL import Image
import xml.etree.ElementTree as ET


# 图片旋转
def rotate_image(image_path, output_image_path, angle):
    image = Image.open(image_path)
    rotated_image = image.rotate(angle, expand=True)
    rotated_image.save(output_image_path)
    return rotated_image.size


# 更新XML标注信息
def update_annotation(xml_path, output_xml_path, new_size, angle, output_img_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 更新图像尺寸
    width, height = new_size
    root.find('size/width').text = str(width)
    root.find('size/height').text = str(height)
    root.find('path').text = output_img_path
    # 仅处理90度旋转的情况
    if angle % 360 == 90:
        for obj in root.findall('object'):
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # 更新边界框坐标
            bndbox.find('xmin').text = str(ymin)
            bndbox.find('ymin').text = str(height - xmax)
            bndbox.find('xmax').text = str(ymax)
            bndbox.find('ymax').text = str(height - xmin)

    tree.write(output_xml_path, encoding='utf-8', xml_declaration=True)

def decrease_brightness(image_path, output_image_path):
    factor = random.uniform(0.2, 1.8)
    # 打开图片
    image = Image.open(image_path)
    # 创建亮度增强器
    enhancer = ImageEnhance.Brightness(image)
    # 调整亮度
    dimmed_image = enhancer.enhance(factor)
    # 保存新的图片
    dimmed_image.save(output_image_path)

def copy_annotation(xml_path, output_xml_path, output_img_path):
    # 读取原始XML
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # 这里可以添加任何必要的XML修改
    root.find('path').text = output_img_path
    # 保存新的XML
    tree.write(output_xml_path, encoding='utf-8', xml_declaration=True)


imgfile = "F:/ffwb/we_data/data_xml/ori_val"
goalDir = "F:/ffwb/we_data/data_xml/ori_val"
originDir = "F:/ffwb/we_data/data_xml/ori_val_rotate"
for ori, dirs, files in os.walk(originDir):
    for file in files:
        of = os.path.join(ori, file)
        dom = xml.dom.minidom.parse(of)
        root = dom.documentElement
        imgWid = float(root.getElementsByTagName("width")[0].firstChild.data)
        imgHei = float(root.getElementsByTagName("height")[0].firstChild.data)

        # filename, prefix_xml = os.path.splitext(file)
        # filename = filename+"_dark"
        # relPath = root.getElementsByTagName("path")[0].firstChild.data
        # OriImgPath = os.path.abspath(os.path.join(os.path.dirname(of), relPath))
        # GoalImgPath = os.path.join(os.path.dirname(OriImgPath), filename+".jpg")
        # GoalXmlPath = os.path.join(ori, filename+".xml")
        # decrease_brightness(OriImgPath, GoalImgPath)
        # copy_annotation(of, GoalXmlPath, GoalImgPath)

        filename, prefix_xml = os.path.splitext(file)
        filename = filename + "_rotate"
        relPath = root.getElementsByTagName("path")[0].firstChild.data
        OriImgPath = os.path.abspath(os.path.join(os.path.dirname(of), relPath))
        GoalImgPath = os.path.join(os.path.dirname(OriImgPath), filename + ".jpg")
        GoalXmlPath = os.path.join(ori, filename + ".xml")
        update_annotation(of, GoalXmlPath, rotate_image(OriImgPath, GoalImgPath, 90), 90, GoalImgPath)