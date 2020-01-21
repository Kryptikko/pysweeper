#! /bin/python
import random
from Queue import Queue

dimx = 4
dimy = 4
random.seed(30)
MINE_COUNT = 2

SIDES = [
    (-1, 1), (0,1), (1, 1),
    (-1, 0), (1,0),
    (-1,-1), (0,-1), (1, -1)
]


class RetryInputException(Exception):
    pass


def game_loop(board, dim):
    is_game_over = False
    scene = board_to_scene(board)
    while not is_game_over:
        dump(scene)
        try:
            user_input = get_input(dim[0], dim[1])
        except RetryInputException:
            print "Bad Input"
            user_input = get_input(dim[0], dim[1])

        is_game_over = apply_input(scene, board, user_input)


def board_to_scene(board):
    scene = []
    for row_idx in range(len(board)):
        scene.append([])
        for col_idx in range(len(board[row_idx])):
            scene[row_idx].append("*")
    return scene


def get_neighbors(xy, sides, grapth):
    for side in sides:
        side_x = xy[0]+side[0]
        side_y = xy[1]+side[1]
        if side_x in range(len(grapth)):
            if side_y in range(len(grapth[side_x])):
                yield (side_x, side_y)


def depth_first(grapth, start, frontier = []):

    frontier.append(start)
    for next in get_neighbors(start, SIDES, grapth):
        if _has_mine(grapth, next):
            frontier.append(next)
        elif not next in frontier:
            frontier += depth_first(grapth, next, frontier)

    return frontier


def _has_mine(grapth, loc):
    x, y = loc
    return grapth[x][y] > 0


def get_input(len_x, len_y):
    raw_x = input("Enter map x coordinates (between 0 and %s): " % len_x)
    raw_y = input("Enter map y coordinates (between 0 and %s): " % len_y)
    try:
        loc_x = __input_to_loc(raw_x, len_x)
        loc_y = __input_to_loc(raw_y, len_y)
    except Exception as e :
        raise RetryInputException("failed validation")
    return (loc_x, loc_y)


def __input_to_loc(raw, max_len):
    if not (type(raw) is int):
        raw = raw.strip()
        raw = int(raw)
    if not (raw in range(max_len)):
       raise "Out of bounds"
    return raw


def apply_input(scene, game_board, xy):
    x, y = xy
    if scene[x][y] != "*":
        return False
    if game_board[x][y] == 9:
        print ("BOOM")
        return True

    scene[x][y] = game_board[x][y]
    if scene[x][y] == 0:
        frontier = depth_first(game_board, (x,y))
        for loc in frontier:
            x, y = loc
            scene[x][y] = game_board[x][y]

    return False


def dump(game_map):
    output = "     "
    # column indexes
    for col in range(len(game_map[0])):
        output += "  %s  " % col
    output += "\n"
    output += "\n"

    for row in range(len(game_map)):
        # row indexes
        output += " %s   " % row
        for col in range(len(game_map[row])):
            output += "| %s |" % game_map[row][col]
        output += "\n"

    print output


def build_map(dimx, dimy):
    output = []

    for item in range(dimx):
        output.append([])
        for in_item in range(dimy):
            output[item].append(0)
    return output


def ley_mine_markers_generator(sides):
    def lay_mine_markers(output, xy):
        for (side_x, side_y) in get_neighbors(xy, sides, output):
            output[side_x][side_y] = min([9, output[side_x][side_y] + 1])
        return output
    return lay_mine_markers


def lay_mines(output, mine_count, random, lay_mine_markers):

    while mine_count > 0:
        x = random.randrange(0, dimx)
        y = random.randrange(0, dimy)
        if output[x][y] < 9:
            output[x][y] = 9
            lay_mine_markers(output, (x, y))
            mine_count -= 1

    return output

lay_mine_markers = ley_mine_markers_generator(SIDES)
game_map = build_map(dimx, dimy)
game_map = lay_mines(game_map, MINE_COUNT, random, lay_mine_markers)
game_loop(game_map, (dimx, dimy))
