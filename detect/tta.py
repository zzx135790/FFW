import cv2
from .receive import Result


# 对于输入进行增强
def tta_in(ori_img):
    """
        tta增强输入图片，目前有考虑的：
            1. 水平翻转
            2. 垂直翻转
            3. 旋转 90, 180, 270
    """
    # print("tta_in")
    return [ori_img,
            cv2.flip(ori_img, 0),
            # cv2.flip(ori_img, 1)]
            cv2.rotate(ori_img, cv2.ROTATE_90_CLOCKWISE),
            # cv2.rotate(ori_img, cv2.ROTATE_180),
            # cv2.rotate(ori_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
           ]


# 对于输出结果进行转换
def tta_out(results: list, w, h) -> list:
    # 原始图像直接转换
    ans = [result for result in results[0]]

    # 垂直翻转转换
    for result in results[1]:
        x2max, x2min, y2min, y2max = result.xmax, result.xmin, result.ymin, result.ymax
        result.ymin = h - y2max
        result.ymax = h - y2min
        ans.append(result)

    # # 水平翻转转换
    # for result in results[2]:
    #     x2max, x2min = result.xmax, result.xmin
    #     result.xmin = w - x2max
    #     result.xmax = w - x2min
    #     ans.append(result)

    # 90旋转转换
    for result in results[2]:
        x2max, x2min, y2min, y2max = result.xmax, result.xmin, result.ymin, result.ymax
        result.xmin = y2min
        result.xmax = y2max
        result.ymin = h - x2max
        result.ymax = h - x2min
        ans.append(result)

#     # 180旋转转换
#     for result in results[4]:
#         x2max, x2min, y2min, y2max = result.xmax, result.xmin, result.ymin, result.ymax
#         result.xmin = w - x2max
#         result.xmax = w - x2min
#         result.ymin = h - y2max
#         result.ymax = h - y2min
#         ans.append(result)

#     # 270旋转转换
#     for result in results[5]:
#         x2max, x2min, y2min, y2max = result.xmax, result.xmin, result.ymin, result.ymax
#         result.xmin = w - y2max
#         result.xmax = w - y2min
#         result.ymin = x2min
#         result.ymax = x2max
#         ans.append(result)

    return ans


