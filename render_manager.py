#imports
import pygame, random, sys, game_object
from pygame.locals import *
#rendering helpers
def Render_image(surface, image, position, rotation, scale):
    if type(image) == type(""):
        output = pygame.image.load (image)
    else:
        output = image
    output = pygame.transform.scale(output, (scale[0], scale [1]))
    output = pygame.transform.rotate(output, rotation)
    output_position = output.get_rect()
    output_position.center = position
    surface.blit(output, output_position)
def Render_objects ():
    for image in game_object.objects:
        image.Draw ()
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
