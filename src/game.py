"""Begins and operates game."""
import sys
from pathlib import Path
from random import uniform
from typing import Callable
from webbrowser import open

import pygame

import constants
import utilities
from sprites import Ball, Paddle

rally_length = 0
difficulty = 1


def make_window() -> pygame.Surface:
    """Make the window that the game is played in"""
    pygame.display.set_caption(constants.TITLE.title())
    pygame.display.set_icon(pygame.image.load(Path.cwd() / 'src' / 'assets' / 'images' / 'icon.png'))
    return pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))


def show_menu() -> None:
    """Show a new menu."""
    pygame.display.update()
    utilities.play_sound('interact')
    pygame.time.wait(constants.WAIT_TIME)


def loop(process: Callable) -> Callable:
    """Wrap the given process in a loop that looks for the game still being run."""
    def stay_on_screen() -> bool:
        """Check if window has been closed or user has requested to return to main menu."""
        for event in pygame.event.get():
            # Check if window is open
            if event.type == pygame.QUIT:
                return False
            # Check for return to main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main()
        return True

    def quit_game() -> None:
        """Quit game and program."""
        pygame.display.quit()
        sys.exit()

    def wrapper():
        """Continue process if window has not been closed and main menu has not been returned to."""
        while stay_on_screen():
            process()
        quit_game()
    return wrapper


def make_default_sprites() -> pygame.sprite.Group:
    """Set sprites to default state."""
    def make_sprites(paddle_speed: int, ball_speed: int) -> pygame.sprite.Group:
        """Create all game sprites at default positions."""

        # Define paddles
        def make_paddle(speed: int) -> Paddle:
            """Create a paddle sprite at default position."""
            paddle = Paddle(constants.COLOR_FG, constants.PADDLE_WIDTH, constants.PADDLE_HEIGHT, speed)
            paddle.rect.centery = constants.SCREEN_HEIGHT / 2
            return paddle

        paddle_left = make_paddle(paddle_speed)
        paddle_left.rect.centerx = constants.OFFSET

        paddle_right = make_paddle(paddle_speed)
        paddle_right.rect.centerx = constants.SCREEN_WIDTH - constants.OFFSET

        # Define ball
        ball = Ball(constants.COLOR_FG, constants.BALL_SIZE, constants.BALL_SIZE, ball_speed)
        ball.rect.centerx = constants.SCREEN_WIDTH / 2
        ball.rect.centery = uniform(constants.SCREEN_HEIGHT / 10, 9 * constants.SCREEN_HEIGHT / 10)

        return pygame.sprite.Group(paddle_left, paddle_right, ball)

    if difficulty == 2:
        sprite_group = make_sprites(constants.PADDLE_SPEED_HARD, constants.BALL_SPEED_HARD)
    else:
        sprite_group = make_sprites(constants.PADDLE_SPEED_STD, constants.BALL_SPEED_STD)

    return sprite_group


def end_point(screen: pygame.Surface, scores: dict, winner: str) -> None:
    """Show score and rally length at the end of a point."""
    scores[winner] += 1
    utilities.prompt_end_of_point(screen, rally_length, scores)

    @loop
    def request_input():
        """Check for specific user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start_point(screen, scores)
    request_input()


def draw_screen(screen: pygame.Surface, sprite_group: pygame.sprite.Group) -> None:
    """Draws elements on screen."""
    # Draw background
    screen.fill(constants.COLOR_BG)

    # Draw net
    pygame.draw.line(surface=screen,
                     color=constants.COLOR_FG,
                     start_pos=(constants.SCREEN_WIDTH / 2, 0),
                     end_pos=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT),
                     width=constants.NET_WIDTH,
                     )

    # Handle sprites
    sprite_group.draw(screen)
    sprite_group.update()

    pygame.display.update()


def start_point(screen: pygame.Surface, scores: dict) -> None:
    # Initialize sprites
    sprite_group = make_default_sprites()
    paddle_left, paddle_right, ball = sprite_group

    draw_screen(screen, sprite_group)
    utilities.play_sound('start')
    pygame.time.wait(constants.WAIT_TIME)

    global rally_length
    rally_length = 0

    @loop
    def game() -> None:
        draw_screen(screen, sprite_group)

        # Move paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle_left.move_up()
        elif keys[pygame.K_s]:
            paddle_left.move_down()
        if keys[pygame.K_UP] or keys[pygame.K_i]:
            paddle_right.move_up()
        elif keys[pygame.K_DOWN] or keys[pygame.K_k]:
            paddle_right.move_down()

        # Check for ball being hit by paddle
        if ball.is_hit(paddle_left, paddle_right):
            ball.hit()
            global rally_length
            rally_length += 1

        # Check for ball colliding with vertical bounds
        if ball.is_bounced():
            ball.bounce()

        # Check for ball colliding with horizontal bounds
        if ball.rect.x >= constants.SCREEN_WIDTH - constants.BALL_SIZE:
            # Left wins
            end_point(screen, scores, 'left')
        elif ball.rect.x <= 0:
            # Right wins
            end_point(screen, scores, 'right')
    game()


def create_game(screen: pygame.Surface):
    """Begin clock and start the first point of the game."""
    def initialize_clock() -> None:
        """Define the game clock."""
        clock = pygame.time.Clock()
        clock.tick(constants.FPS)

    initialize_clock()
    start_point(screen, {'left': 0, 'right': 0})


def open_difficulty_select_menu(screen: pygame.Surface) -> None:
    """Create a difficulty selection menu and capture input."""
    # Write text
    utilities.display_header(screen, 'SELECT DIFFICULTY')
    utilities.display_options(screen, ['STANDARD', 'Nadal ON CLAY'])
    show_menu()

    @loop
    def request_input() -> None:
        """Check for specific user input."""
        global difficulty

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            difficulty = 1
            create_game(screen)
        elif keys[pygame.K_2]:
            difficulty = 2
            create_game(screen)
    request_input()


def open_controls_menu(screen: pygame.Surface) -> None:
    """Show game controls."""
    # Write text
    utilities.display_header(screen, 'CONTROLS')
    utilities.display_controls(screen)
    show_menu()

    def wait(): pass
    loop(wait)


def open_about_menu(screen: pygame.Surface) -> None:
    """Show an about menu with web url."""
    # Write text
    utilities.display_header(screen, 'ABOUT')
    utilities.display_options(screen, ['github.com/karsteneconomou/pong-clone'])
    show_menu()

    @loop
    def request_input() -> None:
        """Check for specific user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            open('https://github.com/karsteneconomou', new=2)
    request_input()


def open_main_menu(screen: pygame.Surface) -> None:
    """Create the main menu and allow navigation to other menus."""
    # Write text
    utilities.display_header(screen, 'BY Karsten Economou')
    utilities.display_options(screen, ['PLAY', 'CONTROLS', 'ABOUT'])
    show_menu()

    @loop
    def request_input() -> None:
        """Check for specific user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            open_difficulty_select_menu(screen)
        elif keys[pygame.K_2]:
            open_controls_menu(screen)
        elif keys[pygame.K_3]:
            open_about_menu(screen)
    request_input()


def main() -> None:
    """Set window at the main menu."""
    pygame.init()
    screen = make_window()
    open_main_menu(screen)


if __name__ == '__main__':
    main()
