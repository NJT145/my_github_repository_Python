import Tkinter as tk
import threading
import time

class BlockInterface(object):
    def __init__(self, master,G):
        master.title("BlockWorld")
        canv_frame=tk.Frame(master)
        canv_frame.pack()
        self.canvas= tk.Canvas(canv_frame, width=10, height=60, bg="gray")
        self.canvas.pack(padx=10, pady=10)
        self.trace = G
        self.create_grid(G[0])
        self.activate(G[0])

    def create_rect(self,coord, val):
        if val==0:
            fill="white"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)
        elif val == 1:
            fill ="blue"
            self.canvas.create_rectangle(coord, fill=fill, outline="black")
        elif val == 2:
            fill = "green"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)
        elif val == 4:
            fill = "red"
            self.canvas.create_rectangle(coord, fill=fill, outline=fill)

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

    def create_grid(self, matrix):
        yc_og= (0,60)
        yc=(0,60)
        self.canvas.configure(height=60*len(matrix))
        for vector in matrix:
            self.create_row(vector, yc)
            yc=(yc[1],yc[1]+yc_og[1])

    def update_grid(self, G):
        self.canvas.update()
        self.create_grid(G)

    def activate(self, G):
        thread=threading.Thread(target=lambda: self.solve_puzzle(G))
        thread.daemon=True # End thread when program is closed
        thread.start()

    def solve_puzzle(self, G):
        i=0
        while True:
            try:
                time.sleep(1)
                G= self.trace[i]
                self.update_grid(G)
                i+=1
            except IndexError:
                break


def start_simulation(G):
    root=tk.Tk()
    root.resizable(0,0)
    BlockInterface(root,G)
    root.mainloop()

# this is an example sequence to check that the simulation works
example_sequence= [[[1,2,1,1],[1,2,4,4],[2,2,4,4],[1,1,0,0]],
                   [[1,2,1,1],[1,2,0,0],[2,2,4,4],[1,1,4,4]],
                   [[1,2,1,0],[1,2,0,1],[2,2,4,4],[1,1,4,4]],
                   [[1,2,0,1],[1,2,0,1],[2,2,4,4],[1,1,4,4]],
                   [[1,0,2,1],[1,0,2,1],[2,2,4,4],[1,1,4,4]]]

# call the start simulation function with your sequence of moves (returned by UCS or A*)
# as long as your moves are valid, it will work as expected

if __name__ == "__main__":
    start_simulation(example_sequence)
