import queue

adj = []

def BFS(self, b):
    # move_vector = [[-1, -1], [-1, 0], [-1, +1], [0, -1], [0, +1], [+1, -1], [+1, 0], [+1, +1]]

    move_vector = [[0, -1], [0, 1], [-1, 0], [1, 0]]

    found = False

    queue1 = queue.Queue()
    queue1.put(self.start)

    visited = []

    last = []
    for i in range(self.grid_size):
        temp = []
        for j in range(self.grid_size):
            temp.append([-1, -1])
        last.append(temp)

    distance = []
    for i in range(self.grid_size):
        temp = []
        for j in range(self.grid_size):
            temp.append(10000)
        distance.append(temp)

    distance[self.start[0]][self.start[1]] = 0

    while not queue1.empty() and not found:
        i, j = queue1.get()
        visited.append([i, j])

        if [i, j] != self.start:
            self.mapadj[i * self.grid_size + j].background_color = self.visited_color

        for it, jt in move_vector:
            if (i + it <= self.grid_size - 1 and i + it >= 0) and (j + jt <= self.grid_size - 1 and j + jt >= 0) and \
                    adj[i + it][j + jt] != '#':
                if adj[i + it][j + jt] == '.':
                    if [i + it, j + jt] in visited:
                        pass
                    else:
                        queue1.put([i + it, j + jt])
                        self.mapadj[(i + it) * self.grid_size + j + jt].background_color = self.queue_color
                        visited.append([i + it, j + jt])
                        if distance[i + it][j + jt] > 1 + distance[i][j]:
                            distance[i + it][j + jt] = 1 + distance[i][j]
                            last[i + it][j + jt] = [i, j]

                elif adj[i + it][j + jt] == 'E':
                    if distance[i + it][j + jt] > 1 + distance[i][j]:
                        distance[i + it][j + jt] = 1 + distance[i][j]
                        last[i + it][j + jt] = [i, j]
                    found = True
        # time.sleep(1)
        if queue1.empty():
            break

    # print(visited)
    if found:
        curr = last[self.end[0]][self.end[1]]
        while curr != self.start:
            i, j = curr
            self.mapadj[self.grid_size * i + j].background_color = self.path_color
            curr = last[i][j]
    else:
        for i in self.mapadj:
            if i.text != 'Start' and i.text != 'End' and i.text != '#':
                i.background_color = [.9, 0, .2, 1]