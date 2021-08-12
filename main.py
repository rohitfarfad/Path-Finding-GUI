from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color
from kivy.graphics import Rectangle
import queue
import time


# start_selected = False
# end_selected = False
# states = ['', '#', 'Start', 'End']

adj = []


class StackMap(StackLayout):
    from bfs_class_draft import BFSMain as BFSanim
    from bfs_class import BFSMain as BFSnorm

    bfs_anim = BFSanim()
    bfs_norm = BFSnorm()

    selected_bfs = bfs_anim

    grid_size = 30

    colormap = {
        "Start": [.8, 0.05, .9, 1],
        "End": [.7, 0.05, .6, 1],
        '.': [.1, .75, .5, 1],
        '#': [.75, .4, .4, 1],
        'path_color': [0, 1, 0, 1],
        'queue_color': [.9, .8, 0, 1],
        'visited_color': [.5, .5, .5, 1]
    }

    path_color = [0, 1, 0, 1]
    queue_color = [1, .7, 0]
    visited_color = [.5, .5, .5, 1]

    start = []
    end = []

    move_vector_dig = [[-1, -1], [-1, 0], [-1, +1], [0, -1], [0, +1], [+1, -1], [+1, 0], [+1, +1]]
    move_vector_norm = [[0, -1], [0, 1], [-1, 0], [1, 0]]

    move_vector = move_vector_norm

    start_available = True
    end_available = True
    mapadj = []
    States = ['.', '#', 'Start', 'End']
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(self.grid_size):
            tempadj = []
            for i in range(self.grid_size):
                b = Button(text='.', size_hint=(1/self.grid_size, 1/(self.grid_size+2)), background_normal='')
                b.bind(on_press=self.button_press)
                b.background_color = [.1, .75, .5, 1]
                self.mapadj.append(b)
                tempadj.append('.')
                self.add_widget(b)
            adj.append(tempadj)

        #self.selected_bfs.adj = adj
        self.reset_button = Button(text = 'Reset Grid', size_hint = (.25, 2/(self.grid_size+2)))
        self.reset_button.bind(on_press = self.reset_grid)
        self.add_widget(self.reset_button)

        self.startbutton = Button(text='Find Path', size_hint = (.25, 2/(self.grid_size+2)))
        self.startbutton.bind(on_press = self.call_BFS)
        self.add_widget(self.startbutton)




    def button_press(self, button):
        rc = self.mapadj.index(button)
        r = int(rc/self.grid_size)
        c = rc%self.grid_size

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
                adj[r][c] = '.'

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
        #self.selected_bfs.adj = adj
        #self.bfs.start = self.start
        #self.bfs.end = self.end


        print('\n\n')
        for i in adj:
            print(' '.join(i))


    def call_BFS(self, button):
        if len(self.start)==0:
            pass
        else:
            self.selected_bfs.BFS(self.start, self.end, adj, self.mapadj, self.grid_size, self.colormap, self.move_vector, self.reset_button, self.startbutton)

            if self.selected_bfs == self.bfs_anim:
                self.reset_button.disabled = True
                self.startbutton.disabled = True

    def reset_grid(self, button):
        self.start = []
        self.end = []
        self.start_available = True
        self.end_available = True
        for index,  i in enumerate(self.mapadj):
            r = int(index/self.grid_size)
            c = index%self.grid_size
            adj[r][c] = '.'
            i.text = '.'
            i.background_color = self.colormap[i.text]

        print('\n\n')
        for i in adj:
            print(' '.join(i))

    def animation_state(self, toggleb):
        if toggleb.state == "normal":
            self.selected_bfs = self.bfs_norm
            toggleb.text = 'Animation: OFF'
        else:
            self.selected_bfs = self.bfs_anim
            toggleb.text = 'Animation: ON'

    def diagonal_movement_state(self, toggleb):
        if toggleb.state == "normal":
            self.move_vector = self.move_vector_norm
            toggleb.text = 'Diagonal Movement: OFF'
        else:
            self.move_vector = self.move_vector_dig
            toggleb.text = 'Diagonal Movement: ON'

    def on_slider_value(self, slider):
        # print("Slider Value: ", slider.value)
        # self.bfs_anim.set_speed_input(1/float(slider.value))
        pass


class GridLayoutMap(GridLayout):
    def __int__(self, **kwargs):
        super().__init__(**kwargs)



class StackLayout1(StackLayout):
    pass

class TheMapApp(App):
    pass


TheMapApp().run()