# Lecture 3 - Optimization

Optimization finds the best solution, not just a valid one.

## Topics
- Local Search
- Hill Climbing
- Simulated Annealing
- Traveling Salesman
- Linear Programming
- Constraint Satisfaction
- Backtracking Search
- Arc Consistency

## Local Search
Local search maintains a single candidate solution and moves to neighboring candidates.
- Useful when the full state space is too large
- Can find good solutions quickly

### Hill Climbing
Hill climbing moves to the best neighbor until no improvement remains.

```text
function Hill-Climb(problem):
  current = initial state
  repeat:
    neighbor = best neighbor of current
    if neighbor not better than current:
      return current
    current = neighbor
```

### Simulated Annealing
Simulated annealing sometimes accepts worse moves to escape local maxima.

## Traveling Salesman
The Traveling Salesman Problem seeks the shortest tour through a set of cities. Exact search is expensive, so heuristics and local search are used.

## Linear Programming
Linear programming optimizes a linear objective under linear constraints.
- Cost functions: `c1 x1 + c2 x2 + ...`
- Inequality constraints: `a1 x1 + a2 x2 <= b`

## Constraint Satisfaction
Constraint satisfaction problems assign values to variables subject to constraints.
- Variables
- Domains
- Constraints

### Backtracking Search
Backtracking recursively assigns values and undoes choices when a conflict occurs.

### Arc Consistency
Arc consistency removes inconsistent values from domains, which can dramatically prune search.
