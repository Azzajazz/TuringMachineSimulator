import tkinter as tk

class Window(tk.Tk):
  def __init__(self, width=900, height=500, **kwargs):
    super().__init__(**kwargs)

    # Main layout of the gui. Canvas on the right, options on the left
    self.editor_canvas = tk.Canvas(self, bg="grey")
    self.editor_canvas.pack(side="right", fill="both", expand=True)
    options_frame = tk.Frame(self)
    options_frame.pack(side="left", fill="y", expand=False)

    tk.Label(options_frame, text="Tape").pack()
    tape_slots_frame = tk.Frame(options_frame)
    tape_slots_frame.pack(fill="x")
    self.tape_slots_entries = [
      tk.Entry(tape_slots_frame, width=3) for _ in range(7)
    ]
    for entry in self.tape_slots_entries:
      entry.pack(side="left")
    self.tape_slots_entries[0].insert(0, "Hello!")
    self.tape_slots_entries[1].insert(0, "Goodbye!")
    # self.tape_entr.insert(0, "This will be a tape")
    # self.tape_entry.pack(side="top", fill="x")
    self.tape_head_label = tk.Label(options_frame, text="/\\")
    self.tape_head_label.pack(side="top", fill="x")

    # Buttons are organised in their own frame.
    debug_button_frame = tk.Frame(options_frame)
    debug_button_frame.pack()
    self.run_button = tk.Button(debug_button_frame, text="Run")
    self.run_button.pack(side="left")
    self.step_button = tk.Button(debug_button_frame, text="Step")
    self.step_button.pack(side="left")
    self.reset_button = tk.Button(debug_button_frame, text="Reset")
    self.reset_button.pack(side="left")
    self.stop_button = tk.Button(debug_button_frame, text="Stop")
    self.stop_button.pack(side="left")
    
    self.alpha_label = tk.Label(options_frame, text="Alphabet = {a, b}")
    self.alpha_label.pack()
    self.alpha_button = tk.Button(options_frame, text="Set Alphabet")
    self.alpha_button.pack()
    self.state_label = tk.Label(options_frame, text="Q = {q0, q1}")
    self.state_label.pack()
    self.finals_label = tk.Label(options_frame, text="F = {q1}")
    self.finals_label.pack()
    self.delta_label_1 = tk.Label(options_frame, text="delta(q0, a) = (q1, a, L)")
    self.delta_label_1.pack()
    self.delta_label_2 = tk.Label(options_frame, text="delta(q1, b) = (q0, a, L)")
    self.delta_label_2.pack()
    ### TODO: There's some more stuff that needs to go in this window, but not sure what yet. ###

    # Sizing the initial window
    self.geometry(f"{width}x{height}")

  def on_step_click(self, _):
    print("Clicked!")
  
  def clear_canvas(self, _):
    self.editor_canvas.delete("all")

  '''Running of the application'''
  def run(self):
    self.mainloop()

def main():
  editor = Window()
  editor.run()

if __name__ == "__main__":
  main()