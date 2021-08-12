import queue
import time
import threading
from kivy.clock import Clock
from kivy.clock import ClockBaseBehavior

event = threading.Event()

def my_callback(dt):
    pass

class BFSMain():
    grid_size = 20

    colormap = {
        "Start": [.8, 0.05, .9, .9],
        "End": [.7, 0.05, .6, .9],
        '.': [.1, .75, .5, 1],
        '#': [1, .45, .45, 1],
        'path_color': [0, 1, 0, 1],
        'queue_color': [1, .7, 0],
        'visited_color': [.5, .5, .5, 1]
    }

    path_color = [0, 1, 0, 1]
    queue_color = [1, .7, 0]
    visited_color = [.5, .5, .5, 1]

    start = []
    end = []

    start_available = True
    end_available = True
    mapadj = []
    adj = []

    move_vector = [[-1, -1], [-1, 0], [-1, +1], [0, -1], [0, +1], [+1, -1], [+1, 0], [+1, +1]]
    move_vector = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    queue1 = queue.Queue()

    distance = []
    visited = []
    last = []
    path_interval = None
    print_path_interval = None
    print_curr = None
    resetb =None
    startb =None

    def __init__(self):
        self.speed_input = 500
        self.animation_speed = 0.025

    def set_speed_input(self, value):

        self.animation_speed = value


    def BFS(self, start, end, adj, mapadj, grid_size, color_map, move_vector, resetb, startb):


        self.resetb = resetb
        self.startb = startb

        self.grid_size = grid_size

        self.color_map = color_map


        self.start = start
        self.end = end

        self.mapadj = mapadj
        self.adj = adj


        for index,  i in enumerate(mapadj):
            r = int(index/grid_size)
            c = index%grid_size
            if adj[r][c] == '.':
                i.background_color = color_map[i.text]


        # move_vector = [[-1, -1], [-1, 0], [-1, +1], [0, -1], [0, +1], [+1, -1], [+1, 0], [+1, +1]]

        self.move_vector = move_vector

        self.found = False

        self.queue1 = queue.Queue()
        self.queue1.put(start)

        self.visited = []

        self.last = []
        for i in range(grid_size):
            temp = []
            for j in range(grid_size):
                temp.append([-1, -1])
            self.last.append(temp)

        self.distance = []
        for i in range(grid_size):
            temp = []
            for j in range(grid_size):
                temp.append(10000)
            self.distance.append(temp)

        self.distance[start[0]][start[1]] = 0

        self.path_interval = Clock.schedule_interval(self.bfs_next, self.animation_speed)





    def bfs_next(self, *args):
        if self.queue1.empty() or self.found:
            terminate =True
        i, j = self.queue1.get()
        self.visited.append([i, j])

        if [i, j] != self.start:
            self.mapadj[i * self.grid_size + j].background_color = self.color_map['visited_color']

        for it, jt in self.move_vector:
            if (i + it <= self.grid_size - 1 and i + it >= 0) and (j + jt <= self.grid_size - 1 and j + jt >= 0) and \
                    self.adj[i + it][j + jt] != '#':
                if self.adj[i + it][j + jt] == '.':
                    if [i + it, j + jt] in self.visited:
                        pass
                    else:
                        self.queue1.put([i + it, j + jt])
                        self.mapadj[(i + it) * self.grid_size + j + jt].background_color = self.color_map['queue_color']
                        self.visited.append([i + it, j + jt])
                        if self.distance[i + it][j + jt] > 1 + self.distance[i][j]:
                            self.distance[i + it][j + jt] = 1 + self.distance[i][j]
                            self.last[i + it][j + jt] = [i, j]

                elif self.adj[i + it][j + jt] == 'E':
                    if self.distance[i + it][j + jt] > 1 + self.distance[i][j]:
                        self.distance[i + it][j + jt] = 1 + self.distance[i][j]
                        self.last[i + it][j + jt] = [i, j]
                    self.found = True

        if self.queue1.empty() or self.found:
            self.path_interval.cancel()
            if len(self.end)!=0:
                self.print_curr = self.last[self.end[0]][self.end[1]]
            #self.print_currcurr = self.last[self.end[0]][self.end[1]]
            self.print_path_interval = Clock.schedule_interval(self.print_path, 0.5*self.animation_speed)


        # print(visited)
    def print_path(self, *args):
        if self.found:
            if self.print_curr != self.start:
                i, j = self.print_curr
                self.mapadj[self.grid_size * i + j].background_color = self.color_map['path_color']
                self.print_curr = self.last[i][j]
            else:
                self.print_path_interval.cancel()
                self.resetb.disabled = False
                self.startb.disabled = False

        else:
            for i in self.mapadj:
                if i.text != 'Start' and i.text != 'End' and i.text != '#':
                    i.background_color = [.9, 0, .2, 1]

            self.print_path_interval.cancel()
            self.resetb.disabled = False
            self.startb.disabled = False
