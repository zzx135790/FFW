import cv2


# 对于输入进行增强
def tta_in(file_name):
    """
        tta增强输入图片，目前有考虑的：
            1. 水平翻转
            2. 垂直翻转
            3. 旋转 90, 180, 270
    """
    ori_img = cv2.imread(file_name)
    return [ori_img,
            cv2.flip(ori_img, 0),
            cv2.flip(ori_img, 1),
            cv2.rotate(ori_img, cv2.ROTATE_90_CLOCKWISE),
            cv2.rotate(ori_img, cv2.ROTATE_180),
            cv2.rotate(ori_img, cv2.ROTATE_90_COUNTERCLOCKWISE)]
