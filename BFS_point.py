import numpy as np

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