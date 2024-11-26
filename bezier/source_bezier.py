from lib.colors import BLACK
from lib.point import Point
from lib.lerp import lerp

from pygame import Surface
import pygame


class SourceBezier:
    def __init__(self, start: Point, end: Point, control1: Point, control2: Point):
        self.start = start
        self.end = end
        self.control1 = control1
        self.control2 = control2

    # Points
    def a1_point(self, t: float) -> Point:
        """Returns the lerped point from the [start] to [control1] points"""
        return Point(
            lerp(self.start.x, self.control1.x, t),
            lerp(self.start.y, self.control1.y, t)
        )

    def a2_point(self, t: float) -> Point:
        """Returns the lerped point from the [end] to [control2] points"""
        return Point(
            lerp(self.control1.x, self.control2.x, t),
            lerp(self.control1.y, self.control2.y, t)
        )

    def a3_point(self, t: float) -> Point:
        """Returns the lerped point from the [control1] to [control2] points"""
        return Point(
            lerp(self.control2.x, self.end.x, t),
            lerp(self.control2.y, self.end.y, t)
        )

    def b1_point(self, t: float) -> Point:
        return Point(
            lerp(self.a1_point(t).x, self.a2_point(t).x, t),
            lerp(self.a1_point(t).y, self.a2_point(t).y, t)
        )

    def b2_point(self, t: float) -> Point:
        return Point(
            lerp(self.a2_point(t).x, self.a3_point(t).x, t),
            lerp(self.a2_point(t).y, self.a3_point(t).y, t)
        )

    def bezier_point(self, t: float, r: float) -> Point:
        return Point(
            lerp(self.b1_point(t).x, self.b2_point(t).x, t),
            lerp(self.b1_point(t).y, self.b2_point(t).y, t),
            r=r
        )

    # Lines
    def sc1_line(self, surface: Surface) -> None:
        """START TO CONTROL 1 LINE"""
        pygame.draw.line(
            surface,
            start_pos=self.start.pos(),
            end_pos=self.control1.pos(),
            color=BLACK
        )

    def ec2_line(self, surface: Surface) -> None:
        """END TO CONTROL 2 LINE"""
        pygame.draw.line(
            surface,
            start_pos=self.end.pos(),
            end_pos=self.control2.pos(),
            color=BLACK
        )

    def c1c2_line(self, surface: Surface) -> None:
        """CONTROL 1 TO CONTROL 2 LINE"""
        pygame.draw.line(
            surface,
            start_pos=self.control1.pos(),
            end_pos=self.control2.pos(),
            color=BLACK
        )

    def a1a2_line(self, surface: Surface, t: float) -> None:
        """A1 TO A2 LINE"""
        pygame.draw.line(
            surface,
            start_pos=self.a1_point(t).pos(),
            end_pos=self.a2_point(t).pos(),
            color=BLACK
        )

    def a2a3_line(self, surface: Surface, t: float) -> None:
        """A2 TO A3 LINE"""
        pygame.draw.line(
            surface,
            start_pos=self.a2_point(t).pos(),
            end_pos=self.a3_point(t).pos(),
            color=BLACK
        )

    def b1b2_line(self, surface: Surface, t: float) -> None:
        """B1 TO B2 LINE"""
        pygame.draw.line(
            surface,
            start_pos=self.b1_point(t).pos(),
            end_pos=self.b2_point(t).pos(),
            color=BLACK
        )
