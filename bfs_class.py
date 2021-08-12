import queue



def my_callback(dt):
    pass

class BFSMain():


    def BFS(self, start, end, adj, mapadj, grid_size, color_map, move_vector, resetb, startb):

        for index,  i in enumerate(mapadj):
            r = int(index/grid_size)
            c = index%grid_size
            if adj[r][c] == '.':
                i.background_color = color_map[i.text]


        # move_vector = [[-1, -1], [-1, 0], [-1, +1], [0, -1], [0, +1], [+1, -1], [+1, 0], [+1, +1]]

        move_vector = move_vector

        found = False

        queue1 = queue.Queue()
        queue1.put(start)

        visited = []

        last = []
        for i in range(grid_size):
            temp = []
            for j in range(grid_size):
                temp.append([-1, -1])
            last.append(temp)

        distance = []
        for i in range(grid_size):
            temp = []
            for j in range(grid_size):
                temp.append(10000)
            distance.append(temp)

        distance[start[0]][start[1]] = 0

        while not queue1.empty() and not found:
            i, j = queue1.get()
            visited.append([i, j])

            if [i, j] != start:
                mapadj[i * grid_size + j].background_color = color_map['visited_color']

            for it, jt in move_vector:
                if (i + it <= grid_size - 1 and i + it >= 0) and (j + jt <= grid_size - 1 and j + jt >= 0) and \
                        adj[i + it][j + jt] != '#':
                    if adj[i + it][j + jt] == '.':
                        if [i + it, j + jt] in visited:
                            pass
                        else:
                            queue1.put([i + it, j + jt])
                            mapadj[(i + it) * grid_size + j + jt].background_color = color_map['queue_color']
                            visited.append([i + it, j + jt])
                            if distance[i + it][j + jt] > 1 + distance[i][j]:
                                distance[i + it][j + jt] = 1 + distance[i][j]
                                last[i + it][j + jt] = [i, j]

                    elif adj[i + it][j + jt] == 'E':
                        if distance[i + it][j + jt] > 1 + distance[i][j]:
                            distance[i + it][j + jt] = 1 + distance[i][j]
                            last[i + it][j + jt] = [i, j]
                        found = True
            if queue1.empty():
                break

        # print(visited)
        if found:
            curr = last[end[0]][end[1]]
            while curr != start:
                i, j = curr
                mapadj[grid_size * i + j].background_color = color_map['path_color']
                curr = last[i][j]
        else:
            for i in mapadj:
                if i.text != 'Start' and i.text != 'End' and i.text != '#':
                    i.background_color = [.9, 0, .2, 1]

        resetb.disabled = False
        startb.disabled = False