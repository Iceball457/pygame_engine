#imports
import pygame, sys, random
from . import input_manager as Input
from . import render_manager as Screen
from pygame.locals import *
from enum import Enum
from copy import deepcopy
#module initialization
pygame.init()
pygame.display.set_caption("Overhead") #the text at the top of the window
Input.joystick_init()
Input.input_init()
#timing initialization
FPS = 60 #change this to change the game's speed
FPSCLOCK = pygame.time.Clock ()
#system variable definitions
camera_position = (0, 0) #everything will be positioned based on the camera's position as well
game_state = 0
#this list will be populated with objects as they are created
objects = []


def Game_tick():
    pass #Use monkey patching to replace this function with the behavior you want
    """Have this code in your game script... assuming you imported this as Engine
    def Game_tick():
        #Code here
    
    Engine.Game_tick = Game_tick 
    """
def Run_game():
    while True:
        Input.Get_inputs()
        Game_tick()
        Screen.Frame_advance(objects)
        Input.Input_clear()

#define objects
class game_object(object): #for the most part, you can leave this class alone: see README.md
    name = "object"
    tags = []
    rect = Rect(0, 0, 50, 50) #the ((x, y), (w, h)) position of the object
    world_space = True #change this to false and the object will be set to screen space
    rotation = 0. #the rotation in degrees of the object
    active = False #code will not run for this object if active is false
    image = pygame.Surface ((0, 0)) #always load an image into this variable
    #to change the z-depth, change this objects position in the list of objects
    def __init__(self, rect, name = "game_object", image = pygame.Surface ((0, 0))): #construction method
        self.name = name
        self.tags = []
        self.rect = Rect(rect)
        self.world_space = True
        self.rotation = 0
        self.active = False
        self.Set_image (image)
        self.Awaken()
    def Awaken(self): #awakens the object
        self.active = True
    def Sleep(self): #puts the object to sleep
        self.active = False
    def Set_position(self, position, relative = False): #takes a tuple (int, int), and moves the center of the object to the position. if relative, slides the object by that amount
        Screen.update_rects.append(self.rect.copy())
        if relative:
            self.rect.center += position
        else:
            self.rect.center = position
        Screen.update_rects.append(self.rect.copy())
    def Set_rotation(self, angle, relative = False): #takes an int, and sets the rotation of the object. If relative then the object is rotated by angle instead.
        Screen.update_rects.append(self.rect.copy())
        if relative:
            self.angle += angle
        else:
            self.angle = angle
        Screen.update_rects.append(self.rect.copy())
    def Set_scale (self, scale): #takes a tuple (int, int), and sets the object's scale. If relative, the object is inflated/deflated instead.
        Screen.update_rects.append(self.rect.copy())
        if relative:
            self.rect.inflate_ip (scale [0], scale [1])
        else:
            self.rect.inflate_ip (scale[0] - self.rect.width, scale[1] - self.rect.height)
        Screen.update_rects.append(self.rect.copy())
    def Set_image(self, image_path):
        if type(image_path) == type(""):
            self.image = pygame.image.load (image_path)
        else:
            self.image = image_path
    def Add_image(self, image_path):
        if type(image_path) == type(""):
            buffer = pygame.image.load (image_path)
        else:
            buffer = image_path
        self.image.blit(buffer)
    def Draw(self, centered = False): #draws this object. If the space is set to world, the camera_position will be taken to account
        if self.active:
            output = self.image
            draw_rect = self.rect
            output = pygame.transform.scale(output, (draw_rect.width, draw_rect.height))
            output = pygame.transform.rotate(output, self.rotation)
            output_position = output.get_rect()
            output_position.topleft = draw_rect.topleft
            if self.world_space:
                Screen.Render_image (Screen.window, output, (output_position.left - camera_position [0], output_position.top - camera_position[1]), 0, (output_position.width, output_position.height), False)
            else:
                Screen.Render_image (Screen.window, output, output_position.topleft, 0, (output_position.width, output_position.height), False)
    def Destroy(self): #destroys the object, removing all references as well
        objects.remove(self)
        del self
    @staticmethod
    def Instantiate(rect, name = "game_object", image = pygame.Surface ((0, 0))):
        buffer = game_object(rect, name, image)
        objects.append (buffer)
        return buffer 
    @staticmethod
    def Find(name):
        for object in objects:
            if isinstance (object, game_object):
                if object.name == name:
                    return object
    @staticmethod
    def Find_tag(tags):
        output = []
        for object in objects:
            if object.active:
                added = False
                if isinstance (object, game_object):
                    for tag in object.tags:
                        for check in tags:
                            if tag == check:
                                output.append (object)
                                added = True
                        if added:
                            break
        return output
