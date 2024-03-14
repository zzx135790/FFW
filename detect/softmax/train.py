from .makeset import MyDataset
from detect.common import  num_detect, num_model
from torch.utils.data import DataLoader
from .tempfile import output_model
import torch
from torch import nn
from torch.nn import init
import sys
import os


def accuracy(y_hat, y):
    return (y_hat.argmax(dim=1) == y).float().mean().item()


def evaluate_accuracy(data_iter, net):
    acc_sum, n = 0.0, 0
    for X, y in data_iter:
        acc_sum += (net(X).argmax(dim=1) == y).float().sum().item()
        n += y.shape[0]
    return acc_sum / n


def train_model(net, train_iter, test_iter, loss, num_epochs, batch_size, params=None, lr=None, optimizer=None):
    for epoch in range(num_epochs):  # 迭代训练轮数
        # 初始化本轮训练损失、训练准确率、样本数量
        train_l_sum, train_acc_sum, n = 0.0, 0.0, 0
        for X, y in train_iter:  # 迭代每个小批量
            y_hat = net(X)  # 前向传播计算预测值

            l = loss(y_hat, y).sum()  # 计算损失

            # 清空梯度
            if optimizer is not None:
                optimizer.zero_grad()
            elif params is not None and params[0].grad is not None:
                for param in params:
                    param.grad.data.zero_()

            l.backward()  # 反向传播计算梯度
            if optimizer is None:
                # 手动更新模型参数
                for param in params:
                    param.data -= lr * param.grad / batch_size  # 注意这里更改param时用的param.data
            else:
                optimizer.step()  # 使用优化器更新模型参数

            train_l_sum += l.item()  # 累计本轮训练损失
            train_acc_sum += (y_hat.argmax(dim=1) == y).sum().item()  # 累计本轮训练正确预测样本数
            n += y.shape[0]  # 累计本轮训练样本数

        test_acc = evaluate_accuracy(test_iter, net)  # 计算测试准确率
        # 输出本轮训练和测试信息
        print('epoch %d, loss %.4f, train acc %.3f, test acc %.3f'
              % (epoch + 1, train_l_sum / n, train_acc_sum / n, test_acc))


def train():
    from .tempfile import train_set, val_set

    if not os.path.exists(os.path.dirname(output_model)):
        try:
            os.makedirs(os.path.dirname(output_model))
        except OSError as exc:  # 防止并发创建目录时出错
            if exc.errno != os.errno.EEXIST:
                raise

    batch_size = 1
    if sys.platform.startswith('win'):
        num_workers = 0  # 0表示不用额外的进程来加速读取数据
    else:
        num_workers = 4

    train_set = MyDataset(train_set)
    val_set = MyDataset(val_set)

    trainloader = DataLoader(train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    valloader = DataLoader(val_set, batch_size=batch_size, shuffle=True, num_workers=num_workers)

    num_inputs = num_detect * num_model
    num_outputs = num_detect

    # 创建网络
    net = nn.Sequential(nn.Linear(num_inputs, num_outputs))

    # 初始化权重参数
    init.normal_(net[0].weight, mean=0, std=0.01)  # 权重
    init.constant_(net[0].bias, val=0)  # 偏置

    # softmax和交叉熵损失函数
    loss = nn.CrossEntropyLoss()

    # 随机梯度下降优化算法
    optimizer = torch.optim.SGD(net.parameters(), lr=0.1)

    train_model(net, trainloader, valloader, loss, 100, batch_size, None, None, optimizer)

    torch.save(net, output_model)
