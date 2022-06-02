import tkinter as tk
import tkinter.ttk as ttk

### TODO: Work out how to handle events driven from the buttons ###

class EditorCanvas(tk.Canvas):
  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
    tk.Label(self, text="Canvas for creating and editing TMs").pack()
    # Some other state goes in here. Not sure what yet

  # Also some event handlers and such. Maybe abstract them to different classes if they get too unwieldy?

class OptionsFrame(tk.Frame):
  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)

    # Weights
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    # Tape stuff
    self.tape_cells = []
    for i in range(10):
      tape = tk.Label(self, text="B")
      tape.grid(row=0, column=i)
      self.tape_cells.append(tape) 

    tk.Label(self, text="/\\", bg = "red").grid(row=1, column=5)

class EditorWindow(tk.Tk):
  def __init__(self, width=900, height=500, **kwargs):
    super().__init__(**kwargs)

    # Column/row weights and minimum sizes.
    # This is complicated since each button is in its own grid cell
    self.columnconfigure(0, minsize=20)
    self.columnconfigure(1, minsize=20)
    self.columnconfigure(2, minsize=20)
    self.columnconfigure(3, minsize=20)
    self.columnconfigure(4, weight=1)

    self.rowconfigure(3, weight=1)

    # Maybe temporary stuff. Could end up in its own frame maybe?
    self.tape_entry = tk.Entry(self)
    self.tape_entry.insert(0, "This is a tape")
    self.tape_entry.grid(row=0, column=0, columnspan=4, sticky="ew")
    self.tape_head = tk.Label(self, text="/\\")
    self.tape_head.grid(row=1, column=0, columnspan=4)

    # Initialise children (buttons and canvas are direct children since buttons affect canvas)
    self.play_button = tk.Button(self, text="Play")
    self.play_button.grid(row=2, column=0)
    self.step_button = tk.Button(self, text="Step")
    self.step_button.grid(row=2, column=1)
    self.reset_button = tk.Button(self, text="Reset")
    self.reset_button.grid(row=2, column=2)
    self.stop_button = tk.Button(self, text="Stop")
    self.stop_button.grid(row=2, column=3)

    self.editor_canvas = EditorCanvas(self, bg="grey")
    self.editor_canvas.grid(row=0, rowspan=4, column=4, sticky = "nsew")

    # Sizing the initial window
    self.geometry(f"{width}x{height}")

  '''Running of the application'''
  def run(self):
    self.mainloop()

if __name__ == "__main__":
  editor = EditorWindow()
  editor.run()