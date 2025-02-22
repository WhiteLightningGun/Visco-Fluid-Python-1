import pygame

def draw_pixel(surface, x, y, color):
    """
    Draws a pixel on the given pygame surface at the specified coordinates with the specified color.

    :param surface: The pygame surface to draw on.
    :param x: The x-coordinate of the pixel.
    :param y: The y-coordinate of the pixel.
    :param color: The color of the pixel (RGB tuple).
    """
    surface.set_at((x, y), color)