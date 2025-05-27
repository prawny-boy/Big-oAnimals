"""
Genre: Game, Fighting/Gambling
Author: Sean Chan
Visuals: Pygame/Python
Art Style: Pixel Art

Description:
Game where you use animals that you catch to fight levels of enemies.

Features:
- Catching animals
- Fighting enemies
    2 Modes: Campaign (with levels) and Challenge
- Money
- Upgrades (Shop)

Coding Conventions:
- Use snake_case for variable names, and all capitals for constants
- Use camelCase for function names
- Use PascalCase for class names
"""
import pygame as _pygame

_pygame.init()
_pygame.font.init()

from sys import exit as _exit
from constants import *
from States.splash import SplashState, State

class Game:
    def __init__(self):
        self.screen = _pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        _pygame.display.set_caption("Big-oAnimals")
        _pygame.display.set_icon(_pygame.transform.scale(ICON, (32, 32)))
        self.clock = _pygame.time.Clock()
        self.game_canvas = _pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.delta_time = 0
        self.state_stack:list[State] = []
        self.events = {
            "mouse_pos": _pygame.mouse.get_pos(),
            "mouse_click": False,
            "keys_pressed": _pygame.key.get_pressed(),
            "keys_released": []
        }
        self.icons = [_pygame.transform.scale(GAME_LOGO, (200, 200))]

        # Game Variables
        self.loaded_user = None
        """
            Data for saving (add more as game grows):
                Total Money
                Level of Player (Main Level/Exp)
                Campaign Stage Achieved
                Upgrades/Items (Type: Amount/Power)
                Animals (Animal Type: Level, Damage, Health, Speed etc.)

                Others:
                    Time Since Last Animal Catch
                    Last Time Played (Daily rewards?)
        """
    
    def game_loop(self):
        while self.running:
            self.get_delta_time()
            self.get_events()
            self.update()
            self.render()
    
    def get_delta_time(self):
        self.delta_time = self.clock.tick(FPS) / 1000
    
    def get_events(self):
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                self.running = False
            elif event.type == _pygame.MOUSEBUTTONDOWN:
                self.events["mouse_click"] = True
            elif event.type == _pygame.MOUSEBUTTONUP:
                self.events["mouse_click"] = False
            elif event.type == _pygame.KEYDOWN:
                self.events["keys_pressed"] = _pygame.key.get_pressed()
                print(self.events["keys_pressed"])
        self.events["mouse_pos"] = _pygame.mouse.get_pos()

    def update(self):
        self.state_stack[-1].update(self.delta_time, self.events)

    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        # Render current state to the screen
        self.screen.blit(_pygame.transform.scale(self.game_canvas, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        _pygame.display.flip()
    
    def reset_actions(self):
        self.events["mouse_click"] = False
        self.events["keys_released"] = []
        self.events["keys_pressed"] = []

if __name__ == "__main__":
    game = Game()
    splash_state = SplashState(game)
    splash_state.enter_state()
    game.state_stack.append(splash_state)
    
    # Start the game loop
    game.game_loop()

    _pygame.quit()
    _exit()

# # Splash Screen
# # Welcome Page

# # Login Page
# login_page = _pygame.sprite.Group()
# login_submit_button = Button(400, 420, 400, 100, "Login", "Home")
# login_page.add(login_submit_button)

# # Signup Page
# signup_page = _pygame.sprite.Group()
# signup_submit_button = Button(400, 420, 400, 100, "Submit", "Home")
# signup_page.add(signup_submit_button)

# # Username/Password Entry
# account_manager = _pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
# username_entry = _pygame_gui.elements.UITextEntryLine(_pygame.Rect(200, 210, 400, 40), manager=account_manager, object_id="#username_entry")
# password_entry = _pygame_gui.elements.UITextEntryLine(_pygame.Rect(200, 260, 400, 40), manager=account_manager, object_id="#password_entry")
# password_entry.set_text_hidden(True)
# password_entry.set_forbidden_characters(['|', '\\', ',', ' '])
# username_entry.set_forbidden_characters(['|', '\\', ',', ' '])

# current_screen = "Welcome Page"

# while True:
#     delta_time = CLOCK.tick(FPS)/1000
#     WINDOW.fill(GREEN)

#     for event in _pygame.event.get():
#         if event.type == _pygame.QUIT:
#             _exit()
#         elif event.type == _pygame.MOUSEBUTTONUP:
#             pass
#         elif event.type == _pygame.KEYDOWN:
#             key_pressed = _pygame.key.get_pressed()
#             if key_pressed[_pygame.K_ESCAPE]:
#                 current_screen = back(current_screen)
        
#         # Managers processing inputs
#         account_manager.process_events(event)
    
#     # Game Screens
#     if current_screen == "Welcome Page":

#         # Change screen if a button is clicked
#         current_screen = manage_buttons(welcome_page, current_screen)

#     if current_screen == "Test Page":
#         draw_text(f"Mouse pos: {_pygame.mouse.get_pos()}", 400, 300)

#         navigation_buttons.update()

#         current_screen = manage_buttons(navigation_buttons, current_screen, True, "Welcome Page")
#         button:Button
#         for button in navigation_buttons:
#             if button.check_click():
#                 if button.direct_to == "Back":
#                     current_screen = "Welcome Page"
    
#     if current_screen == "Login Page":
#         draw_text("Big-o Animals", 400, 50, YELLOW, HEADING_FONT)
#         draw_text("Login to your account", 400, 100, YELLOW, SUBTITLE_FONT)

#         account_manager.update(delta_time)
#         account_manager.draw_ui(WINDOW)
#         login_page.update()
#         navigation_buttons.update()
        
#         current_screen = manage_buttons([login_page, navigation_buttons], current_screen, True, "Welcome Page")

#         if current_screen == "Home":
#             username = username_entry.get_text()
#             password = password_entry.get_text()
#             details = get_all_details()

#             if username == "" or password == "":
#                 create_alert("Username and Password cannot be empty", 400, 200)
#                 current_screen = "Login Page"
#                 continue
#             if username not in details.keys():
#                 create_alert("Username does not exist in database", 400, 200)
#                 current_screen = "Login Page"
#                 continue
#             if details[username] != password:
#                 create_alert("Incorrect Password", 400, 200)
#                 current_screen = "Login Page"
#                 continue

#             load(username)
#             print("User logged in: "+username, password)

#     if current_screen == "Signup Page":
#         draw_text("Big-o Animals", 400, 50, YELLOW, HEADING_FONT)
#         draw_text("Signup to save your progress", 400, 100, YELLOW, SUBTITLE_FONT)

#         account_manager.update(delta_time)
#         account_manager.draw_ui(WINDOW)
#         signup_page.update()
#         navigation_buttons.update()

#         current_screen = manage_buttons([signup_page, navigation_buttons], current_screen, True, "Welcome Page")

#         if current_screen == "Home":
#             username = username_entry.get_text()
#             password = password_entry.get_text()
#             # users = list(get_all_details().keys())
#             users = ["sean"]

#             if username == "" or password == "":
#                 create_alert("Username and Password cannot be empty", 400, 200)
#                 current_screen = "Signup Page"
#                 continue
#             if username in users:
#                 create_alert("Username already exists in database", 400, 200)
#                 current_screen = "Signup Page"
#                 continue
#             if len(password) < 4:
#                 create_alert("Password must be at least 4 characters long", 400, 200)
#                 current_screen = "Signup Page"
#                 continue
#             if len(username) < 4 or len(username) > 20:
#                 create_alert("Username must be between 4 and 20 characters long", 400, 200)
#                 current_screen = "Signup Page"
#                 continue
#             if username == password:
#                 create_alert("Username and Password cannot be the same", 400, 200)
#                 current_screen = "Signup Page"
#                 continue

#             add_user(username)
#             print("User added: "+username.replace(" ", "."), password)
    
#     # Alerts
#     alerts.update()

#     # Update the display
#     _pygame.display.update()