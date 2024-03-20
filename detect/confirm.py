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
            temp_score = model_path(filp_data)
        elif method == "ratio":
            temp_score = ratio_path(filp_data)
        # result.cls = int(temp_score.argmax(dim=1))
        result.score = temp_score[0][result.cls]
        return result


# 使用wbf进行框融合
def wbf(results: [], num):
    if not len(results):
        return Result()

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


def single(results: [], method) -> Result:
    fin_results = []
    single_best = max(results, key=lambda x: x.score)
    for result in results:
        if result.cls == single_best.cls and result.score >= common.right_threshold:
            fin_results.append(result)

    if single_best.cls == 5:
        return Result(0, 5, single_best.score, 0, 0, 0, 0)
    else:
        cls_result = []
        ans = wbf(fin_results, 2)
        return ans


# 用于对所有的模型的结果进行验证，
def confirm(name, results: [], mode="detect", method="model"):
    results = [get_score(r, method) for r in results]
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
        output_results.append(single(page, method))

    if mode == "detect":
        output_file(name, output_results)
    elif mode == "model" or mode == "mAP":
        return output_results

# 输出到文件
def output_file(name, output_results):
    with open(common.output_file, 'a') as out_file:
        for output_result in output_results:
            if output_result.cls != 5 and output_result.score >= common.right_threshold:
                out_file.write(name + " " + str(output_result.cls) + " " + str(output_result.xmin) + " " +
                               str(output_result.ymin) + " " + str(output_result.xmax) + " " + str(
                    output_result.ymax) + "\n")