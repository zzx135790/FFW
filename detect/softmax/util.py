import os.path
import torch
from .tempfile import output_model
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
    partition = x_exp.sum(0, keepdim=True)
    return x_exp / partition


def get_sort(results: []):
    input = torch.tensor(results).flatten()
    return softmax(model(input))


