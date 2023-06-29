from enum import Enum
import time
from projectile_motion import GroundToGround
import pygame


class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (188, 39, 50)
    YELLOW = (255, 255, 0)
    BLUE = (100, 149, 237)


pygame.init()

WIDTH, HEIGHT = 1200, 650
SCALEX = SCALEY = 1
FRAMERATE = 60
BALL_RADIUS = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projectile Motion Simulator")
FONT = pygame.font.SysFont("comicsans", 16)


class Simulator:
    def __init__(
        self,
        initial_velocity: float,
        angle_of_projection: float,
        horizontal_acceleration: float,
        show_text: bool,
    ) -> None:
        self.engine = GroundToGround(
            initial_velocity, angle_of_projection, horizontal_acceleration
        )
        self.show_text = show_text

        self.pos = 0
        self.trajectory = self.engine.trajectory(1 / FRAMERATE)

    def show_info(self, window):
        time_text = FONT.render(
            f"Time of Flight: {round(self.engine.time_of_flight, 2)}s", 1, Color.BLUE.value
        )
        range_text = FONT.render(f"Range: {round(self.engine.range, 2)}m", 1, Color.BLUE.value)
        hmax_text = FONT.render(
            f"Maximum Height: {round(self.engine.hmax, 2)}m", 1, Color.BLUE.value
        )

        texts = [time_text, range_text, hmax_text]
        centre = (WIDTH / 2, HEIGHT / 2)
        for i, text in enumerate(texts):
            window.blit(text, (centre[0], centre[1] + i * 15))

    @staticmethod
    def scale_coordinate(coordinate: tuple[int, int]):
        return (coordinate[0] * SCALEX, HEIGHT - (coordinate[1] * SCALEY))

    def draw(self, window) -> bool:
        try:
            coordinate = self.scale_coordinate(self.trajectory[self.pos])
            self.pos += 1

            # draw the ball
            pygame.draw.circle(window, Color.RED.value, (coordinate), BALL_RADIUS)

            # draw tracing lines
            if len(self.trajectory[: self.pos]) > 2:
                pygame.draw.lines(
                    window,
                    Color.WHITE.value,
                    False,
                    tuple(map(self.scale_coordinate, self.trajectory[: self.pos])),
                    2,
                )

            if not self.show_text:
                return False

            self.show_info(window)

            # draw distance and height
            height_text = FONT.render(
                f"Height: {((HEIGHT - coordinate[1]) / 1000):.2f}km",
                True,
                Color.YELLOW.value,
            )
            distance_text = FONT.render(
                f"Distance: {(coordinate[0]/1000):.2f}km", True, Color.YELLOW.value
            )
            window.blit(height_text, (coordinate[0] - 10, coordinate[1] - 35))
            window.blit(distance_text, (coordinate[0] - 10, coordinate[1] - 20))

        except IndexError:
            return True


def main():
    running = True
    clock = pygame.time.Clock()
    sim = Simulator(300, 30, 0, show_text=True)
    global SCALEX, SCALEY
    SCALEX = WIDTH / sim.engine.range
    SCALEY = HEIGHT / sim.engine.hmax
    print(sim.engine.time_of_flight)

    init = time.perf_counter()
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

    finish = time.perf_counter()
    print(finish - init)
    pygame.quit()


if __name__ == "__main__":
    main()
