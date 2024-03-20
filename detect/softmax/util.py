import os.path
import torch
from .tempfile import output_model
import detect.common as common
model = None


def load_model():
    global model
    if model is None and os.path.exists(output_model):
        model = torch.load(output_model)
        model.eval()
    else:
        return


def softmax(x):
    x_exp = torch.exp(x)
    partition = x_exp.sum(1, keepdim=True)
    return x_exp / partition


def get_sort(results: []):
    input = torch.reshape(torch.tensor(results), (-1, 1, common.num_detect, common.num_model))
    return softmax(model(input))