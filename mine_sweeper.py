import random

dimx = 4
dimy = 4
random.seed(30)
MINE_COUNT = 5

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
        user_input = get_input(dim[0], dim[1])
        is_game_over = apply_input(scene, board, user_input)


def board_to_scene(board):
    scene = []
    for row_idx in range(len(board)):
        scene.append([])
        for col_idx in range(len(board[row_idx])):
            scene[row_idx].append("*")
    return scene


def get_input(len_x, len_y):
    raw_x = input("Enter map x coordinates: ")
    raw_y = input("Enter map y coordinates: ")
    try:
        loc_x = __input_to_loc(raw_x, len_x)
        loc_y = __input_to_loc(raw_y, len_y)
    except Exception as e :
        raise RetryInputException(e)
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
        print("TODO: BREATH FIRST SEARCH")

    return False


def dump(game_map):
    for row in game_map:
        print (row)


def build_map(dimx, dimy):
    output = []

    for item in range(dimx):
        output.append([])
        for in_item in range(dimy):
            output[item].append(0)
    return output


def ley_mine_markers_generator(sides):
    def lay_mine_markers(output, xy):
        for side in sides:
            side_x = xy[0]+side[0]
            side_y = xy[1]+side[1]
            if side_x in range(len(output)):
                if side_y in range(len(output[side_x])):
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
