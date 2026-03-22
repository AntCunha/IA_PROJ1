
SWITCH_SIZE = 4

import random

class Puzzle:

    def __init__(self,n: int, starter: tuple[int,...]):
        self.size = n
        self.initial_state: tuple[int,...] = starter
        self.log: dict[int,str] = {}
        self.goal: tuple[int,...] = tuple(range(1,n+1))  # fully sorted array

    def rotate_left(self, currBoard: tuple[int,...]):
        return currBoard[1:] + (currBoard[0],)
    
    def rotate_right(self, currBoard: tuple[int,...]):
        return (currBoard[-1],) + currBoard[:-1]
    
    def switch(self, currBoard:tuple[int,...]):
        return currBoard[:SWITCH_SIZE][::-1]+currBoard[SWITCH_SIZE:]
    
    def addToLog(self, action: str):
        if action in ("LeftR", "RightR", "Switch"):
            self.log[len(self.log)] = action
            
    def checkEnd(self, currBoard:tuple[int,...]):
        return currBoard == self.goal or currBoard == self.goal[::-1]
    
    def genRandom(self):
        self.initial_state=tuple(random.sample(range(1, self.size + 1), self.size))
        return

