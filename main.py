from lib.colors import GREEN, RED, WHITE, BLACK
from bezier.default_bezier import DefaultBezier
from bezier.debug_bezier import DebugBezier
from lib.point import Point
from lib.clamp import clamp

from pygame import Surface
import pygame
import sys

# Pygame initialization
pygame.init()

# [Screen] properties
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bezier Studio")

# [Start Menu Buttons] properties
START_MENU_BUTTON_WIDTH: float = .3 * WIDTH
START_MENU_BUTTON_HEIGHT: float = 50
START_MENU_BUTTON_X = (WIDTH - START_MENU_BUTTON_WIDTH) / 2
START_MENU_BUTTON_Y = (HEIGHT - START_MENU_BUTTON_HEIGHT) / 2
DEFAULT_BEZIER_X_OFFSET = -30
DEBUG_BEZIER_X_OFFSET = 30

# [Back Button] properties
BACK_BUTTON_WIDTH = 100
BACK_BUTTON_HEIGHT = 40
BACK_BUTTON_X = 10
BACK_BUTTON_Y = 10

# [Reset Button] properties
RESET_BUTTON_WIDTH = 100
RESET_BUTTON_HEIGHT = 40
RESET_BUTTON_X = 10

# [Slider] properties
SLIDE_WIDTH = .65 * WIDTH
SLIDER_HEIGHT = 10
SLIDER_X = (WIDTH - SLIDE_WIDTH) / 2
SLIDER_Y = 440
SLIDER_COLOR = BLACK
t = 0.5

# [Handle] properties
HANDLE_WIDTH = 40
HANDLE_HEIGHT = 40
HANDLE_COLOR = RED

# [Default] & [Debug] Beziers setup
default_bezier = DefaultBezier(
    start=Point(2 / 8 * WIDTH, 4 / 6 * HEIGHT),
    end=Point(6 / 8 * WIDTH, 4 / 6 * HEIGHT),
    control1=Point(3 / 8 * WIDTH, 1 / 6 * HEIGHT),
    control2=Point(5 / 8 * WIDTH, 1 / 6 * HEIGHT),
)
debug_bezier = DebugBezier(
    start=Point(2 / 8 * WIDTH, 4 / 6 * HEIGHT),
    end=Point(6 / 8 * WIDTH, 4 / 6 * HEIGHT),
    control1=Point(3 / 8 * WIDTH, 1 / 6 * HEIGHT),
    control2=Point(5 / 8 * WIDTH, 1 / 6 * HEIGHT),
)


def draw_button(
        screen: Surface,
        background: tuple[float, float, float],
        foreground: tuple[float, float, float],
        x: float,
        y: float,
        width: float,
        height: float,
        text: str):
    """Draws a button of color [background] and on top of it text of color [foreground] with the given sizes"""
    pygame.draw.rect(screen, background, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, foreground)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)


def check_in_rectangle(mouse_pos: tuple[float, float], x: float, y: float, width: float, height: float) -> bool:
    """Checks if the given [mouse_pos] is in the given rectangle"""
    mouse_x, mouse_y = mouse_pos
    return x <= mouse_x <= x + width and y <= mouse_y <= y + height


def check_in_circle(mouse_pos: tuple[float, float], center: tuple[float, float], r: float) -> bool:
    """Checks if the given [mouse_pos] is inside the given cirle"""
    mouse_x, mouse_y = mouse_pos
    x, y = center
    d = pow(pow(mouse_x - x, 2) + pow(mouse_y - y, 2), 1/2)
    return d <= r


running: bool = True
current_screen: str = "home"

dragging_handle: bool = False
dragging_start: bool = False
dragging_control1: bool = False
dragging_control2: bool = False
dragging_end: bool = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if current_screen == "home":
                if check_in_rectangle(mouse_pos, START_MENU_BUTTON_X, START_MENU_BUTTON_Y + DEFAULT_BEZIER_X_OFFSET, START_MENU_BUTTON_WIDTH, START_MENU_BUTTON_HEIGHT):
                    current_screen = "bezier"
                elif check_in_rectangle(mouse_pos, START_MENU_BUTTON_X, START_MENU_BUTTON_Y + DEBUG_BEZIER_X_OFFSET, START_MENU_BUTTON_WIDTH, START_MENU_BUTTON_HEIGHT):
                    current_screen = "bezier_debug"
            elif current_screen in ["bezier", "bezier_debug"]:
                if check_in_rectangle(mouse_pos, BACK_BUTTON_X, BACK_BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT):
                    current_screen = "home"
                elif current_screen == "bezier_debug":
                    if check_in_rectangle(mouse_pos, SLIDER_X, SLIDER_Y - HANDLE_HEIGHT // 2, SLIDE_WIDTH, HANDLE_HEIGHT):
                        dragging_handle = True
                elif current_screen == "bezier":
                    r = default_bezier.start.r
                    if check_in_rectangle(mouse_pos, RESET_BUTTON_X, HEIGHT - 10 - RESET_BUTTON_HEIGHT, RESET_BUTTON_WIDTH, RESET_BUTTON_HEIGHT):
                        default_bezier = DefaultBezier(
                            start=Point(2 / 8 * WIDTH, 4 / 6 * HEIGHT),
                            end=Point(6 / 8 * WIDTH, 4 / 6 * HEIGHT),
                            control1=Point(3 / 8 * WIDTH, 1 / 6 * HEIGHT),
                            control2=Point(5 / 8 * WIDTH, 1 / 6 * HEIGHT),
                        )
                    elif check_in_circle(mouse_pos, default_bezier.start.pos(), r):
                        dragging_start = True
                    elif check_in_circle(mouse_pos, default_bezier.control1.pos(), r):
                        dragging_control1 = True
                    elif check_in_circle(mouse_pos, default_bezier.control2.pos(), r):
                        dragging_control2 = True
                    elif check_in_circle(mouse_pos, default_bezier.end.pos(), r):
                        dragging_end = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_handle = False
            dragging_start = False
            dragging_control1 = False
            dragging_control2 = False
            dragging_end = False
        elif event.type == pygame.MOUSEMOTION and dragging_handle:
            mouse_x, _ = event.pos
            handle_x = max(
                SLIDER_X,
                min(
                    mouse_x - HANDLE_WIDTH // 2,
                    SLIDER_X + SLIDE_WIDTH - HANDLE_WIDTH
                )
            )
            t = (handle_x - SLIDER_X) / (SLIDE_WIDTH - HANDLE_WIDTH)
        elif event.type == pygame.MOUSEMOTION and dragging_start:
            mx, my = event.pos
            r = default_bezier.start.r
            default_bezier.start = Point(
                clamp(mx, 0, WIDTH),
                clamp(my, 0, HEIGHT),
                r
            )
        elif event.type == pygame.MOUSEMOTION and dragging_control1:
            mx, my = event.pos
            r = default_bezier.control1.r
            default_bezier.control1 = Point(
                clamp(mx, 0, WIDTH),
                clamp(my, 0, HEIGHT),
                r
            )
        elif event.type == pygame.MOUSEMOTION and dragging_control2:
            mx, my = event.pos
            r = default_bezier.control2.r
            default_bezier.control2 = Point(
                clamp(
                    mx, 0, WIDTH), clamp
                (my, 0, HEIGHT), r)
        elif event.type == pygame.MOUSEMOTION and dragging_end:
            mx, my = event.pos
            r = default_bezier.end.r
            default_bezier.end = Point(
                clamp(mx, 0, WIDTH),
                clamp(my, 0, HEIGHT),
                r
            )

    screen.fill(WHITE)

    if current_screen == "home":
        draw_button(
            screen,
            BLACK,
            WHITE,
            START_MENU_BUTTON_X,
            START_MENU_BUTTON_Y + DEFAULT_BEZIER_X_OFFSET,
            START_MENU_BUTTON_WIDTH,
            START_MENU_BUTTON_HEIGHT,
            "Interactive"
        )
        draw_button(
            screen,
            BLACK,
            WHITE,
            START_MENU_BUTTON_X,
            START_MENU_BUTTON_Y + DEBUG_BEZIER_X_OFFSET,
            START_MENU_BUTTON_WIDTH, START_MENU_BUTTON_HEIGHT,
            "Preview"
        )
    elif current_screen == "bezier":

        default_bezier.draw(screen)
        draw_button(
            screen,
            RED,
            WHITE,
            BACK_BUTTON_X,
            BACK_BUTTON_Y,
            BACK_BUTTON_WIDTH,
            BACK_BUTTON_HEIGHT,
            "Back"
        )
        draw_button(
            screen,
            GREEN,
            WHITE,
            RESET_BUTTON_X,
            HEIGHT - 10 - RESET_BUTTON_HEIGHT,
            RESET_BUTTON_WIDTH,
            RESET_BUTTON_HEIGHT,
            "Reset"
        )
    elif current_screen == "bezier_debug":

        debug_bezier.draw(screen, t)
        draw_button(screen, RED, WHITE, 10, 10, 100, 40, "Back")

        pygame.draw.rect(
            screen,
            SLIDER_COLOR,
            (
                SLIDER_X,
                SLIDER_Y,
                SLIDE_WIDTH,
                SLIDER_HEIGHT
            )
        )
        handle_x = SLIDER_X + t * (SLIDE_WIDTH - HANDLE_WIDTH)
        pygame.draw.rect(
            screen,
            HANDLE_COLOR,
            (
                handle_x,
                SLIDER_Y - HANDLE_HEIGHT * .45,
                HANDLE_WIDTH,
                HANDLE_HEIGHT
            )
        )

        font = pygame.font.Font(None, 36)
        text_surface = font.render('0.0', True, BLACK)
        text_rect = text_surface.get_rect(
            center=(
                SLIDER_X - text_surface.get_width() * .6,
                SLIDER_Y + text_surface.get_height() * .25,
            )
        )
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"{round(t * 10) / 10}", True, WHITE)
        text_rect = text_surface.get_rect(
            center=(
                handle_x + HANDLE_WIDTH / 2,
                SLIDER_Y + text_surface.get_height() * .25,
            )
        )
        screen.blit(text_surface, text_rect)

        font = pygame.font.Font(None, 36)
        text_surface = font.render('1.0', True, BLACK)
        text_rect = text_surface.get_rect(
            center=(
                SLIDER_X + SLIDE_WIDTH + text_surface.get_width() * .7,
                SLIDER_Y + text_surface.get_height() * .25,
            )
        )
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
