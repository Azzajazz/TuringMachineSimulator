import tkinter as tk
import math
from dataclasses import dataclass
from typing import NamedTuple, Optional, TYPE_CHECKING
from enum import Enum, auto

if TYPE_CHECKING:
    from .controller import Controller


class Point(NamedTuple):
    x: float
    y: float


# TODO: Make a GUI element for selecting this
class ToolSelection(Enum):
    Move = auto()
    NewState = auto()
    NewStateFinal = auto()
    NewTransition = auto()


@dataclass
class StateNamer:
    current_id: int = 0

    @property
    def name(self):
        state_name = f"q{self.current_id}"
        self.current_id += 1
        return state_name


@dataclass
class EventContext:
    # The current editor tool
    tool: ToolSelection = ToolSelection.NewState
    # The transition we are currrently drawing.
    active_transition: Optional[int] = None
    # The starting state of the transition
    start_state: int = 0


### TODO: Figure out how to associate transitions with states in a way that makes maths simple.
class EditorCanvas(tk.Canvas):
    state_radius = 20
    state_inner_radius = 16

    def __init__(self, parent, **kwargs) -> None:
        super().__init__(parent, **kwargs)

        self.context = EventContext()
        self.namer = StateNamer()
        self.id_to_centre: dict[int, Point] = {}

        self.bind("<Button-1>", self.tool_dispatch)
        self.bind("<Motion>", self.update_transition)

    def set_tool(self, tool: ToolSelection) -> None:
        self.context.tool = tool

    def tool_dispatch(self, event) -> None:
        match self.context.tool:
            case ToolSelection.NewState:
                self.add_new_state(event)
            case ToolSelection.NewStateFinal:
                self.add_new_final_state(event)
            case ToolSelection.NewTransition:
                self.transition_click(event)
            case ToolSelection.Move:
                raise NotImplementedError

    def add_new_state(self, event) -> None:
        # If we click on something that already exists, don't create a new state
        if self.find_withtag("current"):
            return
        state_oval = self.create_oval(
            event.x - self.state_radius,
            event.y - self.state_radius,
            event.x + self.state_radius,
            event.y + self.state_radius,
            fill="white",
            tags="state",
        )
        self.tag_bind(state_oval, "state")
        self.id_to_centre[state_oval] = Point(event.x, event.y)
        self.controller.add_state(self.namer.name)

    def add_new_final_state(self, event) -> None:
        # If we click on something that already exists, don't create a new state
        if self.find_withtag("current"):
            return
        state_oval = self.create_oval(
            event.x - self.state_radius,
            event.y - self.state_radius,
            event.x + self.state_radius,
            event.y + self.state_radius,
            fill="white",
            tags="state",
        )
        self.create_oval(
            event.x - self.state_inner_radius,
            event.y - self.state_inner_radius,
            event.x + self.state_inner_radius,
            event.y + self.state_inner_radius,
        )
        self.id_to_centre[state_oval] = Point(event.x, event.y)
        self.controller.add_state(self.namer.name, True)

    def transition_click(self, event) -> None:
        transition = self.context.active_transition
        if transition:
            clicked = self.find_overlapping(event.x, event.y, event.x, event.y)
            if clicked and "state" in self.gettags(clicked[0]):
                centre_start = self.id_to_centre[self.context.start_state]
                centre = self.id_to_centre[clicked[0]]
                anchor1 = calculate_transition_anchor(
                    centre_start, centre, self.state_radius
                )
                anchor2 = calculate_transition_anchor(
                    centre, centre_start, self.state_radius, origin=False
                )
                curve = calculate_curve_point(anchor1, anchor2)
                self.coords(
                    transition,
                    anchor1.x,
                    anchor1.y,
                    curve.x,
                    curve.y,
                    anchor2.x,
                    anchor2.y,
                )
            else:
                self.delete(transition)
            self.context.active_transition = None
        else:
            clicked = self.find_withtag("current")
            if clicked and "state" in self.gettags(clicked[0]):
                centre = self.id_to_centre[clicked[0]]
                anchor = calculate_transition_anchor(
                    centre, Point(event.x, event.y), self.state_radius
                )
                curve = calculate_curve_point(centre, Point(event.x, event.y))
                self.context.active_transition = self.create_line(
                    anchor.x,
                    anchor.y,
                    curve.x,
                    curve.y,
                    event.x,
                    event.y,
                    smooth=True,
                    arrow="last",
                )  # type: ignore
                self.context.start_state = clicked[0]

    def update_transition(self, event) -> None:
        transition = self.context.active_transition
        # Only update the transition if there is one being drawn
        if transition is None:
            return
        centre = self.id_to_centre[self.context.start_state]
        anchor = calculate_transition_anchor(
            centre, Point(event.x, event.y), self.state_radius
        )
        curve = calculate_curve_point(anchor, Point(event.x, event.y))
        self.coords(transition, anchor.x, anchor.y, curve.x, curve.y, event.x, event.y)

    def set_controller(self, controller: "Controller"):
        self.controller = controller


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


def calculate_transition_anchor(
    p0: Point, p1: Point, radius: float, origin: bool = True
) -> Point:
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
    if origin:
        phi = math.atan2(height, width) + 0.5
    else:
        phi = math.atan2(height, width) - 0.5
    centre_x = 20 * math.cos(phi) + p0.x
    centre_y = 20 * math.sin(phi) + p0.y
    return Point(centre_x, centre_y)
