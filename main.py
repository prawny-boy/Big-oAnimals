"""
Genre: Game, Fighting/Gambling
Author: Sean Chan
Visuals: Pygame/Python
Art Style: Pixel Art

Description:
Game where you use animals that you catch to fight levels of enemies.

Features:
- Catching animals
- Fighting enemies
    2 Modes: Campaign (with levels) and Challenge
- Money
- Upgrades (Shop)

Coding Conventions:
- Use snake_case for variable names, and all capitals for constants
- Use camelCase for function names
- Use PascalCase for class names
"""

import pygame as _pygame
from sys import exit as _exit
from os import getcwd as _getcwd
import random as _random

# Special Functions
def convertFileName(filepath:str): # use windows filepath
    # Get file path type
    if "D:" in _getcwd():
        try:
            file_test = "Big-oAnimals/"+'save.txt'.replace("\\", "/")
            with open(file_test, 'r') as _:
                pass
            file_path_type = "Big-oAnimals/"
        except:
            file_test = 'save.txt'.replace("\\", "/")
            print(f"File test: {file_test}")
            with open(file_test, 'r') as _:
                pass
            file_path_type = _getcwd().split("/")[-1]
    
    # Change file name
    if 'C:' in _getcwd():
        return filepath
    elif 'D:' in _getcwd():
        return file_path_type + filepath.replace("\\", "/")
    else:
        return _getcwd()+"/"+filepath.replace("\\", "/")

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SAVE_FILE = "save.txt"
FPS = 60

# Variables
user = ""

# Initializations
# Pygame Screen
_pygame.init()
clock = _pygame.time.Clock()
WINDOW = _pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
_pygame.display.set_caption("Big-oAnimals")

# Others
_pygame.font.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
HEADING_FONT = _pygame.font.Font(convertFileName("Fonts\\PixeloidSansBold.ttf"), 50)
SUBTITLE_FONT = _pygame.font.Font(convertFileName("Fonts\\PixeloidMono.ttf"), 30)
TEXT_FONT = _pygame.font.Font(convertFileName("Fonts\\PixeloidMono.ttf"), 20)

# Images


# Classes
class Button(_pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y, 
        width, 
        height,
        direct_to, 
        colour = WHITE, 
        border_colour = BLACK, 
        border_width = 5, # this is thickness of the border
        border_radius = 10 # this is curving of edges
    ):
        super().__init__()
        self.coordinates = (x, y)
        self.size = (width, height)
        self.colour = colour
        self.border_colour = border_colour
        self.border_width = border_width
        self.border_radius = border_radius
        self.image = _pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft = self.coordinates)
        self.surface_input = _pygame.display.get_surface()
        self.direct_to = direct_to
    
    def draw(self):
        # Draw the button 
        self.image.fill(self.colour)
        # Draw the border
        _pygame.draw.rect(self.image, self.border_colour, self.rect, self.border_width, self.border_radius)
        # Blit the button onto the surface
        self.surface_input.blit(self.image, self.rect)
    
    def check_click(self):
        mouse_pos = _pygame.mouse.get_pos()
        left_click = _pygame.mouse.get_pressed()[0]
        button_rect = _pygame.rect.Rect(self.coordinates, self.size)
        if left_click and button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False
    
    def update(self):
        self.draw()

# Functions
def save(user, stats:dict):
    pass

def load(user):
    pass

def back(current_screen):
    pass

# Main Loop ---------------------------------------------------------------------------------------------------------------------------------------

# Sprite Groups for buttons
# Example
example_group = _pygame.sprite.Group()
button_1 = Button(100, 100, 100, 100, "example screen")
button_2 = Button(200, 200, 100, 100, "example screen")
example_group.add(button_1, button_2)

current_screen = "User Page"

while True:
    WINDOW.fill(BLACK)

    for event in _pygame.event.get():
        if event.type == _pygame.QUIT:
            _exit()
        elif event.type == _pygame.MOUSEBUTTONUP:
            pass
        elif event.type == _pygame.KEYDOWN:
            key_pressed = _pygame.key.get_pressed()
            if key_pressed[_pygame.K_ESCAPE]:
                back(current_screen)
    
    # Game Screens
    if current_screen == "User Page":
        # Draw a title

        # Draw buttons
        example_group.update()

        # Change screen if a button is clicked
        button:Button
        for button in example_group:
            if button.check_click():
                current_screen = button.direct_to
                print(current_screen)

    _pygame.display.update()
    clock.tick(FPS)