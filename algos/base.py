from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SearchNode:
    state:  tuple
    parent: Optional["SearchNode"]
    action: Optional[str]
    cost:      int  


def reconstruct_path(node: SearchNode) -> list[str]:
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return list(reversed(actions))


def successors(node: SearchNode, puzzle) -> list[SearchNode]:
    #3 sucessors (rl , rr , switch)
    result = []
    for action, fn in [
        ("rotate_left",  puzzle.rotate_left),
        ("rotate_right", puzzle.rotate_right),
        ("switch",       puzzle.switch),
    ]:
        result.append(SearchNode(
            state=fn(node.state),
            parent=node,
            action=action,
            cost=node.cost + 1,
        ))
    return result
