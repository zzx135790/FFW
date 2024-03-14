from mmdet.apis import init_detector, inference_detector

# 目标检测配置文件
config_file = "C:/Users/zzx123/Desktop/gitpro/Co-DETR/work_dirs/swin_t/swin_t.py"
# 训练模型
checkpoint_file = "C:/Users/zzx123/Desktop/gitpro/Co-DETR/work_dirs/swin_t/latest.pth"

# 配置模型
model = init_detector(config=config_file,
                      checkpoint=checkpoint_file,
                      device='cuda:0')

img = "C:/Users/zzx123/Desktop/gitpro/Co-DETR/data/train_coco/images/train/well0_0006.jpg"
#  推理实际调用语句
# results = model(return_loss=False, rescale=True, **data)
result = inference_detector(model=model, imgs=img)

from PIL import Image, ImageDraw
# 打开原图
img = Image.open(img).convert('RGB')
# 画出目标框，因为一个类别可能对应多个目标
temp = []
smax = 0
sort = -1
for re in range(len(result)):
    for rec in result[re]:
        if rec[4] > smax:
            smax = rec[4]
            temp = rec
            sort = re

draw = ImageDraw.Draw(img)
draw.rectangle((temp[0], temp[1], temp[2], temp[3]), width=2, outline='#41fc59')
print(sort)
print(temp[4])
# 保存结果图片
img.save('result.png')