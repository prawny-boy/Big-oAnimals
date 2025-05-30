from States.state import State
from States.home import HomeState

from gui import Button, TextBox, draw_text, create_alert, alerts
from constants import *

class SignupState(State):
    def __init__(self, game):
        super().__init__(game)
        self.username_entry = TextBox("Username", 200, 210, 400, 40, 4, 20, colour=YELLOW)
        self.password_entry = TextBox("Password", 200, 260, 400, 40, 4, 20, colour=YELLOW)
        self.buttons = {
            "submit": Button(400, 420, 400, 100, "Submit"),
            "back": Button(65, 570, 90, 45, "Back", border_width=3),
            "next": Button(735, 570, 90, 45, "Next", True, border_width=3)
        }
    
    def update(self, delta_time, actions):
        self.password_entry.update(actions, delta_time)
        self.username_entry.update(actions, delta_time)
        if actions["mouse_click"]:
            if self.buttons["submit"].check_hover():
                username = self.username_entry.get_text()
                if not username:
                    return
                password = self.password_entry.get_text()
                if not password:
                    return
                elif username == password:
                    create_alert("Username and Password cannot be the same", 400, 200)
                elif self.game.user_exists(username):
                    create_alert("Username already exists in database", 400, 200)
                else:
                    self.game.signup_user(username)
                    HomeState(self.game).enter_state()
            elif self.buttons["back"].check_hover():
                self.exit_state()
    
    def render(self, surface):
        surface.fill(GREEN)
        self.password_entry.draw(surface)
        self.username_entry.draw(surface)
        alerts.update(surface)
        for button in self.buttons.values():
            button.draw(surface)
        draw_text("Signup Page", 400, 50, surface, YELLOW, HEADING_FONT)
