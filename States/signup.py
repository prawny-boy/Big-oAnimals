from States.state import State
from States.home import HomeState

from gui import Button, TextBox, draw_text, create_alert, alerts
from constants import *

class SignupState(State):
    def __init__(self, game):
        super().__init__(game)
        self.username_entry = TextBox("Username", 200, 210, 400, 40, 4, 20)
        self.password_entry = TextBox("Password", 200, 260, 400, 40, 4, 20)
        self.submit_button = Button(400, 420, 400, 100, "Submit")
    
    def update(self, delta_time, actions):
        if actions["mouse_click"]:
            if self.submit_button.check_hover():
                username = self.username_entry.get_text()
                password = self.password_entry.get_text()
                if not username or not password:
                    return
                elif username == password:
                    create_alert("Username and Password cannot be the same", 400, 200)
                elif self.game.user_exists(username):
                    create_alert("Username already exists in database", 400, 200)
                else:
                    self.game.add_user(username)
                    HomeState(self.game).enter_state()
    
    def render(self, surface):
        surface.fill(GREEN)
        self.submit_button.draw(surface)
        self.password_entry.draw(surface)
        self.username_entry.draw(surface)
        alerts.update(surface)
        draw_text("Signup Page", 400, 50, surface, YELLOW, HEADING_FONT)
