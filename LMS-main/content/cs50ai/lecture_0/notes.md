# Lecture 0 - Search

Artificial intelligence often begins with search: finding a sequence of actions that leads from an initial state to a goal state.

## Topics
- Agent
- State
- Initial State
- BFS
- DFS
- Greedy Best-First Search
- A* Search
- Minimax
- Alpha-Beta Pruning
- Depth-Limited Minimax

## Search Problems
A search problem is defined by:
- an **agent** that perceives the environment
- a **state** describing the current configuration
- an **initial state** where the search starts
- **actions** that move between states
- a **transition model** that defines the result of applying actions
- a **goal test** that determines whether we've reached the objective
- a **path cost** that defines how good a path is

## Agent and State
An agent is the thinking part of the program. In a navigator app, the agent receives the current location and decides the next move.

A state is a configuration of the world. In the 15-puzzle, each arrangement of tiles is a state. The set of all reachable states is the **state space**, often represented as a graph.

## Search Algorithms
### Depth-First Search (DFS)
DFS uses a **stack** frontier and explores one path as far as possible before backtracking.
- Pros: low memory overhead
- Cons: may not find the optimal path

```python
if self.empty():
    raise Exception("empty frontier")
else:
    node = self.frontier[-1]
    self.frontier = self.frontier[:-1]
    return node
```

### Breadth-First Search (BFS)
BFS uses a **queue** frontier and explores all states at a given depth before moving deeper.
- Pros: guaranteed to find the shortest path
- Cons: higher memory usage

### Greedy Best-First Search
Greedy best-first search expands the node that appears closest to the goal according to a heuristic function **h(n)**.
- Uses problem-specific knowledge
- Faster than uninformed search in many cases
- Not guaranteed optimal unless the heuristic is admissible

### A* Search
A* search combines path cost **g(n)** and heuristic **h(n)**:

```text
f(n) = g(n) + h(n)
```

A* is optimal when **h(n)** is admissible and consistent.

## Adversarial Search
Some problems involve opponents rather than a fixed goal.

### Minimax
Minimax models an adversarial game by assigning values to terminal states and choosing optimal actions for both players.

### Alpha-Beta Pruning
Alpha-beta pruning skips branches that cannot affect the final decision, improving minimax efficiency.

### Depth-Limited Minimax
Depth-limited minimax stops search after a fixed number of moves and uses an evaluation function to estimate non-terminal states.
