import tkinter as tk
import math
from dataclasses import dataclass
from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float


@dataclass
class StateInfo:
    centre: Point
    radius: float


### TODO: Modularise mathematical calculations for reuse in several event bindings
### TODO: Figure out how to associate transitions with states in a way that makes maths simple.
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
        self.create_line(
            event.x,
            event.y,
            event.x,
            event.y,
            event.x,
            event.y,
            tags="drawing",
            smooth=True,
            arrow="last",
        )

    def update_transition(self, event):
        curve_x, curve_y = calculate_curve_point(
            Point(self.transition_start_x, self.transition_start_y),
            Point(event.x, event.y),
        )
        self.coords(
            "drawing",
            self.transition_start_x,
            self.transition_start_y,
            curve_x,
            curve_y,
            event.x,
            event.y,
        )

    def finalise_transition(self, _):
        self.dtag("drawing", "drawing")

        # TEMPORARY
        # state1 = self.create_oval(10, 10, 50, 50)
        # state1info = StateInfo(Point(30, 30), 20)
        # self.id_to_info_map[state1] = state1info

        # state2 = self.create_oval(10, 200, 50, 240)
        # state2info = StateInfo(Point(30, 220), 20)
        # self.id_to_info_map[state2] = state2info

        # centre_x, centre_y = calculate_transition_anchor(
        #     state1info.centre, state2info.centre, self.state_radius
        # )

        # self.create_oval(centre_x - 5, centre_y - 5, centre_x + 5, centre_y + 5)
        # END TEMPORARY

    def add_state(self, event):
        x0 = (event.x - self.state_radius,)
        y0 = (event.y - self.state_radius,)
        x1 = (event.x + self.state_radius,)
        y1 = event.y + self.state_radius
        new_id = self.create_oval(x0, y0, x1, y1)
        new_info = StateInfo(
            center=(0.5 * (x0 + x1), 0.5 * (y0 + y1)), radius=0.5 * abs(x0 - x1)
        )
        self.id_to_info_map[new_id] = new_info


def calculate_curve_point(p0: Point, p1: Point) -> tuple[float, float]:
    """
    Middle point for a curving transition: for transition starting at (x0, y0) and with head at (x1, y1),
    the point that defines the curve of the transition is
      (xmul * math.sqrt(r * r / (m * m + 1)) + xM, ymul * math.sqrt(r * r - r * r / (m * m + 1)) + yM)
    where
      xmul, ymul = +/-1 are determined based on the gradient of the line from (x0, y0) to (x1, y1)
      r = c||(x0, y0) - (x1, y1)||, with c a constant (TBD, controls the strength of the curve)
      m = (x1 - x0) / (y0 - y1)
      (xM, yM) = (0.5 * (x0 + x1), 0.5 * (y0 + y1)) is the midpoint of the line segment from (x0, y0) to (x1, y1)

    if y0 = y1, then m is undefined. In this case, the point that defines the curve of the transition is
    (xM, yM +/- r)
    """

    xM, yM = 0.5 * (p0.x + p1.x), 0.5 * (p0.y + p1.y)
    r = 0.4 * math.sqrt((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2)
    if p0.y == p1.y:
        curve_x, curve_y = xM, yM + math.copysign(r, p1.x - p0.x)
    else:
        m = (p0.x - p1.x) / (p1.y - p0.y)
        curve_x = math.copysign(math.sqrt(r * r / (m * m + 1)), p0.y - p1.y) + xM
        curve_y = (
            math.copysign(math.sqrt(m * m * r * r / (m * m + 1)), p1.x - p0.x) + yM
        )
    return Point(curve_x, curve_y)


def calculate_transition_anchor(p0: Point, p1: Point, radius: float) -> Point:
    """
    Transition anchor points: between circles with centers (x0, y0) and (x1, y1),
    the point on the circumference where a transition will join is
      (rcos(phi +/- theta) + x0, rsin(phi +/- theta) + y0)
    where
      theta is a fixed small angle (TBD)
      phi = atan2(y1 - y0, x1 - x0)
      r is the radius of the state (TBD)
    """

    height = p1.y - p0.y
    width = p1.x - p0.x
    phi = math.atan2(height, width)
    centre_x = 20 * math.cos(phi + 0.5) + p0.x
    centre_y = 20 * math.sin(phi + 0.5) + p0.y
    return Point(centre_x, centre_y)

