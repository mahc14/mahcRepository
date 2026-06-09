import numpy as np


def calculate(lst):
    if len(lst) < 9:
        raise ValueError("A lista deve conter nove números.")

    m = np.array(lst).reshape(3, 3)

    return {
        'mean':               [m.mean(axis=0).tolist(), m.mean(axis=1).tolist(), m.mean().tolist()],
        'variance':           [m.var(axis=0).tolist(),  m.var(axis=1).tolist(),  m.var().tolist()],
        'standard deviation': [m.std(axis=0).tolist(),  m.std(axis=1).tolist(),  m.std().tolist()],
        'max':                [m.max(axis=0).tolist(),  m.max(axis=1).tolist(),  m.max().tolist()],
        'min':                [m.min(axis=0).tolist(),  m.min(axis=1).tolist(),  m.min().tolist()],
        'sum':                [m.sum(axis=0).tolist(),  m.sum(axis=1).tolist(),  m.sum().tolist()],
    }
