import time
import Tkinter as tk
import random

class App(object):
    def __init__(self, master,G):
        master.title("Enter the Maze")
        # define our frames
        canv_frame=tk.Frame(master)
        canv_frame.pack()
        # define canvas
        self.canvas= tk.Canvas(canv_frame, width=10, height=60, bg="gray")
        self.canvas.pack(padx=10, pady=10)
        self.create_grid(G)
        # create the agent
        self.agent=self.canvas.create_oval([25,20,45,40],fill="darkgreen", outline="black")
        self.move_y(1,0)
        self.move_x(1,0)

    def create_grid(self, matrix):
        yc_og= (0,60)  # original or initial y coordinates
        yc=(0,60)
        self.canvas.configure(height=60*len(matrix))
        for vector in matrix:
            self.create_row(vector, yc)
            yc=(yc[1],yc[1]+yc_og[1])

    def create_row(self, vector, y_coord):
        y0, y1=y_coord
        w=70
        x0, x1=0, w
        self.canvas.configure(width=w*len(vector))
        for i in range(len(vector)):
            self.create_rect([x0,y0,x1,y1], vector[i])
            x0=x1
            x1+=w
        return

    def create_rect(self,coord, val):
        if val==0: fill="white"
        elif val==1: fill="lightblue"
        elif val==3: fill="green"
        else: fill="darkblue"
        self.canvas.create_rectangle(coord, fill=fill, outline="black")

    def movement(self, prev_state, next_state):
        # this moves an agent from previous to next state
        move_on_y=next_state[0]-prev_state[0]
        move_on_x=next_state[1]-prev_state[1]
        if move_on_y:
            self.move_y(-move_on_y,0.02)
        elif move_on_x:
            self.move_x(move_on_x,0.02)

    def move_x(self, dr, t):
        # movement along x direction
        try:
            for _ in range(35):
                time.sleep(t)
                self.canvas.move(self.agent,dr*2,0)
                self.canvas.update()
        except tk.TclError:
            pass

    def move_y(self, dr, t):
        # movement along y direction
        try:
            for _ in range(30):
                time.sleep(t)
                self.canvas.move(self.agent,0,dr*2)
                self.canvas.update()
        except tk.TclError:
            pass

    def move_on_path(self,path):
        while len(path) !=1:
            p=path.pop(0)
            n=path[0]
            self.movement(p,n)

####### Start here ###############
# example configuration
config = [[2, 2, 2, 2, 2, 2, 2, 2],
          [2, 0, 0, 0, 1, 0, 0, 2],
          [2, 0, 0, 1, 0, 0, 0, 2],
          [2, 0, 0, 0, 1, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 0, 2],
          [2, 0, 0, 0, 0, 0, 3, 2],
          [2, 2, 2, 2, 2, 2, 2, 2]]
# path taken in above configuration
path = [(6, 1), (5, 1), (5, 2), (4, 2), (4, 3), (3, 3), (3, 4), (2, 4), (2, 5), (2, 6), (1, 6)]

root = tk.Tk()
app=App(root, config)
app.move_on_path(path)
root.mainloop()

