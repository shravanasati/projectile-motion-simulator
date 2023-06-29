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
FRAMERATE = 30
BALL_RADIUS = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion Simulator")


class Simulator:
    def __init__(
        self,
        initial_velocity: float,
        angle_of_projection: float,
        horizontal_acceleration: float = 0,
    ) -> None:
        self.engine = GroundToGround(
            initial_velocity, angle_of_projection, horizontal_acceleration
        )
        self.pos = 0
        self.trajectory = self.engine.trajectory(1 / FRAMERATE)

    @staticmethod
    def scale_coordinate(coordinate: tuple[int, int]):
        return (coordinate[0] + WIDTH / 10, (HEIGHT / 2) - coordinate[1])

    def draw(self, window) -> bool:
        try:
            coordinate = self.trajectory[self.pos]
            self.pos += 1
            pygame.draw.circle(
                window, Color.RED.value, self.scale_coordinate(coordinate), BALL_RADIUS
            )
            if len(self.trajectory[: self.pos]) > 2:
                pygame.draw.lines(
                    window,
                    Color.WHITE.value,
                    False,
                    tuple(map(self.scale_coordinate, self.trajectory[: self.pos])),
                    2,
                )
        except IndexError:
            return True


def main():
    running = True
    clock = pygame.time.Clock()
    sim = Simulator(100, 60, -1)

    while running:
        clock.tick(FRAMERATE)
        WINDOW.fill(Color.BLACK.value)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        finished = sim.draw(WINDOW)
        if finished:
            running = False
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
