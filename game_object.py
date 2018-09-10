#imports
import pygame, random, sys
from pygame.locals import *
#this list will be populated with objects as they are created
objects = []
#define objects
class game_object(object): #for the most part, you can leave this class alone: see README.md
    name = "object"
    tags = []
    rect = Rect(0, 0, 50, 50) #the ((x, y), (w, h)) position of the object
    world_space = True #change this to false and the object will be set to screen space
    scale = (1, 1) #the size to multiply by
    rotation = 0. #the rotation in degrees of the object
    active = False #code will not run for this object if active is false
    image = pygame.Surface ((0, 0)) #always load an image into this variable
    #to change the z-depth, change this objects position in the list of objects
    def __init__(self, rect, name = "game_object", image = pygame.Surface ((0, 0))): #construcion method
        self.name = name
        self.rect = Rect(rect)
        Set_image (image)
        self.Awaken()
    def Awaken(self): #awakens the object
        self.active = True
    def Sleep(self): #puts the object to sleep
        self.active = False
    def Set_position(self, position, relative = False): #takes a tuple (int, int), and moves the center of the object to the position. if relative, slides the object by that amount
        if relative:
            self.rect.center += position
        else:
            self.rect.center = position
    def Set_rotation(self, angle, relative = False): #takes an int, and sets the rotation of the object. If relative then the object is rotated by angle instead.
        if relative:
            self.angle += angle
        else:
            self.angle = angle
    def Set_scale (self, scale): #takes a tuple (int, int), and sets the object's scale. If relative, the object is inflated/deflated instead.
        if relative:
            self.rect.inflate_ip (scale [0], scale [1])
        else:
            self.rect.inflate_ip (scale[0] - self.rect.width, scale[1] - self.rect.height)
    def Set_image(self, image_path):
        self.image.unlock()
        self.image = pygame.image.load (image_path)
        self.image.lock()
    def Draw(self): #draws this object. If the space is set to world, the camera_position will be taken to account
        if self.active:
            output = self.image
            draw_rect = self.rect
            output = pygame.transform.scale(output, (draw_rect.width, draw_rect.height))
            output = pygame.transform.rotate(output, self.rotation)
            output_position = output.get_rect()
            output_position.center = draw_rect.center
            if self.world_space:
                window.blit (output, (output_position.centerx - camera_position [0], output_position.centery - camera_position[1]))
            else:
                window.blit (output, (output.position.centerx, output.position.centery))
    def Destroy(self): #destroys the object, removing all references as well
        objects.remove(self)
        del self
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
