from cgitb import grey
import tkinter as tk
from tkinter import ttk

class Window(tk.Tk):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.tm_canvas = tk.Canvas(self, background="grey", width=300, height=300)
    self.tm_canvas.grid(row=0, column=1)
    self.sidebar = tk.Frame(self, width=100, height=300, background="red")
    self.sidebar.grid(row=0, column=0)
  
  def run(self):
    self.mainloop()

if __name__ == "__main__":
  editor = Window()
  editor.run()