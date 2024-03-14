import xml.dom.minidom
from PIL import Image
import os

sort = {
    "good": 0,
    "broke": 1,
    "lose": 2,
    "uncovered": 3,
    "circle": 4,
}

imgfile = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train"
goalDir = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train_txt"
originDir = "C:\\Users\\zzx123\\Desktop\\work\\竞赛\\服务外包\\2024中国大学生服务外包创新创业大赛data\\train_xmls"

for ori, dirs, files in os.walk(originDir):
    for file in files:
        of = os.path.join(ori, file)
        dom = xml.dom.minidom.parse(of)
        root = dom.documentElement
        imgWid = float(root.getElementsByTagName("width")[0].firstChild.data)
        imgHei = float(root.getElementsByTagName("height")[0].firstChild.data)
        filename, _ = os.path.splitext(file)
        goalFilePath = os.path.join(goalDir, filename+".txt")

        updateNeeded = False

        if imgWid == 0 or imgHei == 0:
            updateNeeded = True
            relPath = root.getElementsByTagName("path")[0].firstChild.data
            imgPath = os.path.abspath(os.path.join(os.path.dirname(of), relPath))
            img = Image.open(imgPath)
            imgWid, imgHei = img.size

            # 更新宽度和高度
            root.getElementsByTagName("width")[0].firstChild.data = str(imgWid)
            root.getElementsByTagName("height")[0].firstChild.data = str(imgHei)

        if updateNeeded:
            # 将更新写回文件
            with open(of, 'w') as f:
                dom.writexml(f, addindent='  ', newl='', encoding='utf-8')

