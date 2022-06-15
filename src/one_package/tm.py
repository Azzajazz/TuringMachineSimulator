from abc import ABC, abstractmethod
from dataclasses import dataclass, field

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
  def add_state(self):
    '''Adds a state to the TM'''
  
  @abstractmethod
  def remove_state(self):
    '''Removes a state and all associated transitions from the TM'''

  @abstractmethod
  def add_transition(self):
    '''Adds a transition to the TM'''

  @abstractmethod
  def remove_transition(self):
    '''Removes a transition from the TM'''

  @abstractmethod
  def set_input(self, _: str):
    '''Sets the input of the TM'''

  @abstractmethod
  def step(self):
    '''Run the TM for one step'''

  @abstractmethod
  def run(self, _: str):
    '''Runs the TM until in a final state. May not terminate'''


@dataclass
class DeterministicTM(GenericTM):
  transitions: dict[tuple, tuple]
  finals: set[int]
  tape: Tape = Tape()
  state: int = 0

  def add_state(self):
    pass

  def remove_state(self):
    pass

  def add_transition(self):
    pass

  def remove_transition(self):
    pass

  def set_input(self, input: str):
    self.tape.set_input(input)

  def step(self):
    st, symbol, direction = self.transitions[self.state, self.tape.read()]
    self.state = st
    self.tape.write(symbol)
    if direction == "R":
      self.tape.move_right()
    else:
      self.tape.move_left()

  def run(self, input: str):
    self.set_input(input)
    print(self)
    while self.state not in self.finals:
      self.step()
      print(self) 
  
  def __repr__(self):
    return f"State: {self.state}, Tape: ({self.tape})"

def main():
  transitions = {
    (0, 'a') : (1, 'b', 'R'),
    (1, 'b') : (2, 'a', 'L')
  }
  finals = {2}

  T = DeterministicTM(transitions=transitions, finals=finals)
  T.run("ab")

if __name__ == "__main__":
  main()
