# file = "val.txt"
# with open(file, 'r') as file:
#     lines = file.readlines()
#
# # 存储每个图像的边界框信息
# image_boxes = { i:0 for i in range(6)}
# output_list = []
# param = 0
# # 遍历文档中的每一行
# for line in lines:
#     parts = line.strip().split()
#     image_boxes[int(parts[24])] += 1
#     if int(parts[24]) == 5 and float(parts[20]) == 1 and float(parts[21]) == 1 and float(parts[22]) == 1:
#         param = (param + 1) % 50
#         if param % 50 == 0:
#             output_list.append(line)
#     else:
#         output_list.append(line)
#
# for i,j in image_boxes.items():
#     print(i, j)
#
# with open("val1.txt", 'w') as output_file:
#     for l in output_list:
#         output_file.write(l)

# import detect.common as common
# file = "val.txt"
# with open(file, 'r') as file:
#     lines = file.readlines()
#
# # 存储每个图像的边界框信息
#
# TP = 0
# FP = 0
#
#
# # 遍历文档中的每一行
# for line in lines:
#     parts = line.strip().split()
#     sort_ans = [0.0 for i in range(common.num_detect)]
#     single_model_best = [[0.0 for i in range(common.num_model)] for i in range(common.num_detect)]
#     max_score = 0
#     ans_cls = 0
#     for i in range(common.num_detect):
#         for j in range(common.num_model):
#             single_model_best[i][j] = float(parts[i*common.num_model+j])
#
#     for cls in range(common.num_detect):
#         for mid in range(common.num_model):
#             sort_ans[cls] += single_model_best[cls][mid] * common.weight_dict[mid][cls]
#
#     for i in range(common.num_detect):
#         if sort_ans[i] > max_score:
#             max_score = sort_ans[i]
#             ans_cls = i
#
#     if ans_cls == int(parts[24]):
#         TP += 1
#     else:
#         FP += 1
#
# print(TP/(TP+FP))


import detect.softmax.util as st
st.load_model()
result = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
print(st.softmax(st.get_sort(result)))
print(st.get_sort(result))