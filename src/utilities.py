"""Contains miscellaneous functions to communicate using sound and text."""
from pathlib import Path

import pygame

import constants


def play_sound(sound: str, volume: float = 0.5) -> None:
    """Plays the specified sound."""
    sound = pygame.mixer.Sound(Path.cwd() / 'src' / 'assets' / 'sounds' / f'{sound}.wav')
    sound.set_volume(volume)
    sound.play()


def get_font():
    return pygame.font.Font(Path.cwd() / 'src' / 'assets' / 'font.ttf', 48)


def make_centered_text(screen: pygame.Surface,
                       text: str,
                       center: tuple = (constants.SCREEN_WIDTH / 2, constants.OFFSET)) -> None:
    """Write text centered at a position."""
    font = get_font()
    title = font.render(text, True, constants.COLOR_FG)
    title_rect = title.get_rect(center=center)
    screen.blit(title, title_rect)


def make_aligned_text(screen: pygame.Surface, text: str, position: tuple) -> None:
    """Write text starting at a specified position."""
    font = get_font()
    text = font.render(text, True, constants.COLOR_FG)
    screen.blit(text, position)


def display_header(screen: pygame.Surface, header: str) -> None:
    """Flushes screen and displays the header."""
    screen.fill(constants.COLOR_BG)
    make_centered_text(screen, constants.TITLE)
    make_centered_text(screen, header, (constants.SCREEN_WIDTH / 2, 2 * constants.OFFSET))


def display_options(screen: pygame.Surface, options: list) -> None:
    """Display a list of numbered options."""
    for i, option in enumerate(options, 1):
        number_position = (constants.OFFSET, (2 + i) * constants.OFFSET)
        make_aligned_text(screen, f'{i}.', number_position)

        option_position = (constants.INDENT * constants.OFFSET, (2 + i) * constants.OFFSET)
        make_aligned_text(screen, option, option_position)


def display_controls(screen: pygame.Surface) -> None:
    """Display a menu of controls."""
    categories = {
        'LEFT PADDLE': ('MOVE UP: W', 'MOVE DOWN: S'),
        'RIGHT PADDLE': ('MOVE UP: I / UP', 'MOVE DOWN: K / DOWN'),
        'MENUS': ('MAIN MENU: ESC', 'NEW POINT: SPACE')
    }

    i = 3
    for category, controls in categories.items():
        make_aligned_text(screen, category, (constants.OFFSET, i * constants.OFFSET))
        for j, control in enumerate(controls, 1):
            make_aligned_text(screen, control, (constants.INDENT * constants.OFFSET, (i + j) * constants.OFFSET))
        i += 1 + j


def prompt_end_of_point(screen: pygame.Surface, rally_length: int, scores: dict) -> None:
    """Play a sound and display the score and a prompt to press space at the end of a point."""
    play_sound('end')
    make_centered_text(screen, f'RALLY LENGTH: {rally_length}',
                       (3 * constants.SCREEN_WIDTH / 4, constants.SCREEN_HEIGHT - constants.OFFSET))
    make_centered_text(screen, f'{scores["left"]} - {scores["right"]}',
                       (constants.SCREEN_WIDTH / 4, constants.SCREEN_HEIGHT - constants.OFFSET))
    pygame.display.update()
