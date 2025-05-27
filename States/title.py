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
            "login": Button(400, 200, 400, 100, "Login"),
            "signup": Button(400, 310, 400, 100, "Signup"),
            "anonymous": Button(400, 420, 400, 100, "Stay Anonymous"),
            "test": Button(400, 530, 400, 100, "Test (Admin)")
        }

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
        surface.fill(GREEN)
        draw_text("Big-o Animals", 400, 50, surface, YELLOW, HEADING_FONT)
        draw_text("By Sean Chan", 400, 100, surface, YELLOW, SUBTITLE_FONT)
        draw_text("Made using Pygame and VSC", 400, 130, surface, YELLOW, TEXT_FONT)
        for button in self.buttons.values():
            button.draw(surface)