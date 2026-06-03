import pygame as pg
import random as rd


def create_bricks(brick_count, screen_width):
    bricks = []

    rows = 5
    cols = 5

    brick_gap = 8
    brick_margin_x = 80
    brick_start_y = 60
    brick_height = 25

    brick_width = (screen_width - brick_margin_x * 2 - brick_gap * (cols - 1)) // cols

    positions = []

    for row in range(rows):
        for col in range(cols):
                positions.append((row, col))

    selected_positions = rd.sample(positions, brick_count)

    for row, col in selected_positions:
        x = brick_margin_x + col * (brick_width + brick_gap)
        y = brick_start_y + row * (brick_height + brick_gap)

        brick = pg.Rect(x, y, brick_width, brick_height)
        bricks.append(brick)

    return bricks

def draw_bricks(screen, bricks, color):
    for brick in bricks:
        pg.draw.rect(screen, color, brick)