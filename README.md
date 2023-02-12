# BREAKOUT.py
This module is the main file of the Breakout game, which sets up the game window, handles user inputs and updates the game state. It includes the following steps:

### Import required modules:
-  pygame: for creating the game window, handling user inputs and updating the game state
-  BRKsettings: for game settings such as screen size, background color, etc.
-  BRKsprites: for creating the game objects such as the paddle, ball and blocks
-  BRKsurface: for creating the game surface with block images

### Initialize the game:
- Create the game window using pygame.display.set_mode() method with the screen size defined in BRKsettings.
- Set up the game clock using pygame.time.Clock() method to control the game speed.
- Load the game objects defined in BRKsprites module.
- Set up the game surface with the images defined in BRKsurface module.

### Game loop:
- Handle user inputs such as key presses and mouse clicks.
- Update the game state by moving the objects, checking for collisions, updating the score, etc.
- Draw the updated game state on the screen.
- Repeat the above steps until the game is over.

### Clean up:
- Quit the game using pygame.quit() method.

# BRKsettings.py
This module contains the game settings such as screen size, background color, block type, etc. The game settings are defined as constants and can be easily changed in this module without affecting the rest of the code.

# BRKsprites.py
This module contains the game objects such as the paddle, ball and blocks. It defines the classes for each object and their properties such as position, speed, size, etc. It also includes the methods for moving the objects and handling the collisions.

# BRKsurface.py
This module is responsible for creating the game surface with the block images. It includes the SurfaceMAKER class which has the following functionality:

### Initialization:
- Load the block images from the "blocks" directory using os.walk() method and store them in a dictionary with the block type as the key.

### Surface creation:
- Create a new surface using pygame.Surface() method with the specified size.
- Remove the black background from the surface using image.set_colorkey() method.
- Scale and paste the block images on the surface in the appropriate position to create the final game surface.

### Surface return:
- Return the final game surface.
