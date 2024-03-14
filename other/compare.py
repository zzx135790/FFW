import os

# 定义图片和XML文件夹的路径
images_folder_path = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train"
xml_folder_path = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train_xmls"

def get_filenames_without_extension(folder_path, extension):
    """
    获取指定文件夹内特定扩展名文件的名称（不含扩展名）。
    """
    filenames = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(extension):
                filename_without_extension = os.path.splitext(file)[0]
                filenames.append(filename_without_extension)
    return filenames

# 获取图片和XML文件的名称（不包括扩展名）
image_names = get_filenames_without_extension(images_folder_path, '.jpg')
xml_names = get_filenames_without_extension(xml_folder_path, '.xml')

# 找出所有存在于图片列表中但不在XML列表中的项目
missing_xmls = set(xml_names) - set(image_names)

# 打印这些项目的名称
print("以下图片缺失对应的XML文档：")
for name in missing_xmls:
    print(name)
