from cgitb import grey
import tkinter as tk
from tkinter import ttk

class EditorCanvas(tk.Canvas):
  def __init__(self, parent, **kwargs):
    super().__init__(**kwargs)
    # Some other state goes in here. Not sure what yet

  # Also some event handlers and such. Maybe abstract them to different classes if they get too unwieldy?  

class EditorWindow(tk.Tk):
  def __init__(self, width=900, height=500, **kwargs):
    super().__init__(**kwargs)

    # Initialise direct children (or more?)
    self.editor_canvas = EditorCanvas(self, background="grey")
    self.editor_canvas.grid(row=0, column=1, sticky="nsew")
    self.options_frame = tk.Frame(self, background="red")
    self.options_frame.grid(row=0, column=0, sticky="nsew")

    # Resizing config
    self.columnconfigure(0, weight=0, minsize=250)
    self.columnconfigure(1, weight=1)
    self.rowconfigure(0, weight=1)

    # Set width and height
    self.geometry(f"{width}x{height}")

  '''Running of the application'''
  def run(self):
    self.mainloop()

if __name__ == "__main__":
  editor = EditorWindow()
  editor.run()