from cgitb import grey
import tkinter as tk
from tkinter import ttk

class EditorCanvas(tk.Canvas):
  def __init__(self, parent, **kwargs):
    super().__init__(**kwargs)
    # Some other state goes in here. Not sure what yet

  # Also some event handlers and such. Maybe abstract them to different classes if they get too unwieldy?  

class EditorWindow():
  def __init__(self, **kwargs):
    self.window_width = 600
    self.window_height = 500
    self.root = tk.Tk()
    self.editor_canvas = EditorCanvas(self.root, width=self.window_width // 3 * 2, height=self.window_height, background="grey")
    self.editor_canvas.grid(row=0, column=1)
    self.options_frame = tk.Frame(self.root, width=self.window_width // 3, height=self.window_height, background="red")
    self.options_frame.grid(row=0, column=0)
    self.root.bind("<Configure>", self.resize)

  '''Running of the application'''
  def run(self):
    self.root.mainloop()

  '''Event on window resize'''
  def resize(self, event):
    if event.widget == self.root and (event.width != self.window_width or event.height != self.window_height):
      self.window_width, self.window_height = event.width, event.height

if __name__ == "__main__":
  editor = EditorWindow()
  editor.run()