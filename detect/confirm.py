from .receive import Result
from .import common
from .softmax.util import get_sort


# 用于判断两个框的重叠部分是否大于threshold
def overlop(area1: Result, area2: Result, threshold: float) -> bool:
    overlap_width = max(0, min(area1.xmax, area2.xmax) - max(area1.xmin, area2.xmin))
    overlap_height = max(0, min(area1.ymax, area2.ymax) - max(area1.ymin, area2.ymin))
    overlap_area = overlap_width * overlap_height

    area1 = (area1.xmax - area1.xmin) * (area1.ymax - area1.ymin)
    area2 = (area2.xmax - area2.xmin) * (area2.ymax - area2.ymin)

    iou = overlap_area / (area1 + area2 - overlap_area)

    return iou >= threshold


def single_develop(results: []) -> Result:
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

    temp_ans = get_sort(single_model_best)

    for i in range(common.num_detect):
        if temp_ans[i] > max_score:
            max_score = temp_ans[i]
            ans_cls = i

    if ans_cls == 5:
        return Result(0, 5, max_score, 0, 0, 0, 0)
    else:
        ans = Result()
        for result in results:
            if result.cls == ans_cls and result.score * common.weight_dict[result.mid][int(result.cls)] > ans.score:
                ans = result
        ans.score = max_score
        return ans


# 用于判断重叠部分的类别是什么
def single(results: []) -> Result:
    appear_model = {i: False for i in range(common.num_model)}
    single_model_best = [[0.0 for i in range(common.num_model)] for i in range(common.num_detect)]
    sort_ans = [0.0 for i in range(common.num_detect)]
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

    for cls in range(common.num_detect):
        for mid in range(common.num_model):
            sort_ans[cls] += single_model_best[cls][mid] * common.weight_dict[mid][cls]

    for i in range(common.num_detect):
        if sort_ans[i] > max_score:
            max_score = sort_ans[i]
            ans_cls = i

    if ans_cls == 5:
        return Result(0, 5, max_score, 0, 0, 0, 0)
    else:
        ans = Result()
        for result in results:
            if result.cls == ans_cls and result.score * common.weight_dict[result.mid][int(result.cls)] > ans.score:
                ans = result
        ans.score = max_score
        return ans


# 用于对所有的模型的结果进行验证，
def confirm(name, results: []):
    had_sort = {i: False for i in range(len(results))}
    results.sort(key=lambda x: x.score, reverse=True)
    overlop_set = []
    for now in range(len(results)):
        if had_sort[now]:
            continue
        overlop_set.append([results[now]])
        had_sort[now] = True
        for nxt in range(now+1, len(results)):
            if had_sort[nxt]:
                continue
            if overlop(results[now], results[nxt], common.iou_threshold):
                overlop_set[-1].append(results[nxt])
                had_sort[nxt] = True

    output_results = []
    for page in overlop_set:
        # output_results.append(single(page))
        output_results.append(single_develop(page))
    with open(common.output_file, 'a') as output_file:
        for output_result in output_results:
            if output_result.cls != 5 and output_result.score >= common.right_threshold:
                output_file.write(name + " " + str(output_result.cls) + " " + str(output_result.xmin) + " " +
                                  str(output_result.ymin) + " " + str(output_result.xmax) + " " + str(
                    output_result.ymax)+"\n")
