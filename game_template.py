#imports
import pygame, random, sys
from pygame.locals import *
from enum import Enum
from copy import deepcopy
#window initialization
pygame.init()
window = pygame.display.set_mode((800, 600)) #change the two numbers to set the window size
pygame.display.set_caption("Overhead") #the text at the top of the window

#timing initialization
FPS = 60 #change this to change the game's speed
FPSCLOCK = pygame.time.Clock ()

#system variable definitions
game_state = "menu" #change this string so the game knows which branch of the main game if statement to run
objects = [] #this list will be populated with objects as they are created
camera_position = (0, 0) #everything will be positioned based on the camera's position as well
DEADZONE = 0.1 #for analog joysticks


#load your assets in here (for large games consider loading only the required assets in a function)
BASICFONT = pygame.font.Font ("freesansbold.ttf", 12)







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
    for image in objects:
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

#Here is where you can add your own objects:






#joystick management
pygame.joystick.init()
controllers = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
controller_count = pygame.joystick.get_count()
button_count = []
axis_count = []
for controller in controllers:
    controller.init()
    button_count.append (deepcopy(controller.get_numbuttons()))
    axis_count.append (deepcopy(controller.get_numaxes()))

#input management
button_empty = []
button_state = []
button_buffer = []
button_down = []
button_up = []
axis_empty = []
axis_state = []
axis_buffer = []
axis_motion = []
for controller in range(controller_count):
    buffer = []
    for x in range(button_count [controller]):
        buffer.append(False)
    button_empty.append(deepcopy(buffer))
    button_state.append(deepcopy(buffer))
    button_buffer.append(deepcopy(buffer))
    button_down.append(deepcopy(buffer))
    button_up.append(deepcopy(buffer))
    buffer =  []
    for x in range(axis_count [controller]):
        buffer.append(0)
    axis_empty.append(deepcopy(buffer))
    axis_state.append(deepcopy(buffer))
    axis_buffer.append(deepcopy(buffer))
    axis_motion.append(deepcopy(buffer))
print (axis_empty)
#ints representing button and axis names
#this was written with XInput controllers in mind
LX = 0
LY = 1
RX = 3
RY = 4
LT = 2
RT = 5
A = 0
B = 1
X = 2
Y = 3
LB = 4
RB = 5
BACK = 6
START = 7
HOME = 8
L3 = 9
R3 = 10

def Get_inputs(): #to access any particular button, use "button_state [c][b]" where c is for controller and b is for button                
    for event in pygame.event.get(): # event handling loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.JOYBUTTONDOWN:
            button_state [event.joy][event.button] = True
            button_down [event.joy][event.button] = True
        elif event.type == pygame.JOYBUTTONUP:
            button_state [event.joy][event.button] = False
            button_up [event.joy][event.button] = True
        elif event.type == pygame.JOYAXISMOTION:
            axis_buffer = deepcopy (axis_state)
            axis_state[event.joy][event.axis] = event.value
            if abs(axis_state[event.joy][event.axis]) < abs(DEADZONE):
                axis_state[event.joy][event.axis] = 0
            if axis_state != 0 and axis_buffer [event.joy][event.axis] == 0:
                axis_motion[event.joy][event.axis] = (axis_state[event.joy][event.axis] - axis_buffer[event.joy][event.axis])
                if axis_motion [event.joy][event.axis] != 0:
                    axis_motion[event.joy][event.axis] /= abs(axis_motion[event.joy][event.axis])

#ECS functions. Search through the list of objects, and run the if statement if the object has all the data required






            
#game_state enumerator setup
class GAME_STATE(Enum):
    MENU = 0
    SETTINGS = 1
    SETUP = 2
    MAP = 3
    INVENTORY = 4
    BATTLE = 5
    TOWN = 6
    EVENT = 7
    TURN_PASS = 8
    OVERVIEW = 9
game_state = GAME_STATE.MENU

#global gameplay variables
menu_height = 0
player_count = 1








#main game loop
while True:
    #clear the screen for the next frame
    window.fill((255, 255, 255))
    #check for keystrokes
    Get_inputs()
        
    #expand this if statement as needed
    if game_state == GAME_STATE.MENU:
        #main menu code
        for button in range(button_count [1]):
            if button_up [1][button]:
                print (button)
    elif game_state == GAME_STATE.SETTINGS:
        #game logic
        ""
    else:
        #if your code gets here something went wrong
        pygame.quit()
        sys.exit()
    #update the screen
    Render_objects ()
    
    
    pygame.display.update()
    #clear the input variables
    button_down = deepcopy(button_empty)
    button_up = deepcopy(button_empty)
    axis_motion = deepcopy(axis_empty)
