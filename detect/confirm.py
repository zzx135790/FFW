from .receive import Result
from . import common
from .softmax.util import get_sort, load_model

# 用于判断两个框的重叠部分是否大于threshold
def overlop(area1: Result, area2: Result, threshold: float) -> bool:
    overlap_width = max(0, min(area1.xmax, area2.xmax) - max(area1.xmin, area2.xmin))
    overlap_height = max(0, min(area1.ymax, area2.ymax) - max(area1.ymin, area2.ymin))
    overlap_area = overlap_width * overlap_height

    area1 = (area1.xmax - area1.xmin) * (area1.ymax - area1.ymin)
    area2 = (area2.xmax - area2.xmin) * (area2.ymax - area2.ymin)

    iou = overlap_area / (area1 + area2 - overlap_area)

    return iou >= threshold


# 使用模型来得到最终结果
def model_path(single_best: []):
    load_model()
    return get_sort(single_best)


# 使用分权来得到结果
def ratio_path(single_best: []):
    sort_ans = [0.0 for i in range(common.num_detect)]
    for cls in range(common.num_detect):
        for mid in range(common.num_model):
            sort_ans[cls] += single_best[cls][mid] * common.weight_dict[mid][cls]
    return sort_ans


def get_score(result: Result, method) -> Result:
    filp_data = [[0.0 for _ in range(common.num_model)] for _ in range(common.num_detect)]
    # filp_data[result.cls] = [1.0 for _ in range(common.num_model)]
    filp_data[result.cls][result.mid] = result.score
    if method == "model":
        result.score = model_path(filp_data).max().item()
    elif method == "ratio":
        result.score = ratio_path(filp_data)[result.cls]
    return result


# 使用wbf进行框融合
def wbf(results: [], method, num):
    if not len(results):
        return Result()

    for i in range(len(results)):
        results[i] = get_score(results[i], method)

    results.sort(key=lambda x: x.score, reverse=True)

    ans_box = results[0]

    c = 0
    for re in results:
        if c >= num:
            break
        c += 1
        ans_box.xmin = (ans_box.xmin * ans_box.score + re.xmin * re.score) / (ans_box.score + re.score)
        ans_box.ymin = (ans_box.ymin * ans_box.score + re.ymin * re.score) / (ans_box.score + re.score)
        ans_box.xmax = (ans_box.xmax * ans_box.score + re.xmax * re.score) / (ans_box.score + re.score)
        ans_box.ymax = (ans_box.ymax * ans_box.score + re.ymax * re.score) / (ans_box.score + re.score)
        ans_box.score = (ans_box.score + re.score) / 2

    return ans_box


# 得到一个局域内所有的数据
def area_data(results: []):
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


def single(results: [], method) -> Result:
    appear_model = {i: False for i in range(common.num_model)}
    single_model_best = [[0.0 for i in range(common.num_model)] for i in range(common.num_detect)]
    max_score = 0
    ans_cls = 0
    for result in results:
        appear_model[result.mid] = True
        # sort_ans[int(result.cls)] += result.score * common.weight_dict[result.mid][int(result.cls)]
        if result.score > single_model_best[int(result.cls)][result.mid]:
            single_model_best[int(result.cls)][result.mid] = result.score

    for blank, key in appear_model.items():
        if not key:
            single_model_best[5][blank] = 1.0

    if method == "model":
        temp_ans = model_path(single_model_best)
        ans_cls = temp_ans.argmax(dim=1).item()
    elif method == "ratio":
        temp_ans = ratio_path(single_model_best)
        for i in range(common.num_detect):
            if temp_ans[i] > max_score:
                max_score = temp_ans[i]
                ans_cls = i

    
    if ans_cls == 5:
        return Result(0, 5, max_score, 0, 0, 0, 0)
    else:
        cls_result = []
        for result in results:
            if result.cls == ans_cls:
                cls_result.append(result)
        ans = wbf(cls_result, method, 3)
        ans.score = max_score
        return ans
        # ans = Result()
        # for result in results:
        #     if result.cls == ans_cls:
        #         temp_ans = get_score(result, method)
        #         if temp_ans.score > ans.score:
        #             ans = temp_ans
        # return ans
        # ans = Result()
        # for result in results:
        #     if result.cls == ans_cls and result.score > ans.score:
        #         ans = result
        # ans.score = max_score
        # return ans


# 用于对所有的模型的结果进行验证，
def confirm(name, results: [], mode="detect", method="model"):
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
        if mode == 'train_mmodel':
            output_results.append(area_data(page))
        else:
            output_results.append(single(page, method))

    if mode == "detect":
        output_file(name, output_results)
    elif mode == "mAP" or mode == 'train_mmodel':
        return output_results


# 输出到文件
def output_file(name, output_results):
    with open(common.output_file, 'a') as out_file:
        for output_result in output_results:
            if output_result.cls != 5 and output_result.score >= common.right_threshold:
                out_file.write(name + " " + str(output_result.cls) + " " + str(output_result.xmin) + " " +
                               str(output_result.ymin) + " " + str(output_result.xmax) + " " + str(
                    output_result.ymax) + "\n")
