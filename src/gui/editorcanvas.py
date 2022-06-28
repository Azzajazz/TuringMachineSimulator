import tkinter as tk
import math
from dataclasses import dataclass

@dataclass
class StateInfo:
  center: tuple[float, float]
  radius: float

class EditorCanvas(tk.Canvas):
  state_radius = 20

  def __init__(self, parent, **kwargs):
    super().__init__(parent, **kwargs)
    self.id_to_info_map: dict[int, StateInfo] = {}
    self.links: dict[int, int] = {}

    self.bind("<Button-3>", self.begin_transition_draw)
    self.bind("<B3-Motion>", self.update_transition)
    self.bind("<ButtonRelease-3>", self.finalise_transition)

  def begin_transition_draw(self, event):
    self.transition_start_x = event.x
    self.transition_start_y = event.y
    self.create_line(event.x, event.y, event.x, event.y, event.x, event.y,
      tags="drawing", smooth=True, arrow="last")
  
  def update_transition(self, event):
    x0, y0 = self.transition_start_x, self.transition_start_y
    x1, y1 = event.x, event.y
    if y0 == y1:
      return
    if x1 >= x0 and y1 >= y0:
      xmul, ymul = -1, 1
    elif x1 >= x0 and y1 < y0:
      xmul, ymul = 1, 1
    elif x1 < x0 and y1 >= y0:
      xmul, ymul = -1, -1
    else:
      xmul, ymul = 1, -1
    xM, yM = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
    m = (x0 - x1) / (y1 - y0)
    r = 0.4 * math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    curve_x = xmul * math.sqrt(r * r / (m * m + 1)) + xM
    curve_y = ymul * math.sqrt(r * r - r * r / (m * m + 1)) + yM
    self.coords(
      "drawing",
      x0, y0,
      curve_x, curve_y,
      x1, y1
    )
  
  def finalise_transition(self, _):
    self.dtag("drawing", "drawing")

    # #TEMPORARY
    # state1 = self.create_oval(10, 10, 50, 50)
    # state1info = StateInfo((30, 30), 20)
    # self.id_to_info_map[state1] = state1info
    
    # state2 = self.create_oval(10, 200, 50, 240)
    # state2info = StateInfo((30, 220), 20)
    # self.id_to_info_map[state2] = state2info

    # height = state2info.center[1] - state1info.center[1]
    # width = state2info.center[0] - state1info.center[0]
    # phi = math.atan2(height, width)
    # center_x = 20 * math.cos(phi + 0.5) + state1info.center[0]
    # center_y = 20 * math.sin(phi + 0.5) + state1info.center[1]
    # self.create_oval(
    #   center_x - 5,
    #   center_y - 5,
    #   center_x + 5,
    #   center_y + 5
    # )
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

'''
Transition anchor points: between circles with centers (x0, y0) and (x1, y1),
the point on the circumference where a transition will join is
  (rcos(phi +/- theta) + x0, rsin(phi +/- theta) + y0)
where
  theta is a fixed small angle (TBD)
  phi = atan2(y1 - y0, x1 - x0)
  r is the radius of the state (TBD)
'''

'''
Middle point for a curving transition: for transition starting at (x0, y0) and with head at (x1, y1),
the point that defines the curve of the transition is
  (xmul * math.sqrt(r * r / (m * m + 1)) + xM, ymul * math.sqrt(r * r - r * r / (m * m + 1)) + yM)
where
  xmul, ymul are determined based on the gradient of the line from (x0, y0) to (x1, y1)
  r = c||(x0, y0) - (x1, y1)||, with c a constant (TBD, controls the strength of the curve)
  m = (x1 - x0) / (y0 - y1)
  (xM, yM) = (0.5 * (x0 + x1), 0.5 * (y0 + y1)) is the midpoint of the line segment from (x0, y0) to (x1, y1)
'''