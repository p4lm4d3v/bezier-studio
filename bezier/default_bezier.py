from src.colors import RED, BLACK
from src.point import Point
from src.lerp import lerp
from bezier.source_bezier import SourceBezier

from pygame import Surface


class DefaultBezier(SourceBezier):
    # Draw func
    def draw(self, surface: Surface) -> None:
        # The Bezier Curve
        n: int = 1000
        for t in range(0, n):
            t /= n
            c: Point = self.bezier_point(t, 1)
            c.draw(surface, BLACK)

        # [Start - Control 1] & [End - Control 2] Lines
        self.sc1_line(surface)
        self.ec2_line(surface)

        # Start & End Points
        self.start.draw(surface, RED)
        self.end.draw(surface, RED)

        # Control Points
        self.control1.draw(surface, RED)
        self.control2.draw(surface, RED)
