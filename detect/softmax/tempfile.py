import os
from detect.common import temp_dir

# 输出模型的路径
output_model = os.path.join(temp_dir, 'models/multiDetect.pt')

# 中间件储存的名字
train_set = os.path.join(temp_dir, 'modelData/train.set')
val_set = os.path.join(temp_dir, 'modelData/val.set')

# 中间件的名称
train_data = os.path.join(temp_dir, 'train.data')
val_data = os.path.join(temp_dir, 'val.data')

# 划分train和val的比例
train_ratio = 0.9

# 储存训练图片的目录
# train_img_dir = "F:/ffwb/we_data/2th/data_xml/ori_val"
train_img_dir = "/mnt/workspace/xml_data/Images"

# 储存训练信息的目录
train_xml_dir = "/mnt/workspace/xml_data/Annotations"
# train_xml_dir = "F:/ffwb/we_data/2th/origin_data/xml"



