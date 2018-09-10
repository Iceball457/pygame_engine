#imports
import pygame, random, sys, input_manager, game_object, render_manager
from pygame.locals import *
from enum import Enum
from copy import deepcopy
#module initialization
pygame.init()
window = pygame.display.set_mode((800, 600)) #change the two numbers to set the window size
pygame.display.set_caption("Overhead") #the text at the top of the window
input_manager.joystick_init()
input_manager.input_init()
#timing initialization
FPS = 60 #change this to change the game's speed
FPSCLOCK = pygame.time.Clock ()
#system variable definitions
game_state = "menu" #change this string so the game knows which branch of the main game if statement to run
camera_position = (0, 0) #everything will be positioned based on the camera's position as well
#load your assets in here (for large games consider loading only the required assets in a function)
BASICFONT = pygame.font.Font ("freesansbold.ttf", 12)



#Here is where you can add your own objects:



#ECS functions. Search through the list of objects, and run the if statement if the object has all the data required


         
#game_state enumerator
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
    input_manager.Get_inputs()
        
    #expand this if statement as needed
    if game_state == GAME_STATE.MENU:
        #main menu code
        ""
    elif game_state == GAME_STATE.SETTINGS:
        #game logic
        ""
    else:
        #if your code gets here something went wrong
        pygame.quit()
        sys.exit()
    #update the screen
    render_manager.Render_objects ()
    pygame.display.update()
    #clear the input variables
    input_manager.Input_clear()
