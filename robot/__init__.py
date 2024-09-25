class MessageStorage:

    def __init__(self):
        self.message_storage = {}

    def receive(self, msg_num):
        return self.message_storage.get(msg_num)

    def send(self, message, msg_num):
        self.message_storage[msg_num] = message


def refresh(_grid):
    if _grid.all_num:
        for p in _grid.all_num:
            _grid.add()[p[0]][p[1]] = str(p[2])

    if _grid.inputs:
        for p in _grid.inputs:
            if not len(p) >= 4:
                _grid.add()[p[0]][p[1]] = 'i'
            else:
                _grid.add()[p[0]][p[1]] = str(p[3])


class Grid:
    def __init__(self, height, width):
        self.grid = [['.' for _ in range(0, width)] for _ in range(0, height)]
        self.grid_robot = []
        self.all_num = []
        self.inputs = []
        self.walls = []
        self.height = height
        self.width = width

    def output(self):
        for i in range(0, len(self.grid)):
            print(' '.join(self.grid[i]))

    def add(self):
        return self.grid

    def end(self):
        if self.grid_robot:
            for slf in range(0, len(self.grid_robot)):
                if not isinstance(self.grid_robot[slf], tuple):
                    self.grid[self.grid_robot[slf].pos[0]][self.grid_robot[slf].pos[1]] = 'f' + str(slf) if not slf == 0 else 'f'
                else:
                    self.grid[self.grid_robot[slf][0].pos[0]][self.grid_robot[slf][0].pos[1]] = str(self.grid_robot[slf][1][1]) + str(self.grid_robot[slf][0].robot_num) if not slf == 0 else str(self.grid_robot[slf][1][1])

        else:
            pass
        self.output()

    def creat_wall(self, y, x):
        self.grid[y][x] = '#'
        self.walls.append([y, x])

    def del_wall(self, y, x):
        if [y, x] in self.walls:
            self.walls.remove([y, x])
            self.grid[y][x] = '.'
        else:
            return None

    def creat_input(self, y, x, answer):
        self.grid[y][x] = 'i'
        self.inputs.append([y, x, answer])

    def creat_nummber(self, y, x, num):
        self.grid[y][x] = str(num)
        self.all_num.append([y, x, num])


class Robot:  # Class Robot
    # directions = {0: 'north', 2: 'south', 1: 'east', 3: 'west'}  # The directions

    def __init__(self, y, x, direction=1):
        self.grid = None
        self.grid_class = None
        self.pos = [y, x, direction]  # y, x, direction
        self.y_size = 10  # the size in the width
        self.x_size = 10  # the size in the lenght
        self.way = []  # The way of this robot/self
        self.memorys = None
        self.player = None
        self.robot_num = None

    # the funktions that don't move the player directly or test something (example: is_wall(...); test whether there is a wall in front of the robot/self)
    def remember(self, label, show=False):  # safe somthing/ an input
        if not (label is None):
            self.memorys = label
        if show:
            print(self.memorys)
        return self.memorys

    def setgrid(self, grid_, robot=None, player_img=(None, None), player_num=False):

        if robot is None:
            if not ((player_img[0] is None) and (player_img[1] is None)):
                robot = self, [player_img[0], player_img[1]]
            else:
                robot = self
        grid_.grid_robot.append(robot)

        if player_num is True:
            self.player = 'x' + str(len(grid_.grid_robot)) if not len(grid_.grid_robot) <= 1 else 'X'
            self.robot_num = str(len(grid_.grid_robot)) if not len(grid_.grid_robot) <= 1 else ''
        else:
            self.player = 'x'
            self.robot_num = ''

        self.grid = grid_.add()
        self.grid_class = grid_
        if not ((player_img[0] is None) and (player_img[1] is None)):
            self.grid[self.pos[0]][self.pos[1]] = str(robot[1][0]) + self.robot_num
        else:
            self.grid[self.pos[0]][self.pos[1]] = str(self.player)

    def is_wall(self):  # test whether is a wall in front
        if self.pos[2] == 0:
            if [(self.pos[0] - 1) % self.y_size, self.pos[1]] in self.grid_class.walls:
                return True

        if self.pos[2] == 2:
            if [(self.pos[0] + 1) % self.y_size, self.pos[1]] in self.grid_class.walls:
                return True

        if self.pos[2] == 1:
            if [self.pos[0], (self.pos[1] + 1) % self.x_size] in self.grid_class.walls:
                return True

        if self.pos[2] == 3:
            if [self.pos[0], (self.pos[1] - 1) % self.x_size] in self.grid_class.walls:
                return True
        return False  #

    def answering(self):  # when the robot/self is on an input you/the robot/self can use this to return a True or a False if you/self/robot remember the key nummber
        for i in self.grid_class.inputs:
            if (i[0], i[1]) == (self.pos[0], self.pos[1]):
                if self.memorys == i[2]:
                    return True
        return False

    def roboter_lenght(self, lenght):  # limited the lenght of the way/robot
        if len(self.way) > lenght:
            while not len(self.way) == lenght:
                self.grid[self.way[0][0] % self.y_size][self.way[0][1] % self.x_size] = '.'
                del self.way[0]

    def type_in(self, input_):  # can type in something in an input
        for i in self.grid_class.inputs:
            if (i[0], i[1]) == (self.pos[0], self.pos[1]):
                self.grid[i[0]][i[1]] = str(input_)
                if len(i) >= 4:
                    i[3] = input_
                else:
                    i.append(input_)

    def read_num(self):  # the robot read the thing on the grid/under it
        for num in self.grid_class.all_num:
            if (num[0], num[1]) == (self.pos[0], self.pos[1]):
                return num[2]

    # movement
    def turn_east(self):  # turn east
        self.pos[2] = 1

    def turn_north(self):  # turn north
        self.pos[2] = 0

    def turn_south(self):  # turn south
        self.pos[2] = 2

    def turn_west(self):  # turn west
        self.pos[2] = 3

    def turn_right(self):  # turn right ;)
        self.pos[2] = (self.pos[2] + 1) % 4

    def turn_left(self):  # turn left
        self.pos[2] = (self.pos[2] - 1) % 4

    def setpos(self, y, x):  # set the pos of the robot on a (spezific) position
        self.grid[self.pos[0]][self.pos[1]] = '!'
        self.pos[0] = y
        self.pos[1] = x
        self.grid[y][x] = '!'
        refresh(self.grid_class)

    def move(self, move_, steps):  # move the way you writte

        def is_wall_():
            if self.pos[2] == 0:
                if [(self.pos[0] - 1) % self.y_size, self.pos[1]] in self.grid_class.walls:
                    return True

            if self.pos[2] == 2:
                if [(self.pos[0] + 1) % self.y_size, self.pos[1]] in self.grid_class.walls:
                    return True

            if self.pos[2] == 1:
                if [self.pos[0], (self.pos[1] + 1) % self.x_size] in self.grid_class.walls:
                    return True

            if self.pos[2] == 3:
                if [self.pos[0], (self.pos[1] - 1) % self.x_size] in self.grid_class.walls:
                    return True
            return False

        def down_move_(steps_):
            for step in range(0, steps_):
                self.pos[2] = 2
                if not is_wall_():
                    self.pos[0] += 1
                    self.player = 'v'
                    self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                    self.pos[0] = self.pos[0] % self.y_size
                    self.pos[1] = self.pos[1] % self.x_size
                self.way.append([self.pos[0], self.pos[1], self.pos[2]])

        def up_move_(_steps):
            for step in range(0, _steps):
                self.pos[2] = 0
                if not is_wall_():
                    self.pos[0] -= 1
                    self.player = '^'
                    self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                    self.pos[0] = self.pos[0] % self.y_size
                    self.pos[1] = self.pos[1] % self.x_size
                self.way.append([self.pos[0], self.pos[1], self.pos[2]])

        def left_move_(steps__):
            for step in range(0, steps__):
                self.pos[2] = 3
                if not is_wall_():
                    self.pos[1] -= 1
                    self.player = '<'
                    self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                    self.pos[0] = self.pos[0] % self.y_size
                    self.pos[1] = self.pos[1] % self.x_size
                self.way.append([self.pos[0], self.pos[1], self.pos[2]])

        def right_move_(__steps):
            for step in range(0, __steps):
                self.pos[2] = 1
                if not is_wall_():
                    self.pos[1] += 1
                    self.player = '>'
                    self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                    self.pos[0] = self.pos[0] % self.y_size
                    self.pos[1] = self.pos[1] % self.x_size
                self.way.append([self.pos[0], self.pos[1], self.pos[2]])

        if move_ == 'up':
            m = up_move_
        elif move_ == 'down':
            m = down_move_
        elif move_ == 'right':
            m = right_move_
        elif move_ == 'left':
            m = left_move_
        else:
            return None
        m(steps)
        refresh(self.grid_class)

    def down_move(self, steps_):  # move the robot down
        for step in range(0, steps_):
            self.pos[2] = 2
            if not self.is_wall():
                self.pos[0] += 1
                self.player = 'v'
                self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                self.pos[0] = self.pos[0] % self.y_size
                self.pos[1] = self.pos[1] % self.x_size
            self.way.append([self.pos[0], self.pos[1], self.pos[2]])

    def up_move(self, _steps):  # move the robot up
        for step in range(0, _steps):
            self.pos[2] = 0
            if not self.is_wall():
                self.pos[0] -= 1
                self.player = '^'
                self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                self.pos[0] = self.pos[0] % self.y_size
                self.pos[1] = self.pos[1] % self.x_size
            self.way.append([self.pos[0], self.pos[1], self.pos[2]])

    def left_move(self, steps__):  # move the robot left
        for step in range(0, steps__):
            self.pos[2] = 3
            if not self.is_wall():
                self.pos[1] -= 1
                self.player = '<'
                self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                self.pos[0] = self.pos[0] % self.y_size
                self.pos[1] = self.pos[1] % self.x_size
            self.way.append([self.pos[0], self.pos[1], self.pos[2]])

    def right_move(self, __steps):  # move the robot right
        for step in range(0, __steps):
            self.pos[2] = 1
            if not self.is_wall():
                self.pos[1] += 1
                self.player = '>'
                self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                self.pos[0] = self.pos[0] % self.y_size
                self.pos[1] = self.pos[1] % self.x_size
            self.way.append([self.pos[0], self.pos[1], self.pos[2]])

    def square(self, length, width, direction=None):  # make a square
        if direction is None:
            direction = ['right', 'down']

        if not isinstance(length, int) or length <= 0:
            raise ValueError('Invalid length value provided')

        if not isinstance(width, int) or width <= 0:
            raise ValueError('Invalid width value provided')

        self.move(direction[0], width)
        self.move(direction[1], length)

        if direction[0] == 'right':
            self.move('left', width)
        else:
            self.move('right', width)

        if direction[1] == 'down':
            self.move('up', length)
        else:
            self.move('down', length)

    def forward(self, steps, refreshing=True):  # move the robot forward
        for step in range(0, steps):
            if not self.is_wall():
                if self.pos[2] == 0:
                    self.pos[0] -= 1
                    self.player = '^'

                if self.pos[2] == 2:
                    self.pos[0] += 1
                    self.player = 'v'

                if self.pos[2] == 1:
                    self.pos[1] += 1
                    self.player = '>'

                if self.pos[2] == 3:
                    self.pos[1] -= 1
                    self.player = '<'

                self.pos[0] = self.pos[0] % self.y_size
                self.pos[1] = self.pos[1] % self.x_size
                self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                if refreshing:
                    refresh(self.grid_class)
            self.way.append([self.pos[1], self.pos[0], self.pos[2]])

    def backward(self, steps, refreshing=True):  # move the robot backwards
        for step in range(0, steps):
            if not self.is_wall():
                if self.pos[2] == 0:
                    self.pos[0] += 1
                    self.player = 'v'

                if self.pos[2] == 2:
                    self.pos[0] -= 1
                    self.player = '^'

                if self.pos[2] == 1:
                    self.pos[1] -= 1
                    self.player = '>'

                if self.pos[2] == 3:
                    self.pos[1] += 1
                    self.player = '<'

                self.pos[0] = self.pos[0] % self.y_size
                self.pos[1] = self.pos[1] % self.x_size
                self.grid[self.pos[0] % self.y_size][self.pos[1] % self.x_size] = str(self.player)
                if refreshing:
                    refresh(self.grid)
            self.way.append([self.pos[0], self.pos[1], self.pos[2]])

    # something else
    def make_text(self, txt):  # make a text you type in
        txt = list(txt)
        for e in txt:
            self.forward(1)
            self.grid.creat_nummber(self.pos[0], self.pos[1], e)
        self.forward(1)
