import pygame
from puzzle import SWITCH_SIZE

BG          = (26,  26,  46)
TILE        = (128, 0, 128)
TILE_SWITCH = (255, 255,  0)
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
GREY        = (170, 170, 204)
BTN_BG      = (44, 44, 78)
BTN_HOVER   = (74, 74, 126)

TILE_W, TILE_H = 52, 52
TILE_GAP       = 8
STEP           = TILE_W + TILE_GAP
LEFT_W         = 150
BOARD_W        = 600
LOG_W          = 150
WIN_W, WIN_H   = LEFT_W + BOARD_W + LOG_W, 600
TOP_Y, BOT_Y   = 130, WIN_H - 100
BOARD_CX       = LEFT_W + BOARD_W // 2  # horizontal center of the board


def _track_bounds(k):
    left_x = LEFT_W + (BOARD_W - (k * TILE_W + (k - 1) * TILE_GAP)) // 2
    return left_x, left_x + (k - 1) * STEP


def tile_positions(n, k):
    left_x, right_x = _track_bounds(k)
    remaining = n - k
    side_n = max(0, (remaining - k) // 2)
    bot_n  = remaining - 2 * side_n

    pos = [(left_x + i * STEP, TOP_Y) for i in range(k)]

    if side_n:
        gap = (BOT_Y - TOP_Y) / (side_n + 1)
        pos += [(right_x, int(TOP_Y + (i + 1) * gap)) for i in range(side_n)]

    pos += [(right_x - i * STEP, BOT_Y) for i in range(bot_n)]

    if side_n:
        gap = (BOT_Y - TOP_Y) / (side_n + 1)
        pos += [(left_x, int(BOT_Y - (i + 1) * gap)) for i in range(side_n)]

    return pos


class Button:
    def __init__(self, x, y, w, h, label):
        self.rect  = pygame.Rect(x, y, w, h)
        self.label = label

    def draw(self, surface, font):
        color = BTN_HOVER if self.rect.collidepoint(pygame.mouse.get_pos()) else BTN_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, self.rect, 1, border_radius=6)
        txt = font.render(self.label, True, WHITE)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_tile(surface, val, x, y, color, font):
    rect = pygame.Rect(x, y, TILE_W, TILE_H)
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
    txt = font.render(str(val), True, BLACK)
    surface.blit(txt, txt.get_rect(center=rect.center))


# Left panel buttons (algorithms)
_bx, _bw, _bh, _gap = 15, 120, 32, 12
bfs_btn   = Button(_bx, 50,                  _bw, _bh, "BFS")
dfs_btn   = Button(_bx, 50 +   (_bh + _gap), _bw, _bh, "DFS")
reset_btn = Button(_bx, 50 + 4*(_bh + _gap), _bw, _bh, "Reset")


def draw(surface, state, puzzle, font, font_small):
    surface.fill(BG)
    n, k = puzzle.size, SWITCH_SIZE
    left_x, right_x = _track_bounds(k)

    # Left panel divider
    pygame.draw.line(surface, GREY, (LEFT_W, 0), (LEFT_W, WIN_H), 1)
    surface.blit(font_small.render("SOLVE", True, WHITE), (15, 20))
    bfs_btn.draw(surface, font_small)
    dfs_btn.draw(surface, font_small)
    reset_btn.draw(surface, font_small)

    # Track outline
    track_rect = pygame.Rect(left_x - 10, TOP_Y - 10,
                             right_x - left_x + TILE_W + 20,
                             BOT_Y - TOP_Y + TILE_H + 20)
    pygame.draw.rect(surface, GREY, track_rect, 2, border_radius=12)

    # Switch zone label
    lbl = font_small.render("SWITCH ZONE", True, TILE_SWITCH)
    surface.blit(lbl, lbl.get_rect(center=(BOARD_CX, TOP_Y - 18)))

    for i, (x, y) in enumerate(tile_positions(n, k)):
        draw_tile(surface, state[i], x, y, TILE_SWITCH if i < k else TILE, font)

    hint = font_small.render("← → rotate    SPACE switch", True, GREY)
    surface.blit(hint, hint.get_rect(center=(BOARD_CX, WIN_H - 30)))

    # Right log panel
    pygame.draw.line(surface, GREY, (LEFT_W + BOARD_W, 0), (LEFT_W + BOARD_W, WIN_H), 1)
    surface.blit(font_small.render("LOG", True, WHITE), (LEFT_W + BOARD_W + 10, 10))
    for i, (_, action) in enumerate(reversed(list(puzzle.log.items()))):
        if 30 + i * 20 > WIN_H - 10:
            break
        surface.blit(font_small.render(f"{len(puzzle.log) - i}. {action}", True, GREY),
                     (LEFT_W + BOARD_W + 10, 30 + i * 20))
