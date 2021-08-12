from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color
from kivy.graphics import Rectangle
import queue


# start_selected = False
# end_selected = False
# states = ['', '#', 'Start', 'End']

adj = []


class StackMap(StackLayout):

    colormap = {
        "Start": [.8, 0.05, .9, .9],
        "End": [.7, 0.05, .6, .9],
        '.': [.1, .75, .5, 1],
        '#': [1, .45, .45, 1]
    }

    path_color = [0, 1, 0, 1]
    queue_color = [0, 1, 1]
    visited_color = [.5, .5, .5, 1]

    start = []
    end = []

    start_available = True
    end_available = True
    mapadj = []
    States = ['.', '#', 'Start', 'End']
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(10):
            tempadj = []
            for i in range(10):
                b = Button(text='.', size_hint=(.1, .1))
                b.bind(on_press=self.button_press)
                b.background_color = [.1, .75, .5, 1]
                self.mapadj.append(b)
                tempadj.append('.')
                self.add_widget(b)
            adj.append(tempadj)

            #self.blist.append(b)
        #Button(text="Button", size_hint=(None, None), size=(dp(100), dp(100)))

        startbutton = Button(text='Find Path')
        startbutton.bind(on_press = self.DFS)
        self.add_widget(startbutton)

    def button_press(self, button):
        rc = self.mapadj.index(button)
        r = int(rc/10)
        c = rc%10

        if button.text == '.':
            button.text = '#'

        elif button.text == '#':
            if self.start_available:
                button.text = 'Start'
                self.start = [r, c]
                self.start_available = False

            elif self.end_available:
                button.text = 'End'
                self.end = [r, c]
                self.end_available = False


            else:
                button.text = '.'

        elif button.text == 'Start':
            if self.end_available:
                button.text = 'End'
                self.end = [r, c]
                self.end_available = False
                self.start = []
                self.start_available = True

            else:
                button.text = '.'
                self.start = []
                self.start_available = True

        elif button.text == 'End':
            button.text = '.'
            self.end = []
            self.end_available = True


        if button.text == 'Start':
            adj[r][c] = 'S'
        elif button.text == 'End':
            adj[r][c] = 'E'
        else:
            adj[r][c] = button.text

        button.background_color = self.colormap[button.text]

        print('\n\n')
        for i in adj:
            print(' '.join(i))


    def DFS(self, start_button):

        #move_vector = [[-1, -1], [-1, 0], [-1, +1], [0, -1], [0, +1], [+1, -1], [+1, 0], [+1, +1]]

        move_vector = [[0, -1], [0, 1], [-1, 0], [1, 0]]

        found = False

        queue1 = queue.Queue()
        queue1.put(self.start)

        visited = []

        last = []
        for i in range(10):
            temp = []
            for j in range(10):
                temp.append([-1, -1])
            last.append(temp)

        distance = []
        for i in range(10):
            temp = []
            for j in range(10):
                temp.append(10000)
            distance.append(temp)

        distance[self.start[0]][self.start[1]] = 0

        while not queue1.empty() and not found:
            i, j = queue1.get()
            visited.append([i, j])

            if [i, j] != self.start:
                self.mapadj[i*10 + j].background_color = self.visited_color

            for it, jt in move_vector:
                if (i + it <= 9 and i + it >= 0) and (j + jt <= 9 and j + jt >= 0) and adj[i + it][j + jt] != '#':
                    if adj[i + it][j + jt] == '.':
                        if [i + it, j + jt] in visited:
                            pass
                        else:
                            queue1.put([i + it, j + jt])
                            self.mapadj[(i+it)*10+j+jt].background_color = self.queue_color
                            visited.append([i+it, j+jt])
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

        print(visited)
        if found:
            curr = last[self.end[0]][self.end[1]]
            while curr != self.start:
                i, j = curr
                self.mapadj[10 * i + j].background_color = self.path_color
                curr = last[i][j]
        else:
            for i in self.mapadj:
                if i.text !='Start' and i.text != 'End' and i.text != '#':
                    i.background_color = [.9, 0, .2, 1]





class GridLayoutMap(GridLayout):
    def __int__(self, **kwargs):
        super().__init__(**kwargs)




class StackLayout1(StackLayout):
    pass

class TheMapApp(App):
    pass


TheMapApp().run()