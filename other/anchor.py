# # -*- coding: utf-8 -*-
# # @Time    : 20-2-13 下午5:03
# # @Author  : wusaifei
# # @FileName: Vision_data.py
# # @Software: PyCharm
#
# import pandas as pd
# import seaborn as sns
# import numpy as np
# import json
# import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['font.family']='sans-serif'
# plt.rcParams['figure.figsize'] = (10.0, 10.0)
#
#
# # 读取数据
# ann_json = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\we_data\\data_coco\\annotations\\train.json"
# with open(ann_json) as f:
#     ann=json.load(f)
#
# #################################################################################################
# #创建类别标签字典
# category_dic=dict([(i['id'],i['name']) for i in ann['categories']])
# counts_label=dict([(i['name'],0) for i in ann['categories']])
# for i in ann['annotations']:
#     counts_label[category_dic[i['category_id']]]+=1
#
# # 标注长宽高比例
# box_w = []
# box_h = []
# box_wh = []
# categorys_wh = [[] for j in range(10)]
# for a in ann['annotations']:
#     if a['category_id'] != 0:
#         box_w.append(round(a['bbox'][2],2))
#         box_h.append(round(a['bbox'][3],2))
#         wh = round(a['bbox'][2]/a['bbox'][3],0)
#         if wh <1 :
#             wh = round(a['bbox'][3]/a['bbox'][2],0)
#         box_wh.append(wh)
#
#         categorys_wh[a['category_id']-1].append(wh)
#
#
# # 所有标签的长宽高比例
# box_wh_unique = list(set(box_wh))
# box_wh_count=[box_wh.count(i) for i in box_wh_unique]
#
# # 绘图
# wh_df = pd.DataFrame(box_wh_count,index=box_wh_unique,columns=['宽高比数量'])
# wh_df.plot(kind='bar',color="#55aacc")
# plt.show()

import json
import matplotlib.pyplot as plt

# 步骤1：读取COCO标注文件
with open("C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\we_data\\data_coco\\annotations\\train.json") as f:
    coco_data = json.load(f)

# 步骤2：提取每个标注框的宽度和高度
widths = []
heights = []

for annotation in coco_data['annotations']:
    bbox = annotation['bbox']  # bbox格式通常是[x_min, y_min, width, height]
    widths.append(bbox[2])
    heights.append(bbox[3])

# 步骤3：计算长宽比
aspect_ratios = [w/h for w, h in zip(widths, heights)]

# 步骤4：分析长宽比分布
plt.figure(figsize=(10, 6))
plt.hist(aspect_ratios, bins=50, color='blue', edgecolor='black', alpha=0.7)
plt.title('Aspect Ratio Distribution of Bounding Boxes')
plt.xlabel('Aspect Ratio (Width/Height)')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

