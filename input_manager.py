#imports
import pygame, random, sys
from pygame.locals import *
from copy import deepcopy
#global variables
DEADZONE = 0.1 #for analog joysticks
#input arrays
button_empty = []
button_state = []
button_buffer = []
button_down = []
button_up = []
axis_empty = []
axis_state = []
axis_buffer = []
axis_motion = []
#ints representing button and axis names
#this was written with XInput controllers in mind
LX = 0
LY = 1
RX = 3
RY = 4
LT = 2
RT = 5
FA = 0
FB = 1
FX = 2
FY = 3
LB = 4
RB = 5
BACK = 6
START = 7
HOME = 8
LC = 9
RC = 10
#counts and count arrays
controller_count = 0
button_count = []
axis_count = []
#joystick management
def joystick_init():
    global contollers, controller_count, button_count, axis_count
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
def input_init():
    global button_empty, button_state, button_buffer, button_down, button_up, axis_empty, axis_state, axis_buffer, axis_motion
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
def Input_clear():
    global button_down, button_empty, button_up, axis_motion, axis_empty
    button_down = deepcopy(button_empty)
    button_up = deepcopy(button_empty)
    axis_motion = deepcopy(axis_empty)
