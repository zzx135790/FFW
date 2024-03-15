ori_map = [
    good ap= 0.8379590360562696
    broke ap= 0.6766702220710803
    lose ap= 0.8808697511466254
    uncovered ap= 0.9364508273983682
    circle ap= 0.27855477855477856
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
