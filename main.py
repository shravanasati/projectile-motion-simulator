from enum import Enum
from projectile_motion import GroundToGround
import pygame


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (188, 39, 50)


pygame.init()

WIDTH, HEIGHT = 1000, 800
SCALEX, SCALEY = WIDTH, HEIGHT

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion Simulator")


class Simulator:
    pass
