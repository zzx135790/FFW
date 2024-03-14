import os
import random
import detect.common as common
from detect.confirm import overlop
from .tempfile import train_data, val_data, train_ratio


# 得到一个局域内所有的数据
def single(results: []):
    appear_model = {i: False for i in range(common.num_model)}
    single_model_best = [[0.0 for i in range(common.num_model)] for i in range(common.num_detect)]
    max_score = 0
    ans_boxes = [0, 0, 0, 0]
    for result in results:
        appear_model[result.mid] = True
        if result.score > single_model_best[int(result.cls)][result.mid]:
            single_model_best[int(result.cls)][result.mid] = result.score
        if result.score > max_score:
            max_score = result.score
            ans_boxes = [result.xmin, result.ymin, result.xmax, result.ymax]

    for blank, key in appear_model.items():
        if not key:
            single_model_best[5][blank] = 1.0

    return ans_boxes, single_model_best


# 用于对所有的模型的结果进行验证，
def output_dataset(name, results: []):

    had_sort = {i: False for i in range(len(results))}
    results.sort(key=lambda x: x.score, reverse=True)
    overlop_set = []
    for now in range(len(results)):
        if had_sort[now]:
            continue
        overlop_set.append([results[now]])
        had_sort[now] = True
        for nxt in range(now + 1, len(results)):
            if had_sort[nxt]:
                continue
            if overlop(results[now], results[nxt], common.iou_threshold):
                overlop_set[-1].append(results[nxt])
                had_sort[nxt] = True

    output_results = []
    for page in overlop_set:
        output_results.append(single(page))

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
