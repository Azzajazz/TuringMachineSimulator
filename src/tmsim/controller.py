from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .turingmachine import GenericTM
    from .window import Window


class Controller:
    def __init__(self, machine: "GenericTM", window: "Window") -> None:
        self.machine = machine
        self.window = window

    def add_state(self, name: str, is_final: bool = False):
        self.machine.add_state(name, is_final)

    def save(self):
        self.machine.save_as_json()
