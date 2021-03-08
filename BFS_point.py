import numpy as np
import cv2

# Map creation with edges as '1' in order to provide a void border of the map

obs_map = np.zeros((302, 402), dtype=int)
obs_map[0, :] = 1
obs_map[301, :] = 1
obs_map[:, 0] = 1
obs_map[:, 401] = 1


class Queue:

# Creating a class to convert a list into a queue

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

# Creating a class to determine the node of the iteration. Node is the puzzle state.

class Node:

# Defining the __init__ function

    def __init__(self, data, parent, act, cost):
        self.data = data
        self.parent = parent
        self.act = act
        self.id = self.get_id()
        self.cost = cost

# Defining a function to generate a unique id of the state of the puzzle.

    def get_id(self):
        _id = np.ravel(self.data).tolist()
        _id = [str(item) for item in _id]
        _id = "-".join(_id)
        self.id = _id
        return self.id

# Defining the __repr__ function

    def __repr__(self):
        return str(self.data)

# Creating a function to define the circle obstacle's area on the map

def getCircleObstacle(i, j):
    cond = ((j - 90) ** 2) + ((i - 70) ** 2) <= 1225
    return cond

# Creating a function to define the C shape obstacle's area on the map

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

# Creating a function to define the slanted rectangle obstacle's area on the map

def getSlantedRectObstacle(i, j):
    cond1 = (i) + (1.42814 * j) >= 176.5511
    cond2 = (i) - (0.7 * j) >= 74.39
    cond3 = (i) + (1.42814 * j) <= 428.06815
    cond4 = (i) - (0.7 * j) <= 98.80545
    ret_val = (cond1 and cond2 and cond3 and cond4)
    return ret_val

# Creating a function to define the ellipseobstacle's area on the map

def getEllipseObstacle(i, j):
    cond = (((j - 246) / 60) ** 2) + (((i - 145) / 30) ** 2) <= 1
    return cond

# Creating a function to define the polygon obstacle's area on the map
# The Polygon is divided into a rectangle and two triangles

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

# Creating an if-condition to change value of the element in area under all obstacles to '1' in order to create a void in the map

for i in range(obs_map.shape[0]):
    for j in range(obs_map.shape[1]):
        if getCircleObstacle(obs_map.shape[0] - i, j) or getCShapeObstacle(obs_map.shape[0] - i,
                                                                           j) or getSlantedRectObstacle(
            obs_map.shape[0] - i, j) or getEllipseObstacle(obs_map.shape[0] - i, j) or getPolygonObstacle(
            obs_map.shape[0] - i, j) or getPolygonObstacle2(
            obs_map.shape[0] - i, j) or getPolygonObstacle3(
            obs_map.shape[0] - i, j):
            obs_map[i, j] = 1

# Defining the move up function where if the element above does not have '1' value, i.e. if there isn't a void in the element above, the object moves up

def move_up(i, j):
    if obs_map[i - 1, j] != 1:
        return (i - 1, j)

# Defining the move down function where if the element below does not have '1' value, i.e. if there isn't a void in the element below, the object moves down

def move_down(i, j):
    if obs_map[i + 1, j] != 1:
        return (i + 1, j)

# Defining the move left function where if the element on the left does not have '1' value, i.e. if there isn't a void in the element on the left, the object moves left

def move_left(i, j):
    if obs_map[i, j - 1] != 1:
        return (i, j - 1)

# Defining the move right function where if the element on the right does not have '1' value, i.e. if there isn't a void in the element on the right, the object moves right

def move_right(i, j):
    if obs_map[i, j + 1] != 1:
        return (i, j + 1)

# Defining the move up left function where if the element above and left does not have '1' value, i.e. if there isn't a void in the element above and left , the object moves up left

def move_up_left(i, j):
    if obs_map[i - 1, j - 1] != 1:
        return (i - 1, j - 1)

# Defining the move up right function where if the element above and right does not have '1' value, i.e. if there isn't a void in the element above and right, the object moves up right

def move_up_right(i, j):
    if obs_map[i - 1, j + 1] != 1:
        return (i - 1, j + 1)

# Defining the move down left function where if the element below and left does not have '1' value, i.e. if there isn't a void in the element below and left, the object moves down left

def move_down_left(i, j):
    if obs_map[i + 1, j - 1] != 1:
        return (i + 1, j - 1)

# Defining the move down right function where if the element below and right does not have '1' value, i.e. if there isn't a void in the element below and right, the object moves down right

def move_down_right(i, j):
    if obs_map[i + 1, j + 1] != 1:
        return (i + 1, j + 1)

# Defining a function to generate new legal moves as per the state

def generate_new_moves(state):
    list_states = []
    for func in [move_left, move_right, move_down, move_up, move_up_left, move_up_right, move_down_left,
                 move_down_right]:
        dum_state = state
        out_state = func(dum_state[0], dum_state[1])
        if out_state is not None:
            list_states.append(out_state)
    return list_states

# Inputting values from the user and checking if the values are valid by checking the outbound values and in-obstacle values

try:
    start_node_x = int(input('Enter start node x postion: '))
    if start_node_x < 0:
        print("Invalid start node x position, setting x postion to 0")
        start_node_x = 0
    elif start_node_x > 402:
        print("Invalid start node x position, setting x postion to 403")
        start_node_x = 402

    start_node_y = int(input('Enter start node y postion: '))
    if start_node_y < 0:
        print("Invalid start node y position, setting y postion to 0")
        start_node_y = 0
    elif start_node_y > 302:
        print("Invalid start node y position, setting y postion to 300")
        start_node_y = 302

    goal_node_x = int(input('Enter goal node x postion: '))
    if goal_node_x < 0:
        print("Invalid goal node x position, setting x postion to 0")
        goal_node_x = 0
    elif goal_node_x > 402:
        print("Invalid goal node x position, setting x postion to 403")
        start_node_x = 402

    goal_node_y = int(input('Enter goal node y postion: '))
    if goal_node_y < 0:
        print("Invalid goal node y position, setting y postion to 0")
        goal_node_y = 0
    elif goal_node_y > 302:
        print("Invalid goal node y position, setting y postion to 300")
        start_node_y = 302

    if obs_map[obs_map.shape[0] - start_node_y, start_node_x] == 1:
        print("Error: Start position is in void space. Exiting program")
        exit(1)

    if obs_map[obs_map.shape[0] - goal_node_y, goal_node_x] == 1:
        print("Error: Goal position is in void space. Exiting program")
        exit(1)
except:
    print("Error: Invalid Input. Exiting program")
    exit(2)

# Creating the goal state and initial state.

goal_state = (obs_map.shape[0] - goal_node_y, goal_node_x)
init_state = (obs_map.shape[0] - start_node_y, start_node_x)
state_queue = Queue()
state_queue.add(Node(init_state, None, None, None))

visited = []

# Creating a new array in order to write as video

result_map = obs_map.copy()
result_map = result_map * 255
result_map = np.dstack((result_map, result_map, result_map))
result_map = result_map.astype(np.uint8)
height, width = obs_map.shape
FPS_val = 240

video_save = cv2.VideoWriter("Path-detection.mp4", cv2.VideoWriter_fourcc(*'mp4v'), FPS_val, (width, height))

# While loop to iterate the values inside the array with legal moves.
# If the current state is same as the goal state then the loop breaks.
# If the state ID is found in the visited list, then the node is skipped

while True:
    try:
        cur_node = state_queue.pop()
    except:
        if len([node for node in state_queue.queue]) == 0:
            break
    if np.all(cur_node.data == goal_state):
        break
    if cur_node.id in visited:
        continue
    moves = generate_new_moves(cur_node.data)
    for move in moves:
        new_node = Node(move, cur_node, None, None)
        state_queue.add(new_node)
    visited.append(cur_node.id)

    result_map[cur_node.data[0], cur_node.data[1], :] = np.asarray((255, 0, 0))

    result_map[result_map.shape[0] - start_node_y, start_node_x, :] = np.asarray((0, 0, 255))
    result_map[result_map.shape[0] - goal_node_y, goal_node_x, :] = np.asarray((0, 255, 0))

    video_save.write(result_map)

target_node = cur_node
path = []

# While loop to add a step in the path

while cur_node is not None:
    path.append(cur_node)
    cur_node = cur_node.parent

# Traceback the path

path.reverse()

# Converting the data in path array to BGR values

for item in path:
    result_map[item.data[0], item.data[1], :] = np.asarray((0, 255, 255))
    result_map[result_map.shape[0] - start_node_y, start_node_x, :] = np.asarray((0, 0, 255))
    result_map[result_map.shape[0] - goal_node_y, goal_node_x, :] = np.asarray((0, 255, 0))

    for _ in range(int(FPS_val / 20)):
        video_save.write(result_map)

# Writing and saving the complete traverse

video_save.write(result_map)

video_save and video_save.release()
cv2.imshow("Path", result_map)
if cv2.waitKey(0) and 0XFF == ord('q'):
    exit(0)

cv2.destroyAllWindows()