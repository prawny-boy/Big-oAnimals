from utility import convertFileName
import pygame as _pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SAVE_FILE = "user_stats.txt"
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
HEADING_FONT = _pygame.font.Font(convertFileName("Assets\\Fonts\\PixeloidSansBold.ttf"), 50)
SUBTITLE_FONT = _pygame.font.Font(convertFileName("Assets\\Fonts\\PixeloidMono.ttf"), 30)
TEXT_FONT = _pygame.font.Font(convertFileName("Assets\\Fonts\\PixeloidMono.ttf"), 20)
GAME_LOGO = _pygame.image.load(convertFileName("Assets\\Sprites\\logo.png"))
GAME_TITLE = _pygame.image.load(convertFileName("Assets\\Sprites\\title.png"))
ICON = _pygame.image.load(convertFileName("Assets\\Sprites\\icon.png"))

DEFAULT_USER = {
    "User Variables": {
        "Password": "",
        "Total Money": 0,
        "Player Experience": 0,
        "Campaign Stage Achieved": 0
    },
    "Items": {},
    "Upgrades": {},
    "Animals": {}
}