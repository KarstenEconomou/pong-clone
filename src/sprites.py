"""Contains game sprite classes."""
from random import choice

import pygame.sprite

import constants
from utilities import play_sound


def make_image(sprite: pygame.sprite.Sprite, color: tuple, width: int, height: int) -> None:
    """Initialize a sprite."""
    sprite.image = pygame.Surface((width, height))
    sprite.image.fill(constants.COLOR_BG)
    sprite.image.set_colorkey(constants.COLOR_BG)

    pygame.draw.rect(sprite.image, color, (0, 0, width, height))
    sprite.rect = sprite.image.get_rect()


class Paddle(pygame.sprite.Sprite):
    """Sprite representing a paddle that can be moved vertically."""
    def __init__(self, color: tuple, width: int, height: int, speed: int) -> None:
        super().__init__()
        make_image(self, color, width, height)

        self.speed = speed

    def move_up(self) -> None:
        """Move up."""
        self.rect.y -= self.speed

        # Stop paddle at upper bound
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self) -> None:
        """Move down."""
        self.rect.y += self.speed

        # Stop paddle at lower bound
        if self.rect.y > constants.SCREEN_HEIGHT - constants.PADDLE_HEIGHT:
            self.rect.y = constants.SCREEN_HEIGHT - constants.PADDLE_HEIGHT


class Velocity:
    """Describe the ball's velocity."""
    def __init__(self, speed: int) -> None:
        self.x = choice((-1, 1)) * speed
        self.y = choice((-1, 1)) * speed

    def flip_horizontal_direction(self) -> None:
        """Flips the horizontal component of velocity."""
        self.x *= -1

    def flip_vertical_direction(self) -> None:
        """Flips the vertical component of velocity."""
        self.y *= -1


class Ball(pygame.sprite.Sprite):
    """Sprite representing a ball."""
    def __init__(self, color: tuple, width: int, height: int, speed: int) -> None:
        super().__init__()
        make_image(self, color, width, height)

        self.velocity = Velocity(speed)

    def update(self) -> None:
        """Update position based on velocity."""
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def hit(self) -> None:
        """Update velocity on a paddle hit."""
        play_sound('hit')

        # Correct position to ensure no double hit
        if self.rect.x < constants.SCREEN_WIDTH / 2:
            # Hit on left side
            self.rect.x = constants.OFFSET + constants.PADDLE_WIDTH / 2
        else:
            # Hit on right side
            self.rect.x = constants.SCREEN_WIDTH - constants.OFFSET - constants.PADDLE_WIDTH / 2 - constants.BALL_SIZE

        self.velocity.flip_horizontal_direction()

    def bounce(self) -> None:
        """Update velocity on a vertical bound hit."""
        play_sound('bounce')
        self.velocity.flip_vertical_direction()

    def is_hit(self, paddle1: Paddle, paddle2: Paddle) -> bool:
        """Check if a collision with a paddle has occurred."""
        return self.rect.colliderect(paddle1.rect) or self.rect.colliderect(paddle2.rect)

    def is_bounced(self) -> bool:
        """Check if a collision with a vertical bound has occurred."""
        return self.rect.y >= constants.SCREEN_HEIGHT - constants.BALL_SIZE or self.rect.y <= 0
