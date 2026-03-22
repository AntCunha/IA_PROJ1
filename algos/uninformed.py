from collections import deque
import heapq
from algos.base import SearchNode, reconstruct_path, successors


def bfs(puzzle) -> list[str] | None:
    """Breadth-First Search — optimal (fewest moves)."""
    root = SearchNode(state=puzzle.initial_state, parent=None, action=None, cost=0)

    if puzzle.checkEnd(root.state):
        return []

    frontier = deque([root])
    visited  = {root.state}

    while frontier:
        node = frontier.popleft()
        for child in successors(node, puzzle):
            if child.state in visited:
                continue
            if puzzle.checkEnd(child.state):
                return reconstruct_path(child)
            visited.add(child.state)
            frontier.append(child)

    return None  # no solution


def dfs(puzzle, max_depth: int = 50) -> list[str] | None:
    """Depth-First Search — not optimal, depth-limited to avoid infinite loops."""
    root = SearchNode(state=puzzle.initial_state, parent=None, action=None, cost=0)

    stack   = [root]
    visited = {root.state}

    while stack:
        node = stack.pop()
        if puzzle.checkEnd(node.state):
            return reconstruct_path(node)
        if node.cost >= max_depth:
            continue
        for child in successors(node, puzzle):
            if child.state not in visited:
                visited.add(child.state)
                stack.append(child)

    return None

