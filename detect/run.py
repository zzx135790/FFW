from .common import models_path, num_model, folder_path, read_jpg_files, config_path, output_file, test_dir
from .threads import YoloThread, CodetrThread
from .confirm import confirm
from .test import get_map
from detect.softmax.outfeature import output_dataset
from detect.softmax.train import train
from detect.softmax.makeset import mk_set, cln_set
from detect.softmax.tempfile import train_img_dir, train_data, val_data, train_set, val_set
from ultralytics import YOLO
from mmdet.apis import init_detector
from tqdm import tqdm
from io import StringIO
import sys
import os


def run(mode='detect'):
    """
        总体运行函数
        args：
            mode 用于切换模式，
                其中detect是运行检测，最终得到的是检测结果
                train_mmodel是用于训练中间件模型
                map 用于得出mAP分析结果
    """
    with open(output_file, 'w') as file:
        file.write('')
    model_list = [None for i in range(num_model)]
    threads_list = [None for i in range(num_model)]

    if mode == 'detect':
        file_list = read_jpg_files(folder_path)
    elif mode == 'train_mmodel':
        file_list = read_jpg_files(train_img_dir)
    elif mode == "mAP":
        file_list = read_jpg_files(test_dir)
        all_results = []

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = StringIO()
    sys.stderr = StringIO()

    for i in range(num_model):
        if config_path[i] == '':
            model_list[i] = YOLO(models_path[i])
        else:
            model_list[i] = init_detector(config_path[i], models_path[i], device='cuda:0')

    sys.stdout = old_stdout
    sys.stderr = old_stderr

    for file in tqdm(file_list, desc='Processing', unit='items'):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        single_results = []
        for i in range(num_model):
            if config_path[i] == '':
                threads_list[i] = YoloThread("yolo " + str(i), i, model_list[i], file)
            else:
                threads_list[i] = CodetrThread("codetr" + str(i), i, model_list[i], file)
            threads_list[i].start()

        for i in range(num_model):
            threads_list[i].join()
            for single in threads_list[i].results:
                single_results.append(single)

        if mode == 'detect':
            confirm(os.path.basename(file), single_results)
        elif mode == 'train_mmodel':
            output_dataset(os.path.basename(file), single_results)
        elif mode == "mAP":
            all_results.append((os.path.basename(file), confirm(os.path.basename(file), single_results, "mAP")))

        sys.stdout = old_stdout
        sys.stderr = old_stderr

    if mode == "mAP":
        get_map(all_results)


def train_mmodels():
    if not os.path.exists(os.path.dirname(train_data)):
        try:
            os.makedirs(os.path.dirname(train_data))
        except OSError as exc:  # 防止并发创建目录时出错
            if exc.errno != os.errno.EEXIST:
                raise

    if not (os.path.exists(train_data) and os.path.exists(val_data)):
        with open(train_data, 'w') as train_out:
            with open(val_data, 'w') as val_out:
                train_out.write('')
                val_out.write('')
        run(mode='train_mmodel')

    if not (os.path.exists(train_set) and os.path.exists(val_set)):
        mk_set()
        cln_set()

    train()
