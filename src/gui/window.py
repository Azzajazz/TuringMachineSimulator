import tkinter as tk
from editorcanvas import EditorCanvas


class Window(tk.Tk):
    def __init__(self, width=900, height=500, **kwargs):
        super().__init__(**kwargs)

        self.build_window()
        self.geometry(f"{width}x{height}")

    def build_window(self):
        self.build_editor_canvas()
        self.build_options_frame()

    def build_editor_canvas(self):
        self.editor_canvas = EditorCanvas(self, bg="grey")
        self.editor_canvas.pack(side="right", fill="both", expand=True)

    def build_options_frame(self):
        options_frame = tk.Frame(self)
        options_frame.pack(side="left", fill="y", ipadx=10)
        self.build_tape_frame(options_frame)
        self.build_debug_frame(options_frame)
        self.build_description_frame(options_frame)

    def build_tape_frame(self, parent):
        tape_frame = tk.Frame(parent)
        tape_frame.pack(pady=10)
        tk.Label(tape_frame, text="Tape").pack()
        tape_slots_frame = tk.Frame(tape_frame)
        tape_slots_frame.pack()
        self.tape_slots_entries = [
            tk.Entry(tape_slots_frame, width=3) for _ in range(7)
        ]
        for entry in self.tape_slots_entries:
            entry.pack(side="left")
        self.tape_head_label = tk.Label(tape_frame, text="/\\")
        self.tape_head_label.pack()

    def build_debug_frame(self, parent):
        debug_frame = tk.Frame(parent)
        debug_frame.pack()
        self.build_input_frame(debug_frame)
        self.build_debug_button_frame(debug_frame)

    def build_input_frame(self, parent):
        input_frame = tk.Frame(parent)
        input_frame.pack(fill="x")
        tk.Label(input_frame, text="Input:").pack(side="left")
        self.input_entry = tk.Entry(input_frame)
        self.input_entry.pack(side="left", fill="x")

    def build_debug_button_frame(self, parent):
        debug_button_frame = tk.Frame(parent)
        debug_button_frame.pack()
        self.run_button = tk.Button(debug_button_frame, text="Run")
        self.run_button.pack(side="left")
        self.step_button = tk.Button(debug_button_frame, text="Step")
        self.step_button.pack(side="left")
        self.reset_button = tk.Button(debug_button_frame, text="Reset")
        self.reset_button.pack(side="left")
        self.stop_button = tk.Button(debug_button_frame, text="Stop")
        self.stop_button.pack(side="left")

    def build_description_frame(self, parent):
        description_frame = tk.Frame(parent)
        description_frame.pack(fill="x", side="bottom", pady=20, padx=10)
        self.alpha_label = tk.Label(
            description_frame, text="Alphabet = {a, b}", justify="left"
        )
        self.alpha_label.grid(row=0, column=0, sticky="w")
        self.alpha_button = tk.Button(description_frame, text="Set Alphabet")
        self.alpha_button.grid(row=1, column=0, sticky="w")
        self.state_label = tk.Label(
            description_frame, text="Q = {q0, q1}", justify="left"
        )
        self.state_label.grid(row=2, column=0, sticky="w")
        self.finals_label = tk.Label(description_frame, text="F = {q1}", justify="left")
        self.finals_label.grid(row=3, column=0, sticky="w")
        self.delta_label_1 = tk.Label(
            description_frame, text="delta(q0, a) = (q1, a, L)", justify="left"
        )
        self.delta_label_1.grid(row=4, column=0, sticky="w")
        self.delta_label_2 = tk.Label(
            description_frame, text="delta(q1, b) = (q0, a, L)", justify="left"
        )
        self.delta_label_2.grid(row=5, column=0, sticky="w")

        ### TODO: There's some more stuff that needs to go in this window, but not sure what yet. ###

    def run(self):
        self.mainloop()


def main():
    editor = Window()
    editor.run()


if __name__ == "__main__":
    main()

