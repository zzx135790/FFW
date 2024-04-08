# from mmdet.apis import init_detector, inference_detector
# config_file = "C:\\Users\\zzx123\\Desktop\\gitpro\\Co-DETR\\work_dirs\\swin_t\\swin_t.py"
# pth_file = "C:\\Users\\zzx123\\Desktop\\gitpro\\Co-DETR\\work_dirs\\swin_t\\latest.pth"
# img_file = "C:\\Users\\zzx123\\Desktop\\work\\temp\\good05.jpg"
# model = init_detector(config=config_file,
#                       checkpoint=pth_file,
#                       device='cuda:0')
#
#
# # results = model(return_loss=False, rescale=True, **data)
# result = inference_detector(model=model, imgs=img_file)
#
# # 打印结果
# for i in result:
#     print(i)

from detect.test import test_model
test_model('test.txt')