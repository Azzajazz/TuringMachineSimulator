from ssl import _create_unverified_context
import tkinter as tk
import math
from dataclasses import dataclass

class EditorCanvas(tk.Canvas):
  state_radius = 20

  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
    self.id_to_info_map: dict[int, StateInfo] = {}
    self.links: dict[int, int] = {}

    #TEMPORARY
    state1 = self.create_oval(10, 10, 50, 50)
    state1info = StateInfo((30, 30), 20)
    self.id_to_info_map[state1] = state1info
    
    state2 = self.create_oval(10, 200, 50, 240)
    state2info = StateInfo((30, 220), 20)
    self.id_to_info_map[state2] = state2info

    height = state2info.center[1] - state1info.center[1]
    width = state2info.center[0] - state1info.center[0]
    phi = math.atan2(height, width)
    center_x = 20 * math.cos(phi + 0.5) + state1info.center[0]
    center_y = 20 * math.sin(phi + 0.5) + state1info.center[1]
    self.create_oval(
      center_x - 5,
      center_y - 5,
      center_x + 5,
      center_y + 5
    )
    # self.bind("<Button-1>", self.add_state)
  
  def add_state(self, event):
    x0 = event.x - self.state_radius,
    y0 = event.y - self.state_radius,
    x1 = event.x + self.state_radius,
    y1 = event.y + self.state_radius
    new_id = self.create_oval(x0, y0, x1, y1)
    new_info = StateInfo(
      center=(0.5 * (x0 + x1), 0.5 * (y0 + y1)),
      radius=0.5 * abs(x0 - x1)
    )
    self.id_to_info_map[new_id] = new_info

@dataclass
class StateInfo:
  center: tuple[float, float]
  radius: float

'''
Transition anchor points: between circles with centers (x0, y0) and (x1, y1),
the point on the circumference where a transition will join is
  (rcos(phi +/- theta) + x0, rsin(phi +/- theta) + y0)
where
  theta is a fixed small angle (TBD)
  phi = atan2(y1 - y0, x1 - x0)
  r is the radius of the state (TBD)
'''