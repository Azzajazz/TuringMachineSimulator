import tkinter as tk
import math
from dataclasses import dataclass
from typing import NamedTuple, Optional


class Point(NamedTuple):
    x: float
    y: float


@dataclass
class StateInfo:
    centre: Point
    radius: float


@dataclass
class EventContext:
    active_transition: Optional[int] = None
    start_state: Optional[int] = None
    end_state: Optional[int] = None
    in_state: bool = False
    last_mouse_pos: Point = Point(0, 0)


### TODO: Figure out how to associate transitions with states in a way that makes maths simple.
### TODO: Figure out an alternative to "enter while right mouse button is pressed" event for snapping transitions.
# Holding down a mouse button blocks events from any widget except the focused one.
class EditorCanvas(tk.Canvas):
    state_radius = 20

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.context = EventContext()
        self.id_to_state_info: dict[int, StateInfo] = {}

        self.bind("<Button-1>", self.add_state)
        self.bind("<B3-Motion>", self.update_transition_draw)
        self.bind("<B3-ButtonRelease>", self.end_transition_draw)
        self.bind("<Button-2>", lambda _: print(self.find_withtag("<Button-3>")))

    def add_state(self, event) -> None:
        state_oval = self.create_oval(
            event.x - self.state_radius,
            event.y - self.state_radius,
            event.x + self.state_radius,
            event.y + self.state_radius,
            fill="white",
        )
        state_info = StateInfo(Point(event.x, event.y), self.state_radius)
        self.id_to_state_info[state_oval] = state_info

        self.tag_bind(state_oval, "<Button-3>", self.begin_transition_draw)
        self.tag_bind(state_oval, "<B3-Enter>", self.snap_transition)
        self.tag_bind(state_oval, "<B3-Leave>", self.unsnap_transition)

    def begin_transition_draw(self, event) -> None:
        state_id = self.find_withtag("current")[0]
        state_info = self.id_to_state_info[state_id]
        anchor_point = calculate_transition_anchor(
            state_info.centre, Point(event.x, event.y), self.state_radius
        )
        curve_point = calculate_curve_point(state_info.centre, Point(event.x, event.y))
        transition = self.create_line(
            anchor_point.x,
            anchor_point.y,
            curve_point.x,
            curve_point.y,
            event.x,
            event.y,
            arrow="last",
            smooth=True,
        )  # type: ignore

        self.context.start_state = state_id
        self.context.active_transition = transition

    def update_transition_draw(self, event) -> None:
        if self.context.in_state:
            return
        active_transition = self.context.active_transition
        start_state = self.context.start_state
        if active_transition is None or start_state is None:
            return

        state_info = self.id_to_state_info[start_state]
        anchor_point = calculate_transition_anchor(
            state_info.centre, Point(event.x, event.y), self.state_radius
        )
        curve_point = calculate_curve_point(state_info.centre, Point(event.x, event.y))
        self.coords(
            active_transition,
            anchor_point.x,
            anchor_point.y,
            curve_point.x,
            curve_point.y,
            event.x,
            event.y,
        )

    def end_transition_draw(self, event) -> None:
        end_state = self.context.end_state
        active_transition = self.context.active_transition
        if active_transition is None:
            return

        if end_state is None:
            self.delete(active_transition)
        else:
            self.context.active_transition = None
            self.context.start_state = None
            self.context.end_state = None

    def snap_transition(self, event) -> None:
        self.context.in_state = True
        active_transition = self.context.active_transition
        start_state = self.context.start_state
        if active_transition is None or start_state is None:
            return

        self.context.end_state = self.find_withtag("current")[0]

    def unsnap_transition(self, event) -> None:
        self.context.in_state = False
        self.context.end_state = None


def calculate_curve_point(p0: Point, p1: Point) -> Point:
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

