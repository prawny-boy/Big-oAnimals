from States.state import State
from States.title import TitleState

from gui import Button
from constants import *

class SplashState(State):
    def __init__(self, game):
        super().__init__(game)
        self.icon_idx = 0
        self.alpha = 0
        self.dir = "+"
        self.icon = self.game.icons[self.icon_idx]

    def update(self, delta_time, actions):
        if actions["mouse_click"]:
            self.dir = "-"
        
        if self.dir == "+":
            self.alpha += 2
            if self.alpha >= 300:
                self.dir = "-"
        else:
            self.alpha -= 2
            if self.alpha <= 0:
                self.icon_idx += 1
                if self.icon_idx < len(self.game.icons):
                    self.icon = self.game.icons[self.icon_idx]
                    self.dir = "+"
                else:
                    TitleState(self.game).enter_state()

    def render(self, surface):
        surface.fill(BLACK)
        self.icon.set_alpha(self.alpha)
        surface.blit(self.icon, (surface.get_width() / 2 - self.icon.get_width() / 2,
                                     surface.get_height() / 2 - self.icon.get_height() / 2))