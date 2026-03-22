
import pygame
import puzzle
import ui
from algos.uninformed import bfs, dfs


def newPuzzle(n):
    p = puzzle.Puzzle(n, tuple(range(1, n+1)))
    p.genRandom()
    return p

def main():
    pygame.init()
    screen = pygame.display.set_mode((ui.WIN_W, ui.WIN_H))
    pygame.display.set_caption("Top Spin")
    clock = pygame.time.Clock()

    font       = pygame.font.SysFont("arial", 20, bold=True)
    font_small = pygame.font.SysFont("arial", 13)

    p = newPuzzle(10)
    state    = p.initial_state
    solution = []  # pending moves from solver
    run      = True

    def apply(action: str):
        nonlocal state
        if action == "rotate_left":
            state = p.rotate_left(state)
            p.addToLog("LeftR")
        elif action == "rotate_right":
            state = p.rotate_right(state)
            p.addToLog("RightR")
        elif action == "switch":
            state = p.switch(state)
            p.addToLog("Switch")

    initial_state = p.initial_state
    solveAssist = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    apply("rotate_left")
                elif event.key == pygame.K_RIGHT:
                    apply("rotate_right")
                elif event.key in (pygame.K_SPACE,):
                    apply("switch")

            elif ui.bfs_btn.is_clicked(event):
                solveAssist = True
                p.initial_state = state
                solution = bfs(p) or []
            elif ui.dfs_btn.is_clicked(event):
                solveAssist = True
                p.initial_state = state
                solution = dfs(p) or []
            elif ui.reset_btn.is_clicked(event):
                state = initial_state
                p.log = {}
                solution = []
                solveAssist = False

        # Animate one solution step per frame
        if solution:
            apply(solution.pop(0))

        ui.draw(screen, state, p, font, font_small)

        if p.checkEnd(state) and not solveAssist:
            run = False
            print("you won!!!!")

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
