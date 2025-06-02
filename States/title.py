from States.state import State
from States.login import LoginState
from States.signup import SignupState
from States.home import HomeState
from States.test import TestState

from gui import Button, draw_text
from constants import *

class TitleState(State):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = {
            "login": Button(400, 250, 200, 50, "Login"),
            "signup": Button(400, 330, 200, 50, "Signup"),
            "anonymous": Button(400, 410, 200, 50, "Stay Anonymous"),
            "test": Button(400, 490, 200, 50, "Test (Admin)")
        }
        self.title_hovered = False

    def update(self, delta_time, actions):
        if actions["mouse_click"]:
            if self.buttons["login"].check_hover():
                LoginState(self.game).enter_state()
            elif self.buttons["signup"].check_hover():
                SignupState(self.game).enter_state()
            elif self.buttons["anonymous"].check_hover():
                HomeState(self.game).enter_state()
            elif self.buttons["test"].check_hover():
                TestState(self.game).enter_state()

    def render(self, surface):
        surface.fill(WHITE)
        surface.blit(GAME_TITLE, (surface.get_width() / 2 - GAME_TITLE.get_width() / 2, 20))
        # draw_text("Big-o Animals", 400, 50, surface, BLACK, HEADING_FONT)
        # draw_text("By Sean Chan", 400, 100, surface, BLACK, SUBTITLE_FONT)
        # draw_text("Made using Pygame and VSC", 400, 130, surface, BLACK, TEXT_FONT)
        for button in self.buttons.values():
            button.draw(surface)