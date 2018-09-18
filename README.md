# pygame_engine 1.1 #

Global Variables you need to know about:
 -game_state (string) change this string so the game knows which branch of the main game loop to run
 -objects (list [game_objects]) this list will be populated with objects as they are created
 -camera_position (tuple (int, int)) everything in world_space will be positioned based on the camera's position
 -DEADZONE (float) for analog joysticks
 -controller_count (int) use this to make looping through all the controllers easy.
  -for controller in range(controller_count)
 -button_count (list [int]) a list of controller button counts.
  -use button_count [controller] to loop through all the buttons on a controller easy. (Loop through all inputs quickly using a nested for loop.)
 -axis_count (list [int]) same as button_count but with axes.
  -Try plugging in different kinds of controllers to see the changes in these count arrays!
  -print ("Conrollers: %d, Buttons: %s, Axes: %s" % (controller_count, str(button_count), str(axis_count)))
 -LX = 0, LY = 1, RX = 3, RY = 4, LT = 2, RT = 5
  -These variables correspond to the appropriate Xinput axis, for ease of use.
 -A = 0, B = 1, X = 2, Y = 3, LB = 4, RB = 5, BACK = 6, START = 7, HOME = 8, L3 = 9, R3 = 10
  -Like the axis, these correspond the the Xinput buttons.
  -L3 and R3 are the sticks, when you click them.

Joystick management to go along with pygame's joystick code:
 -All joysticks are initialized and put in a list, then all the buttons are put in a few 2D lists. This is all done automatically.
 -the first axis is the controller index, and the second is the button or axis index.
 -Added support for 3 (4?) kinds of button input:
  -button_state[][] is true if the button is pressed
  -button_buffer[][] is true one frame after button_state[][] (This is mostly for testing if the button's state has changed.)
  -button_down[][] is true the first frame the button is pressed
  -button_up[][] is true the first frame the button is released
 -Added support for 2 (3?) kinds of axis input:
  -axis_state[][] is a float from -1.0 to 1.0 representing the joystick's current location
  -axis_buffer[][] trails one frame behind axis_state[][] to compare joystick changes
  -axis_motion[][] is 1.0 (or -1.0) on the first frame the axis leaves 0

A game_object class with easy to use rendering functions.
 -game_objects are all kept in a list called objects[]
  -To create a new game_object, use objects.append (object())
   -include parameter after object like you normally would when assigning to a variable
 -game_objects all have a name (a string) so they can be identified by a reasonable developer.
  -You can find the first-created game_object with any given name by calling the static Find() method. It takes a string, of course.
 -game_objects have a list of tags, and like the name variable, you can use these to search for certain objects.
  -Call the static Find_tag() method to get a list of all game_objects with at least one of the tags in the supplied list.
   -The tags don't have to be strings, the function will work with any data type (Needs testing).
 -game_objects have a rect and a rotation, used for position, rotation, and scaling.
  -You may set a game_object's position, rotation, and scale using the built-in functions:
   -Set_position () takes a tuple (int, int), and a boolean (relative)
   -Set_rotation () takes an int and the relative boolean
   -Set_scale () takes a tuple (int, int) and the relative boolean
  -All of these functions have an optional "relative" flag as the second parameter, set it to true to take the game_object's current state into account.
  -The Set_ fuctions also add the game_objects rect to the list of locations to update on the next frame, so only use these functions to move your objects around.
 -The world_space flag (boolean) tells the game_object if it needs to take the global camera_position into account for it's positioning on screen. If the flag is false the object is considered to be in screen_space.
 -Set_image properly unlocks and locks the surface, although this will probably change and be accompanied by a Render_over() method soon.
 -Draw() will draw the object, taking into condideration its size, scale, and if it is in world_space or not.
  -This took me 2 days to get right, all things considered.
 -Destroy() will delete the object and remove its reference in the objects list

A gamestate machine.
 -Technically this won't be a "feature" for long, just a part of the template.
 -The gamestate machine loops through the code and only runs the correct segment making "scene management" really easy.

This is an ECS based "engine", you create your classes and give them an __init__() function, but all functionality is done from global functions looping through the main objects list.
 -To get an ECS method working, create a global method such as the following:

def My_function():
	for object in objects:
		if isinstance(my_class, (valid_object_type_1, valid_object_type_2, ...)):
			#Run all code you need here, you should safely be able to use attributes
			#as the isinstance() method only allows objects with the appropriate structure
			#(as deemed by you) into this section.