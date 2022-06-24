from gui.gui import EditorCanvas
from ..tm import DeterministicTM

class Events:
  def __init__(self):
    self.editor_canvas_events = {
      "<Button-1>": self.draw_state,
      "<Shift-Button-1>": self.draw_final_state,
      "<Button-3>": self.initialise_transition,
      "<B3-Motion>": self.draw_intermediate_transition,
      "<ButtonRelease-3>": self.finalise_transition,
    }
    self.button_events = {
      "run": self.on_run_click,
      "pause": self.on_pause_click,
      "step": self.on_step_click,
      "reset": self.on_reset_click,
    }
    self.engine = DeterministicTM()

  def bind_canvas_events(self, canvas: EditorCanvas):
    for event, handler in self.editor_canvas_events.items():
      canvas.bind(event, handler)

  