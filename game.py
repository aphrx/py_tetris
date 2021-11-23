import pygame
import sys
import random
from copy import deepcopy

frame_width = 500
frame_height = 1000
block_size = 50
dir = 0
fall = 0
lr = 0
score = 0

pygame.init()
pygame.display.set_caption("Tetris")

game_display = pygame.display.set_mode((frame_width, frame_height))
clock = pygame.time.Clock()

shapes = [
        [
            [
                [3*block_size, -2*block_size],
                [4*block_size, -2*block_size], # Line
                [5*block_size, -2*block_size],
                [6*block_size, -2*block_size]
            ],
            [
                [4*block_size, -1*block_size],
                [4*block_size, -2*block_size], # Line
                [4*block_size, -3*block_size],
                [4*block_size, -4*block_size]
            ],
            [
                [3*block_size, -3*block_size],
                [4*block_size, -3*block_size], # Line
                [5*block_size, -3*block_size],
                [6*block_size, -3*block_size]
            ],
            [
                [5*block_size, -1*block_size],
                [5*block_size, -2*block_size], # Line
                [5*block_size, -3*block_size],
                [5*block_size, -4*block_size]
            ],
        ],
        [
            [
                [4*block_size, -3*block_size],
                [4*block_size, -2*block_size], # L
                [4*block_size, -1*block_size],
                [5*block_size, -1*block_size]
            ],
            [
                [3*block_size, -2*block_size],
                [4*block_size, -2*block_size], # L
                [5*block_size, -2*block_size],
                [3*block_size, -1*block_size]
            ],
            [
                [5*block_size, -3*block_size],
                [5*block_size, -2*block_size], # L
                [5*block_size, -1*block_size],
                [4*block_size, -3*block_size]
            ],
            [
                [3*block_size, -1*block_size],
                [4*block_size, -1*block_size], # L
                [5*block_size, -1*block_size],
                [5*block_size, -2*block_size]
            ],
        ],
        [
            [
                [4*block_size, -3*block_size],
                [4*block_size, -2*block_size], # S
                [5*block_size, -2*block_size],
                [5*block_size, -1*block_size]
            ],
            [
                [5*block_size, -2*block_size],
                [4*block_size, -2*block_size], # S
                [4*block_size, -1*block_size],
                [3*block_size, -1*block_size]
            ],
            [
                [4*block_size, -1*block_size],
                [4*block_size, -2*block_size], # S
                [5*block_size, -2*block_size],
                [5*block_size, -3*block_size]
            ],
            [
                [3*block_size, -2*block_size],
                [4*block_size, -2*block_size], # S
                [4*block_size, -1*block_size],
                [5*block_size, -1*block_size]
            ],
        ],
        [
            [
                [4*block_size, -3*block_size],
                [4*block_size, -2*block_size], # T
                [4*block_size, -1*block_size],
                [5*block_size, -2*block_size]
            ],
            [
                [3*block_size, -2*block_size],
                [4*block_size, -2*block_size], # T
                [5*block_size, -2*block_size],
                [4*block_size, -1*block_size]
            ],
            [
                [5*block_size, -3*block_size],
                [5*block_size, -2*block_size], # T
                [5*block_size, -1*block_size],
                [4*block_size, -2*block_size]
            ],
            [
                [3*block_size, -1*block_size],
                [4*block_size, -1*block_size], # T
                [5*block_size, -1*block_size],
                [4*block_size, -2*block_size]
            ],
        ],
        [
            [
                [4*block_size, -1*block_size],
                [4*block_size, -2*block_size], # Sq
                [5*block_size, -1*block_size],
                [5*block_size, -2*block_size]
            ],
        ]
    ]

colors = [
    pygame.Color(3,65,174),
    pygame.Color(114,203,59),
    pygame.Color(255,213,0),
    pygame.Color(255,151,28),
    pygame.Color(255,50,19)
]

field_squares = []
field_colors = {}

rand_shape_index = random.randint(0, len(shapes)-1)                     # Random Shape Picker
curr_shape_index = random.randint(0, len(shapes[rand_shape_index])-1)   # Random Orientation Picker
curr_shape = deepcopy(shapes[rand_shape_index][curr_shape_index])       # Instance of Random Shape & Orientation

# Check if shape overlaps an existing game tile position
def in_field_squares(field_squares, sq):
    for fs in field_squares:
        if fs[0] == sq:
            return True
    return False

# Check if overflowing from visible game
def overflow_check(field_squares):
    for fs in field_squares:
        if fs[0][1] < 0:
            return True
    return False

# Remove tile from game
def fs_remove(field_squares, block):
    for fs in field_squares:
        if fs[0] == block:
            field_squares.remove(fs)
            break        
    return field_squares

# Quit Game
def quit():
    pygame.quit()
    sys.exit()

# Generate new shape
def new_shape(shape, rsi):
    for sq in shape:
        field_squares.append([sq, rsi])
    fall = 0
    lr = 0
    rand_shape_index = random.randint(0, len(shapes)-1)
    curr_shape_index = random.randint(0, len(shapes[rand_shape_index])-1)
    curr_shape = deepcopy(shapes[rand_shape_index][curr_shape_index])
    return rand_shape_index, curr_shape_index, curr_shape, fall, lr

# Move shape
def move(key):
    global curr_shape, curr_shape_index, lr, fall, dir
    # UP
    if key == 0:
        ocsi = deepcopy(curr_shape_index)
        ocs = deepcopy(curr_shape)
        if curr_shape_index == len(shapes[rand_shape_index])-1:
            curr_shape_index = 0
        else:
            curr_shape_index += 1
        curr_shape = deepcopy(shapes[rand_shape_index][curr_shape_index])
        for sp in curr_shape:
            sp[0] += lr
            sp[1] += fall
            
            # if sp[0] < 0 or sp[0] >= frame_width or in_field_squares(field_squares, sp):
            #     curr_shape_index = deepcopy(ocsi)
            #     curr_shape = deepcopy(ocs)
    # LEFT
    elif key == -1:
        lq = 0
        lock = False
        for sq in curr_shape:
            if not in_field_squares(field_squares, [sq[0]-block_size, sq[1]+block_size]):
                lq += 1
            if sq[0]-block_size < 0:
                lock = True
        if lq == 4 and not lock:
            dir = -block_size
    # RIGHT
    elif key == 1:
        lq = 0
        lock = False
        for sq in curr_shape:
            if not in_field_squares(field_squares, [sq[0]+block_size, sq[1]+block_size]):
                lq += 1
            if sq[0] + block_size == frame_width:
                lock = True
        if lq == 4 and not lock:
            dir = block_size

# Once a line is cleared to be removed
def remove_line(score, field_s):
    score += 100
    print(score)
    for fsi in range(frame_width//block_size):
        field_s = fs_remove(field_s, [fsi*block_size, fsj*block_size])
    tfs = []
    for fs in field_s:
        if fs[0][1] < fsj * block_size:
            tfs.append([[fs[0][0], fs[0][1]+block_size], fs[1]])
        else:
            tfs.append(fs)

    return score, tfs

while True:
    q = 0
    dir = 0

    # If shape overflows visible game space
    if overflow_check(field_squares):
        print("Game over")
        quit()

    # Move shape or change shape orientation
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(0)
            elif event.key == pygame.K_LEFT:
                move(-1)
            elif event.key == pygame.K_RIGHT:
                move(1)

    game_display.fill(pygame.Color(0, 0, 0))

    for sq in curr_shape: 
        if not in_field_squares(field_squares, [sq[0], sq[1]+block_size]) and sq[1]+block_size != frame_height :
            q += 1
        
    # Check    
    if q == 4:
        for sq in curr_shape:
            sq[0] += dir
            sq[1] += block_size
        fall += block_size
        lr += dir
    else:
        rand_shape_index, curr_shape_index, curr_shape, fall, lr = new_shape(curr_shape, rand_shape_index)

    # Draw shape
    for sq in curr_shape:
        pygame.draw.rect(game_display, colors[rand_shape_index], pygame.Rect(sq[0], sq[1], block_size, block_size))

    # Move tile
    for fsj in range(frame_height//block_size):
        count = 0
        for fsi in range(frame_width//block_size):
            if in_field_squares(field_squares, [fsi*block_size, fsj*block_size]):
                count += 1
        if count == 10:
            score, tfs = remove_line(score, field_squares)
            field_squares = deepcopy(tfs)

    # Draw placed tiles
    for sh in field_squares:
        pygame.draw.rect(game_display, colors[sh[1]], pygame.Rect(sh[0][0], sh[0][1], block_size, block_size))

    # Draw EW lines
    for i in range(frame_height//block_size):
        pygame.draw.line(game_display, pygame.Color(20,20,20), (0,i*block_size), (frame_width, i*block_size), 1)

    # Draw NS lines
    for j in range(frame_width//block_size):
        pygame.draw.line(game_display, pygame.Color(20,20,20), (j*block_size,0), (j*block_size, frame_height), 1)

    pygame.display.update()
    clock.tick(6)