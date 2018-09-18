#imports
import pygame, random, sys
from pygame.locals import *

pygame.init()

infoObject = pygame.display.Info()
window = pygame.Surface ((800, 600), pygame.DOUBLEBUF)
final = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)

#display settings
fullscreen = False

#list of locations to update on-screen
update_rects = []

#display update methods
def Frame_advance(objects):
    global update_rects
    #update the screen
    Render_objects (objects)
    Render_image(final, window, (int((final.get_width() / 2) - (window.get_width () * (final.get_height () / window.get_height ()) / 2)), 0), 0, (int(final.get_height () * (4 / 3)), final.get_height()), False)
    pygame.display.update(update_rects)
    update_rects = []
def Fullscreen_toggle():
    global fullscreen
    if fullscreen:
        final = pygame.display.set_mode ((800, 600))
    else:
        final = pygame.display.set_mode ((infoObject.current_w, infoObject.current_h), pygame.FULLSCREEN)
    fullscreen = not fullscreen

#rendering helpers
def Render_image(surface, image, position, rotation, scale, centered = True, upscale_amount = 0):
    if type(image) == type(""):
        output = pygame.image.load (image)
    else:
        output = image
    for x in range(upscale_amount):
        output = pygame.transform.scale2x(output)
    output = pygame.transform.scale(output, (scale[0], scale [1]))
    output = pygame.transform.rotate(output, rotation)
    output_position = output.get_rect()
    if centered:
        output_position.center = position
    else:
        output_position.topleft = position
    surface.blit(output, output_position)
def Draw_window(surface, rect, sprites, colors): #colors is a tuple of (r, g, b, a) tuples
    rect = Rect(rect)
    corner = Palette_swap (sprites[0].copy(), colors)
    edge = Palette_swap (sprites[1].copy(), colors)
    fill = Palette_swap (sprites[2].copy(), colors)
    output = pygame.Surface ((rect.width, rect.height), pygame.SRCALPHA)
    output.fill ((0, 0, 0, 0))
    Render_image (output, corner, (0, 0), 0, (5, 5), False)
    Render_image (output, corner, (0, output.get_height() - 5), 90, (5, 5), False)
    Render_image (output, corner, (output.get_width() - 5, 0), -90, (5, 5), False)
    Render_image (output, corner, (output.get_width() - 5, output.get_height() - 5), 180, (5, 5), False)
    Render_image (output, edge, (5, 0), 0, (output.get_width() - 10, 5), False)
    Render_image (output, edge, (0, 5), 90, (output.get_height() - 10, 5), False)
    Render_image (output, edge, (output.get_width() - 5, 5), -90, (output.get_height() - 10, 5), False)
    Render_image (output, edge, (5, output.get_height() - 5), 180, (output.get_width() - 10, 5), False)
    Render_image (output, fill, (5, 5), 0, (output.get_width() - 10, output.get_height() - 10), False)
    Render_image (surface, output, rect.topleft, 0, rect.size, False)

def Palette_swap(image, colors):
    if type(image) == type(""):
        output = pygame.image.load (image).copy()
    else:
        output = image
    output = pygame.PixelArray(image)
    for color in range(len(colors)):
        output.replace ((color, color, color, 255), colors[color])
    return output.make_surface()
def Render_objects (objects):
    for image in objects:
        image.Draw ()
def Blit_text(surface, text, pos, font, color=pygame.Color('white')):
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
