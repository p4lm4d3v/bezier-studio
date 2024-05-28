from src.colors import RED, GREEN, BLUE, BLACK
from src.point import Point
from src.lerp import lerp
from bezier.source_bezier import SourceBezier

from pygame import Surface


class DebugBezier(SourceBezier):
    # Draw func
    def draw(self, surface: Surface, t: float) -> None:
        # Drawing Lines
        self.sc1_line(surface)
        self.ec2_line(surface)
        self.c1c2_line(surface)
        self.a1a2_line(surface, t)
        self.a2a3_line(surface, t)
        self.b1b2_line(surface, t)

        # [Start] & [End] Points
        self.start.draw(surface, RED)
        self.end.draw(surface, RED)

        # [Control 1] & [Control 2] Points
        self.control1.draw(surface, RED)
        self.control2.draw(surface, RED)

        # [a1] Point
        self.a1_point(t).draw(surface, GREEN)
        # [a2] Point
        self.a2_point(t).draw(surface, GREEN)
        # [a3] Point
        self.a3_point(t).draw(surface, GREEN)
        # [b1] Point
        self.b1_point(t).draw(surface, BLUE)
        # [b2] Point
        self.b2_point(t).draw(surface, BLUE)
        # [c1] Point
        self.bezier_point(t).draw(surface, BLACK)
