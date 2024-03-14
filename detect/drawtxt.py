import cv2
import os
from .common import folder_path, model_classes
# 读取包含边界框信息的文档
with open('../result.txt', 'r') as file:
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
    image_path = os.path.join(folder_path, image_filename)

    # 如果图像尚未在字典中，将其添加
    if image_path not in image_boxes:
        image_boxes[image_path] = []

    # 将边界框信息添加到图像的边界框列表中
    image_boxes[image_path].append({
        'category_id': category_id,
        'xmin': xmin,
        'ymin': ymin,
        'xmax': xmax,
        'ymax': ymax
    })

# 处理每个图像
for image_path, boxes in image_boxes.items():
    # 读取图像
    image = cv2.imread(image_path)

    # 在图像上绘制每个边界框和标签
    color = (0, 255, 0)  # 边界框的绿色
    thickness = 2
    for box in boxes:
        category_id = box['category_id']
        xmin, ymin, xmax, ymax = map(int, [box['xmin'], box['ymin'], box['xmax'], box['ymax']])
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)
        cv2.putText(image, f'category: {model_classes[category_id]}', (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, thickness)

    # 保存修改后的图像到指定文件夹
    output_folder = 'C:\\Users\\zzx123\\Desktop\\work\\outimg2'
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, os.path.basename(image_path))
    cv2.imwrite(output_path, image)
    # cv2.imshow('Image with Bounding Box', image)
    # cv2.waitKey(0)
cv2.destroyAllWindows()

