from src.colors import BLACK
from pygame import Surface
import pygame


class Point:
    def __init__(self, x: float, y: float, r: int = 5):
        self.x = x
        self.y = y
        self.r = r

    def draw(self, surface: Surface, color: tuple[float, float, float] = BLACK) -> None:
        pygame.draw.circle(surface, color, (self.x, self.y), self.r)

    def tuple(self) -> tuple[float, float]:
        return (self.x, self.y)
