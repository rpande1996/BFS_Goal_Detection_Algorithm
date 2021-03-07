import numpy as np
import cv2

obs_map = np.zeros((302, 402), dtype=int)
obs_map[0, :] = 1
obs_map[301, :] = 1
obs_map[:, 0] = 1
obs_map[:, 401] = 1


class Queue:

    def __init__(self):
        self.queue = []

    def add(self, node):
        self.queue.append(node)

    def pop(self):
        node = self.queue[0]
        self.queue = self.queue[1:]
        return node

    def __len__(self):
        return len(self.queue)


class Node:

    def __init__(self, data, parent, act, cost):
        self.data = data
        self.parent = parent
        self.act = act
        self.id = self.get_id()
        self.cost = cost

    def get_id(self):
        _id = np.ravel(self.data).tolist()
        _id = [str(item) for item in _id]
        _id = "-".join(_id)
        self.id = _id
        return self.id

    def __repr__(self):
        return str(self.data)


def getCircleObstacle(i, j):
    cond = ((j - 90) ** 2) + ((i - 70) ** 2) <= 1225
    return cond


def getCShapeObstacle(i, j):
    cond1 = j >= 200
    cond2 = j <= 210
    cond3 = i <= 280
    cond4 = i >= 230
    cond5 = j <= 230
    cond6 = i >= 270
    cond7 = i <= 240
    ret_val = (cond1 and cond2 and cond3 and cond4) or (cond1 and cond5 and cond3 and cond6) or (
            cond1 and cond5 and cond7 and cond4)
    return ret_val


def getSlantedRectObstacle(i, j):
    cond1 = (i) + (1.42814 * j) >= 176.5511
    cond2 = (i) - (0.7 * j) >= 74.39
    cond3 = (i) + (1.42814 * j) <= 428.06815
    cond4 = (i) - (0.7 * j) <= 98.80545
    ret_val = (cond1 and cond2 and cond3 and cond4)
    return ret_val


def getEllipseObstacle(i, j):
    cond = (((j - 246) / 60) ** 2) + (((i - 145) / 30) ** 2) <= 1
    return cond


def getPolygonObstacle(i, j):
    cond1 = i + j >= 391
    cond2 = j - i <= 265
    cond3 = i + 0.49646 * j <= 305.20202
    cond4 = 0.89003 * j - i >= 148.7438
    ret_val = (cond1 and cond2 and cond3 and cond4)
    return ret_val


def getPolygonObstacle2(i, j):
    cond1 = i + 0.49646 * j >= 305.20202
    cond2 = i + 0.81259 * j <= 425.66019
    cond3 = i + 0.17512 * j <= 199.99422
    ret_val = (cond1 and cond2 and cond3)
    return ret_val


def getPolygonObstacle3(i, j):
    cond1 = i + 13.49145 * j <= 5256.7216
    cond2 = 1.43169 * j - i >= 368.82072
    cond3 = i + 0.81259 * j >= 425.66019
    ret_val = (cond1 and cond2 and cond3)
    return ret_val

for i in range(obs_map.shape[0]):
    for j in range(obs_map.shape[1]):
        if getCircleObstacle(obs_map.shape[0] - i, j) or getCShapeObstacle(obs_map.shape[0] - i,
                                                                           j) or getSlantedRectObstacle(
            obs_map.shape[0] - i, j) or getEllipseObstacle(obs_map.shape[0] - i, j) or getPolygonObstacle(
            obs_map.shape[0] - i, j) or getPolygonObstacle2(
            obs_map.shape[0] - i, j) or getPolygonObstacle3(
            obs_map.shape[0] - i, j):
            obs_map[i, j] = 1



