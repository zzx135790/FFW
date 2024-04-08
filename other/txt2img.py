from PIL import Image, ImageDraw, ImageFont
import os

# 设定图片文件夹的路径和文本文件路径
image_folder_path = 'C:/Users/zzx123/Desktop/data/test'
file_path = 'C:/Users/zzx123/Desktop/data/test.txt'

# 设定框的颜色和类别标签
box_color = [('good', 'red'), ('broke', 'green'), ('lose', 'blue'), ('uncovered', 'yellow'), ('circle', 'black')]

# 解析文本文件，按图像组织边界框数据
boxes_by_image = {}
with open(file_path, 'r') as file:
    for line in file.readlines():
        parts = line.strip().split(' ')
        if len(parts) == 6:
            image_name, category_index, xmin, ymin, xmax, ymax = parts
            category_index = int(category_index)
            if image_name not in boxes_by_image:
                boxes_by_image[image_name] = []
            boxes_by_image[image_name].append((category_index, xmin, ymin, xmax, ymax))

# 遍历每张图像，绘制所有边界框和类别名称
for image_name, boxes in boxes_by_image.items():
    image_path = os.path.join(image_folder_path, image_name)
    try:
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            for box in boxes:
                category_index, xmin, ymin, xmax, ymax = box
                label, color = box_color[category_index]

                # 绘制边界框
                draw.rectangle([float(xmin), float(ymin), float(xmax), float(ymax)], outline=color, width=3)

                # 绘制类别名称
                try:
                    font = ImageFont.truetype("arial.ttf", 20)  # 尝试使用Arial字体
                except IOError:
                    font = ImageFont.load_default()  # 否则使用默认字体
                draw.text((float(xmin), float(ymin) - 10), label, fill=color, font=font)

            # 保存修改后的图像
            save_path = os.path.join(image_folder_path, f"processed_{image_name}")
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img.save(save_path)
            print(f"Image processed and saved: {save_path}")
    except FileNotFoundError:
        print(f"Image file not found: {image_path}")
