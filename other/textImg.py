import os

def check_files(folder_path):
    # 存储包含大于1的数字（除了每行的第一个数字）的文件名
    files_with_values_over_one = []

    # 遍历指定文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # 分割每行并转换为浮点数，除了第一个数字
                    values = [float(value) for value in line.split()[1:]]
                    # 检查是否有任何值大于1
                    if any(value > 1 for value in values):
                        files_with_values_over_one.append(filename)
                        break  # 找到一个就足够了，无需检查更多行
        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    return files_with_values_over_one

# 指定要检查的文件夹路径
folder_path = 'C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train_txt'
# 调用函数并打印结果
files = check_files(folder_path)
print("Files with values over 1 (excluding the first number in each line):")
for file in files:
    print(file)
