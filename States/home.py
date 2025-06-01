from States.state import State

from gui import Button, draw_text
from constants import *

class HomeState(State):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = {
            "play": Button(400, 200, 200, 50, "Play"),
            "shop": Button(400, 280, 200, 50, "Shop"),
            "exit": Button(400, 360, 200, 50, "Exit")
        }
    
    def update(self, delta_time, actions):
        if actions["mouse_click"]:
            if self.buttons["play"].check_hover():
                pass
            elif self.buttons["shop"].check_hover():
                pass
            elif self.buttons["exit"].check_hover():
                self.game.signout_user()
                self.exit_state()

    def render(self, surface):
        surface.fill(WHITE)
        for button in self.buttons.values():
            button.draw(surface)
        draw_text("Home Page", 400, 50, surface, BLACK, HEADING_FONT)