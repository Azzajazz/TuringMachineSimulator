# Turing Machine Simulator and Editor

This is intended to be a tool to build and run Turing Machines. It is not functional currently, but here's some intended features:
- Visual editing and creation of Turing Machines
- Debugging of Turing Machines (step, run, reset, etc.)
- Support for Turing Machine extensions (non-determinism, alternating, multi-tape, etc.)
- Designing and saving of Turing Machine "modules". Modules can be pieces together in various ways to make more complicated Turing Machines

## Controls

### Visual editor
For the visual editor area on the right:
- Click empty area to make state. Shift-click to create a final state. Then type in state symbol name (latex support may come later)
- Right click & drag from one state to another to make a transition. Label the transition immediately after (or later). Click & click will also be supported(?)
- Double click a transition or state to rename/relabel it.

### Simulations
For the buttons that control the simulation:
- Enter an input into the text box just above the buttons.
- Click the **run** button to simulate the Turing Machine to completion (or until paused). Speed can be set by a slider(?)
- Click the **pause** button to pause execution at the current step.
- Click the **step** button to simulate one step of the Turing Machine.
- Click the **reset** button to reset the simulation to its initial state.
Keyboard shortcuts:
- **run**/**pause**: Shift-Space
- **step** (once paused): Space
- **reset**: Shift-R