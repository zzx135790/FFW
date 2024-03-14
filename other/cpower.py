ori_map = [
    [0.713, 0.853, 0.838, 0.87, 0.299],
    [0.719, 0.857, 0.826, 0.896, 0.224],
    [0.684, 0.845, 0.825, 0.876, 0.217],
    [0.539, 0.582, 0.742, 0.573, 0.355]
]

result = [[], [], [], []]

for i in range(0, 5):
    ss = 0
    for j in range(0,4):
        ss += ori_map[j][i]
    for j in range(0,4):
        result[j].append(ori_map[j][i] / ss)

print(result)
