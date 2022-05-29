from abc import ABC, abstractmethod

class Tape:
  def __init__(self):
    self.contents = ['B']
    self.head = 0

  def set_input(self, word):
    self.contents = list(word)

  def read(self):
    return self.contents[self.head]

  def write(self, symbol : str):
    self.contents[self.head] = symbol

  def move_left(self):
    if self.head == 0:
      self.contents = ['B'] + self.contents
    else:
      self.head -= 1

  def move_right(self):
    if self.head >= len(self.contents) - 1:
      self.contents.append("B")
    self.head += 1


class GenericTM(ABC):
  def run(self):
    '''Runs the TM to completion'''

class DeterministicTM(GenericTM):
  '''
  transitions is a dictionary with elements of the form 
    (state, symbol) : (new_state, new_symbol, head_direction)
  '''
  def __init__(self, transitions, finals):
    self.state = 0
    self.tape = Tape()
    self.transitions = transitions
    self.finals = finals

  def step(self):
    st, symbol, direction = self.transitions[self.state, self.tape.read()]
    self.state = st
    self.tape.write(symbol)
    if direction == "R":
      self.tape.move_right()
    else:
      self.tape.move_left()

  def run(self, input):
    self.tape.set_input(input)
    print(self)
    while self.state not in self.finals:
      self.step()
      print(self)
  
  def __str__(self):
    return f"State: {self.state}, Tape: {self.tape.contents}, Head: {self.tape.head}"

def main():
  transitions = {
    (0, 'a') : (1, 'b', 'R'),
    (1, 'b') : (2, 'a', 'L')
  }
  finals = {2}

  T = DeterministicTM(transitions, finals)
  T.run("ab")

if __name__ == "__main__":
  main()
