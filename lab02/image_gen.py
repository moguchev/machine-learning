from PIL import Image, ImageDraw
from random import randrange as rr
from pathlib import Path


FIGURE_AMOUNT = 5

IMG_SIZE = 512
STEP = 128

MIN_SIZE_DIFF = STEP/8
MAX_SIZE_DIFF = STEP/2-1

MIN_COLOUR_DIFF = 50
MAX_COLOR_DIFF = 255

MIN_ANGLE = 3
MAX_ANGLE = 7


def iterate(coors: list, step):
    if coors[0] != IMG_SIZE-step/2:
        coors[0] += step
    else:
        coors[0] = step/2
        coors[1] += step if coors[1] != IMG_SIZE-step/2 else 0


def draw_circle(draw, coors):
    dr = rr(MIN_SIZE_DIFF, MAX_SIZE_DIFF)
    draw.ellipse((coors[0] - dr, coors[1] - dr, coors[0] + dr, coors[1] + dr),
                 fill=(
                     rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF),
                     rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF),
                     rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF)))


def draw_polygon(draw, coors):
    draw.regular_polygon(((coors[0]), (coors[1]), rr(MIN_SIZE_DIFF, MAX_SIZE_DIFF)),
                         rr(MIN_ANGLE, MAX_ANGLE), rotation=rr(0, 120),
                         fill=(
                             rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF),
                             rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF),
                             rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF)))


def draw_rectangle(draw, coors):
    dx = rr(MIN_SIZE_DIFF, MAX_SIZE_DIFF)
    dy = rr(MIN_SIZE_DIFF, MAX_SIZE_DIFF)
    draw.rectangle((coors[0] - dx, coors[1] - dy, coors[0] + dx, coors[1] + dy),
                   fill=(
                       rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF),
                       rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF),
                       rr(MIN_COLOUR_DIFF, MAX_COLOR_DIFF)))


def generate_images(num_images):
    figure_pool = [draw_polygon, draw_circle, draw_rectangle]

    for new_image_num in range(num_images):
        centre = [STEP/2, STEP/2]

        img = Image.new('RGB', (IMG_SIZE, IMG_SIZE), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        for fig in range(FIGURE_AMOUNT):
            figure_pool[rr(0, figure_pool.__len__())](draw, centre)
            iterate(centre, STEP)

        Path("sources").mkdir(parents=True, exist_ok=True)
        img.save(f"sources/test{new_image_num}.jpg")
