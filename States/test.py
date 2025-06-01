from States.state import State

from gui import Button, draw_text
from constants import *

class TestState(State):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = {
            "back": Button(65, 570, 90, 45, "Back", border_width=3),
            "next": Button(735, 570, 90, 45, "Next", True, border_width=3)
        }
        self.mouse_pos = (0, 0)
    
    def update(self, delta_time, actions):
        if actions["mouse_click"]:
            if self.buttons["back"].check_hover():
                self.exit_state()
        self.mouse_pos = actions["mouse_pos"]
    
    def render(self, surface):
        surface.fill(WHITE)
        draw_text("Test Page", 400, 50, surface, BLACK, HEADING_FONT)
        draw_text(f"Mouse pos: {self.mouse_pos}", 400, 300, surface, BLACK, TEXT_FONT)
        for button in self.buttons.values():
            button.draw(surface)