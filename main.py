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
from collections import defaultdict

_pygame.init()
_pygame.font.init()

from sys import exit as _exit
from constants import *
from States.splash import SplashState, State
from filesave import FileSaveSystem

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
            "keys": defaultdict()
        }
        self.icons = [_pygame.transform.scale(GAME_LOGO, (200, 200))]

        # Game Variables
        self.stats = FileSaveSystem(SAVE_FILE, system_type="read-write", encoded=True)
        self.loaded_user = None
        self.user_stats = {}
        """
            Data for saving (add more as game grows):
                Total Money
                Player Experience
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
        for key, time in self.events["keys"].items():
            if time > 0:
                self.events["keys"][key] += 1
        for event in _pygame.event.get():
            if event.type == _pygame.QUIT:
                self.running = False
            elif event.type == _pygame.MOUSEBUTTONDOWN:
                self.events["mouse_click"] = True
            elif event.type == _pygame.MOUSEBUTTONUP:
                self.events["mouse_click"] = False
            elif event.type == _pygame.KEYDOWN:
                self.events["keys"][_pygame.key.name(event.key)] = 1
            elif event.type == _pygame.KEYUP:
                self.events["keys"][_pygame.key.name(event.key)] = 0
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
        self.events["keys"] = defaultdict()
    
    def user_exists(self, username):
        return self.stats.file_contains(username)

    def get_user_password(self, username):
        return self.stats.data[username]["User Variables"]["Password"]
    
    def signup_user(self, username, password):
        self.user_stats = DEFAULT_USER
        self.user_stats["User Variables"]["Password"] = password
        self.stats.data[username] = self.user_stats

    def login_user(self, username):
        self.loaded_user = username
        self.user_stats = self.stats.group_content(username)

if __name__ == "__main__":
    game = Game()
    splash_state = SplashState(game)
    splash_state.enter_state()
    game.state_stack.append(splash_state)
    
    # Start the game loop
    game.game_loop()

    game.stats.save()
    _pygame.quit()
    _exit()
