import tkinter as tk
import tkinter.ttk as ttk

class EditorCanvas(tk.Canvas):
  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
    tk.Label(self, text="Canvas for creating and editing TMs").pack()
  
  ### TODO: Work out how to deal with events on this canvas ###

### TODO: Make this window prettier. ###
class EditorWindow(tk.Tk):
  def __init__(self, width=900, height=500, **kwargs):
    super().__init__(**kwargs)

    # Main layout of the gui. Canvas on the right, options on the left
    self.editor_canvas = EditorCanvas(self, bg="grey")
    self.editor_canvas.pack(side="right", fill="both", expand=True)
    options_frame = tk.Frame(self, bg="#e9e9e9")
    options_frame.pack(side="left", fill="y", expand=False)

    # Things that go in the option frame.
    # These are members of the EditorWindow class since they will affect the canvas and each other.
    self.tape_entry = tk.Entry(options_frame)
    self.tape_entry.insert(0, "This will be a tape")
    self.tape_entry.pack(side="top", fill="x")
    self.tape_head_label = tk.Label(options_frame, text="/\\")
    self.tape_head_label.pack(side="top", fill="x")

    # Buttons are organised in their own frame.
    button_frame = tk.Frame(options_frame)
    button_frame.pack(side="top", fill="x")
    self.play_button = tk.Button(button_frame, text="Play")
    self.play_button.pack(side="left")
    self.step_button = tk.Button(button_frame, text="Step")
    self.step_button.pack(side="left")
    self.reset_button = tk.Button(button_frame, text="Reset")
    self.reset_button.pack(side="left")
    self.stop_button = tk.Button(button_frame, text="Stop")
    self.stop_button.pack(side="left")

    ### TODO: There's some more stuff that needs to go in this window, but not sure what yet. ###

    # Sizing the initial window
    self.geometry(f"{width}x{height}")

  '''Running of the application'''
  def run(self):
    self.mainloop()

if __name__ == "__main__":
  editor = EditorWindow()
  editor.run()