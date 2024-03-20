import os
import random
import detect.common as common
from detect.confirm import overlop, confirm
from .tempfile import train_data, val_data, train_ratio


# 得到一个局域内所有的数据
def flip_data(results: []):
    data = []
    for result in results:
        f_d = [[0.0 for _ in range(common.num_model)] for _ in range(common.num_detect)]
        f_d[result.cls][result.mid] = result.score
        data.append([[result.xmin, result.ymin, result.xmax, result.ymax], f_d])
    return data


# 用于对所有的模型的结果进行验证，
def output_dataset(name, results: []):
    output_results = flip_data(results)
    with open(train_data, 'a') as train_out:
        with open(val_data, 'a') as val_out:
            for output_result in output_results:
                ss = name + ' '
                for box in output_result[0]:
                    ss += str(box) + ' '
                for mm in output_result[1]:
                    for score in mm:
                        ss += str(score) + ' '
                if random.random() > train_ratio:
                    val_out.write(ss+'\n')
                else:
                    train_out.write(ss+'\n')
