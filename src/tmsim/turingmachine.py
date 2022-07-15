from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from .controller import Controller


@dataclass
class Tape:
    contents: list[str] = field(default_factory=list)
    head: int = 0

    def set_input(self, input: str):
        self.contents = list(input)

    def read(self):
        return self.contents[self.head]

    def write(self, symbol: str):
        self.contents[self.head] = symbol

    def move_left(self):
        if self.head == 0:
            self.contents = ["B"] + self.contents
        else:
            self.head -= 1

    def move_right(self):
        if self.head >= len(self.contents) - 1:
            self.contents.append("B")
        self.head += 1

    def __repr__(self):
        return f"Contents: {self.contents}, Head: {self.head}"


class GenericTM(ABC):
    @abstractmethod
    def add_state(self, state: str, is_final: bool):
        """Adds a state to the TM"""

    @abstractmethod
    def remove_state(self, state: str):
        """Removes a state and all associated transitions from the TM"""

    @abstractmethod
    def add_transition(self, transition: tuple):
        """Adds a transition to the TM"""

    @abstractmethod
    def remove_transition(self, rule: tuple):
        """Removes a transition from the TM"""

    @abstractmethod
    def set_input(self, input: str):
        """Sets the input of the TM"""

    @abstractmethod
    def step(self):
        """Run the TM for one step"""

    @abstractmethod
    def run(self, _: str):
        """Runs the TM until in a final state. May not terminate"""

    @abstractmethod
    def set_controller(self, controller: "Controller"):
        """Set the controller for interfacing with the gui"""


@dataclass
class DeterministicTM(GenericTM):
    current_state: str = ""
    states: set[str] = field(default_factory=set)
    transitions: dict[tuple, tuple] = field(default_factory=dict)
    finals: set[str] = field(default_factory=set)
    tape: Tape = Tape()
    controller: Optional["Controller"] = None

    @classmethod
    def from_json_file(cls, file):
        with open(file, "r") as f:
            json_info = json.load(f)

        states = set(json_info["states"])
        finals = set(json_info["finals"])
        current_state = json_info["initial"]

        transitions = {}
        for state, trans in json_info["transitions"].items():
            for symbol, change in trans.items():
                transitions[state, symbol] = tuple(change)

        return cls(
            states=states,
            transitions=transitions,
            finals=finals,
            current_state=current_state,
        )

    def add_state(self, state: str, final: bool = False):
        self.states.add(state)
        if final:
            self.finals.add(state)

    def remove_state(self, state: str):
        self.states.remove(state)
        if state in self.finals:
            self.finals.remove(state)
        ### TODO: What to do with current_state? ###
        self.current_state = ""

    def add_transition(self, transition: tuple):
        input, output = transition
        self.transitions[input] = output

    def remove_transition(self, rule: tuple):
        self.transitions.pop(rule)

    def set_input(self, input: str):
        self.tape.set_input(input)

    def step(self) -> bool:
        if (self.current_state, self.tape.read()) not in self.transitions:
            return False
        st, symbol, direction = self.transitions[self.current_state, self.tape.read()]
        self.current_state = st
        self.tape.write(symbol)
        if direction == "R":
            self.tape.move_right()
        else:
            self.tape.move_left()
        return True

    def run(self):
        valid_transition = True
        while self.current_state not in self.finals and valid_transition:
            print(self)
            valid_transition = self.step()

    def set_controller(self, controller: "Controller"):
        self.controller = controller

    def __repr__(self):
        return f"State: {self.current_state}, Tape: ({self.tape})"


def main():
    tm = DeterministicTM.from_json_file("test.json")
    tm.set_input("1111")
    tm.run()


if __name__ == "__main__":
    main()
