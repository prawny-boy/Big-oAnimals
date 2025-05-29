import pygame as _pygame
from constants import *

class Button(_pygame.sprite.Sprite):
    def __init__(
        self,
        x:int,
        y:int, 
        width:int, 
        height:int,
        text:str,
        disabled:bool = False,
        colour:tuple = WHITE, 
        border_colour:tuple = YELLOW,
        text_colour:tuple = BLACK,
        text_font:_pygame.font.Font = TEXT_FONT,
        border_width:int = 5, # this is thickness of the border
        border_radius:int = -1, # this is curving of edges
        accent_type:str = "colour", # 3 modes, colour, size and opacity
        accent_value:tuple|int = GREEN # this is the value of the accent, it can be a rgb value, size added (int) or the opacity of accented (int)
    ):
        super().__init__()
        offset = (width / 2, height / 2)
        self.coordinates = (x - offset[0], y - offset[1])
        self.size = (width, height)
        self.colour = colour
        self.text = text
        self.disabled = disabled
        self.text_colour = text_colour
        self.text_font = text_font
        self.border_colour = border_colour
        self.border_width = border_width
        self.border_radius = border_radius
        self.accent_type = accent_type
        self.accent_value = accent_value
    
    def check_hover(self):
        mouse_pos = _pygame.mouse.get_pos()
        button_rect = _pygame.rect.Rect(self.coordinates, self.size)
        if button_rect.collidepoint(mouse_pos):
            return True
        else:
            return False

    def draw(self, surface:_pygame.Surface):
        hover = self.check_hover()
        if self.accent_type == "size" and hover:
            self.image = _pygame.Surface((self.size[0]*self.accent_value, self.size[1]*self.accent_value))
        else:
            self.image = _pygame.Surface(self.size)
        if self.disabled:
            self.image.set_alpha(128)  # Set transparency for disabled buttons
            hover = False  # Disable hover effect for disabled buttons
        self.rect = self.image.get_rect(topleft = (self.coordinates))
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
        surface.blit(self.image, self.rect)
    
    def is_hovered(self):
        mouse_pos = _pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

class Alert(_pygame.sprite.Sprite):
    def __init__(self, text:str, x:int, y:int, colour:tuple = RED, font:_pygame.font.Font = TEXT_FONT):
        super().__init__()
        self.text = text
        self.coordinates = (x, y)
        self.colour = colour
        self.font = font
        self.alpha = 255
    
    def draw(self, surface):
        text_surface = self.font.render(self.text, True, self.colour)
        text_rect = text_surface.get_rect(center = self.coordinates)
        text_surface.set_alpha(self.alpha)
        surface.blit(text_surface, text_rect)
        self.alpha -= 5
    
    def update(self, surface):
        self.check_alpha()
        self.draw(surface)
    
    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

alerts = _pygame.sprite.Group()
def create_alert(text:str, x:int, y:int, colour:tuple = RED, font:_pygame.font.Font = TEXT_FONT):
    alert = Alert(text, x, y, colour, font)
    alerts.add(alert)

class TextBox(_pygame.sprite.Sprite):
    def __init__(self,
                 prompt:str,
                 x:int,
                 y:int,
                 width:int,
                 height:int,
                 min_characters:int = 0,
                 max_characters:int = 0,
                 colour:tuple = BLACK,
                 font:_pygame.font.Font = TEXT_FONT):
        super().__init__()
        self.prompt = prompt
        self.coordinates = (x, y)
        self.dimensions = (width, height)
        self.min_characters = min_characters
        self.max_characters = max_characters
        self.colour = colour
        self.font = font
        self.selected = False
        self.text = ""
    
    def deselect(self):
        self.selected = False
    def select(self):
        self.selected = True
    
    def get_text(self):
        if self.min_characters > 0:
            if len(self.text) < self.min_characters:
                create_alert(f"Not enough characters ({self.min_characters}-{self.max_characters})", 400, 200)
                return False
        if self.max_characters > 0:
            if len(self.text) > self.max_characters:
                create_alert(f"Too many characters ({self.min_characters}-{self.max_characters})", 400, 200)
                return False
        return self.text
    
    def update(self, actions:dict):
        mouse_pos = _pygame.mouse.get_pos()
        # add typing
        if actions["keys_pressed"]:
            pass
        if actions["mouse_click"]:
            if self.rect.collidepoint(mouse_pos):
                self.deselect()
            else:
                self.select()
    
    def draw(self, surface:_pygame.Surface):
        self.rect = _pygame.rect.Rect(*self.coordinates, *self.dimensions)
        if self.selected:
            text_surface = self.font.render(self.text, True, self.colour)
            text_rect = text_surface.get_rect(center = self.rect.center)
        else:
            text_surface = self.font.render(self.prompt, True, self.colour)
            text_rect = text_surface.get_rect(center = self.rect.center)
        _pygame.draw.rect(surface, self.colour, self.rect, 2)
        surface.blit(text_surface, text_rect)
                
def draw_text(text, x, y, surface:_pygame.Surface, colour=BLACK, font=TEXT_FONT, line_spacing=5, align="c"):
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
