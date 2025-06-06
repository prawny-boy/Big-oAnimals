from States.state import State
from States.home import HomeState

from gui import Button, TextBox, alerts, create_alert, draw_text
from constants import *

class LoginState(State):
    def __init__(self, game):
        super().__init__(game)
        self.username_entry = TextBox("Username", 200, 210, 400, 40, 4, 20, colour=BLACK)
        self.password_entry = TextBox("Password", 200, 260, 400, 40, 4, 20, password=True, colour=BLACK)
        self.buttons = {
            "back": Button(65, 570, 90, 45, "Back", border_width=3),
            "next": Button(735, 570, 90, 45, "Next", True, border_width=3),
            "submit": Button(400, 420, 200, 50, "Submit")
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
                if self.game.user_exists(username):
                    if self.game.get_user_password(username) == password:
                        self.game.login_user(username)
                        HomeState(self.game).enter_state()
                    else:
                        create_alert("Incorrect Password", 400, 200)
            elif self.buttons["back"].check_hover():
                self.exit_state()
    
    def render(self, surface):
        surface.fill(WHITE)
        self.password_entry.draw(surface)
        self.username_entry.draw(surface)
        alerts.update(surface)
        for button in self.buttons.values():
            button.draw(surface)
        draw_text("Login Page", 400, 50, surface, BLACK, HEADING_FONT)