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
        x:int,
        y:int, 
        width:int, 
        height:int,
        text:str,
        direct_to:str, 
        colour:tuple = WHITE, 
        border_colour:tuple = BLACK,
        text_colour:tuple = BLACK,
        text_font:_pygame.font.Font = TEXT_FONT,
        border_width:int = 5, # this is thickness of the border
        border_radius:int = -1, # this is curving of edges
        accent_type:str = "colour", # 3 modes, colour, size and opacity
        accent_value:tuple|int = BLACK # this is the value of the accent, it can be a rgb value, size added (int) or the opacity of accented (int)
    ):
        super().__init__()
        offset = (width / 2, height / 2)
        self.coordinates = (x - offset[0], y - offset[1])
        self.size = (width, height)
        self.colour = colour
        self.text = text
        self.text_colour = text_colour
        self.text_font = text_font
        self.border_colour = border_colour
        self.border_width = border_width
        self.border_radius = border_radius
        self.direct_to = direct_to
        self.accent_type = accent_type
        self.accent_value = accent_value
    
    def check_hover(self):
        mouse_pos = _pygame.mouse.get_pos()
        button_rect = _pygame.rect.Rect(self.coordinates, self.size)
        if button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def draw(self):
        hover = self.check_hover()
        if self.accent_type == "size" and hover:
            self.image = _pygame.Surface((self.size[0]*self.accent_value, self.size[1]*self.accent_value))
        else:
            self.image = _pygame.Surface(self.size)
        self.rect = self.image.get_rect(topleft = (self.coordinates))
        self.surface_input = _pygame.display.get_surface()
        # Draw the fill on the button
        if self.accent_type == "colour" and hover:
            _pygame.draw.rect(self.image, self.accent_value, self.image.get_rect())
        elif self.accent_type == "opacity" and hover: # no work :(
            _pygame.draw.rect(self.image, (self.colour[0], self.colour[1], self.colour[2], self.accent_value), self.image.get_rect())
        else:
            _pygame.draw.rect(self.image, self.colour, self.image.get_rect())
        # Draw the border
        _pygame.draw.rect(self.image, self.border_colour, self.image.get_rect(), self.border_width, self.border_radius)
        # Draw the text
        text_surface = self.text_font.render(self.text, True, self.text_colour)
        offset = (self.image.get_width()/2 - text_surface.get_width()/2, self.image.get_height()/2 - text_surface.get_height()/2)
        text_rect = text_surface.get_rect(topleft=offset)
        self.image.blit(text_surface, text_rect)

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
# Pygame
def draw_text(text, x, y, colour=BLACK, font=TEXT_FONT, line_spacing=5, surface=WINDOW, align="c"):
    lines = text.split("\n")
    for line in lines:
        text_surface = font.render(line, True, colour[:3])
        text_surface.set_alpha(colour[3] if len(colour) > 3 else 255)
        if align == "c":
            text_rect = text_surface.get_rect(center=(x, y))
        elif align == "r":
            text_rect = text_surface.get_rect(topright=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        surface.blit(text_surface, text_rect)
        y += text_surface.get_height() + line_spacing

# Normal
def save(user, stats:dict):
    pass

def load(user):
    pass

def back(current_screen):
    pass

# Main Loop ---------------------------------------------------------------------------------------------------------------------------------------

# Sprite Groups for buttons
# Example
welcome_page_buttons = _pygame.sprite.Group()
login_button = Button(400, 200, 400, 100, "Login", "Login Page")
signup_button = Button(400, 310, 400, 100, "Signup", "Signup Page")
anonymous_button = Button(400, 420, 400, 100, "Stay Anonymous", "Home")
test_button = Button(400, 530, 400, 100, "Test (Admin)", "Home")
welcome_page_buttons.add(login_button, signup_button, anonymous_button, test_button)

current_screen = "Welcome Page"

while True:
    clock.tick(FPS)
    WINDOW.fill(GREEN)

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
    if current_screen == "Welcome Page":
        # Draw a title
        draw_text("Big-o Animals", 400, 50, YELLOW, HEADING_FONT)
        draw_text("By Sean Chan", 400, 100, YELLOW, SUBTITLE_FONT)
        draw_text("Made using Pygame and VSC", 400, 130, YELLOW, TEXT_FONT)
        # Draw buttons
        welcome_page_buttons.update()

        # Change screen if a button is clicked
        button:Button
        for button in welcome_page_buttons:
            if button.check_click():
                current_screen = button.direct_to
    
    _pygame.display.update()