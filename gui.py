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
        border_colour:tuple = BLACK,
        text_colour:tuple = BLACK,
        text_font:_pygame.font.Font = TEXT_FONT,
        border_width:int = 5, # this is thickness of the border
        border_radius:int = -1, # this is curving of edges
        accent_type:str = "size", # 3 modes, colour, size and opacity
        accent_value:tuple|int = (1.2, 1.2) # this is the value of the accent, it can be a rgb value, size added (int) or the opacity of accented (int)
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

    def draw(self, surface: _pygame.Surface):
        hover = self.check_hover()
        if self.disabled:
            hover = False
        if self.accent_type == "size" and hover:
            size = (self.size[0] * self.accent_value[0], self.size[1] * self.accent_value[1])
        else:
            size = self.size
        self.image = _pygame.Surface(size)
        if self.disabled:
            self.image.set_alpha(128)
        if self.accent_type == "size" and hover:
            self.rect = self.image.get_rect(topleft=(self.coordinates[0]+(self.size[0]-size[0])/2, self.coordinates[1]+(self.size[1]-size[1])/2))
        else:
            self.rect = self.image.get_rect(topleft=self.coordinates)
        if self.accent_type == "colour" and hover:
            _pygame.draw.rect(self.image, self.accent_value, self.image.get_rect())
        elif self.accent_type == "opacity" and hover:  # no work :(
            _pygame.draw.rect(self.image, (self.colour[0], self.colour[1], self.colour[2], self.accent_value), self.image.get_rect())
        else:
            _pygame.draw.rect(self.image, self.colour, self.image.get_rect())
        _pygame.draw.rect(self.image, self.border_colour, self.image.get_rect(), self.border_width, self.border_radius)
        text_surface = self.text_font.render(self.text, True, self.text_colour)
        offset = (self.image.get_width() / 2 - text_surface.get_width() / 2, self.image.get_height() / 2 - text_surface.get_height() / 2)
        text_rect = text_surface.get_rect(topleft=offset)
        self.image.blit(text_surface, text_rect)
        # Blit the button onto the surface
        surface.blit(self.image, self.rect)

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
        self.rect = _pygame.rect.Rect(*self.coordinates, *self.dimensions)
        self.show_cursor = False
        self.cursor_timer = 0
    
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
    
    def update(self, actions:dict, delta_time:float):
        try:
            if actions["keys"]["left shift"] > 0 or actions["keys"]["right shift"] > 0:
                shift = True
            else:
                shift = False
        except KeyError:
            shift = False
        if self.selected:
            for key, time in actions["keys"].items():
                if time == 1 or time > 50:
                    if key == "backspace":
                        self.text = self.text[:-1]
                    elif key == "return" or key == "escape":
                        self.selected = False
                    elif key == "space":
                        self.text += " "
                    elif "shift" in key:
                        pass
                    else:
                        self.text += key.upper() if shift else key
        if actions["mouse_click"]:
            if self.rect.collidepoint(actions["mouse_pos"]):
                self.select()
            else:
                self.deselect()
        
        if self.selected:
            self.cursor_timer += delta_time
            if self.cursor_timer >= 0.5:  # Blinks every 0.5 seconds
                self.show_cursor = not self.show_cursor
                self.cursor_timer = 0

    def draw(self, surface:_pygame.Surface):
        display_text = self.prompt if self.text == "" else self.text
        if self.selected and self.show_cursor and not self.text == "":
            display_text += "|"
        text_surface = self.font.render(display_text, True, self.colour)
        text_width = text_surface.get_width()
        max_width = self.rect.width - 10
        while text_width > max_width and len(display_text) > 0:
            display_text = display_text[1:]
            text_surface = self.font.render(display_text, True, self.colour)
            text_width = text_surface.get_width()
        text_rect = text_surface.get_rect(left=self.rect.left + 5, top=self.rect.top + 5)
        border_thickness = 5 if self.selected else 2
        _pygame.draw.rect(surface, self.colour, self.rect, border_thickness)
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
