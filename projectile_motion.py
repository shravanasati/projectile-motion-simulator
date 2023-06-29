from enum import Enum
import math


class Constant(Enum):
    g = 9.8  # m/s^2


class GroundToGround:
    def __init__(
        self,
        initial_velocity: float,
        angle_of_projection: float,
        horizontal_acceleration: float = 0,
    ) -> None:
        """
        Angle of projection must be in degrees.
        The other two parameters are in m/s and m/s^2 resp.
        """
        # convert angle into radians
        self.theta = angle_of_projection * math.pi / 180

        self.ux = initial_velocity * math.cos(self.theta)
        self.uy = initial_velocity * math.sin(self.theta)

        # acceleration due to gravity
        self.ay = -(Constant.g.value)
        self.ax = horizontal_acceleration

    @property
    def time_of_flight(self):
        return (2 * self.uy) / Constant.g.value

    @property
    def range(self) -> float:
        return (self.ux * self.time_of_flight) + (0.5 * self.ax * (self.time_of_flight**2))

    @property
    def hmax(self) -> float:
        return (self.uy**2) / (2 * Constant.g.value)


if __name__ == "__main__":
    g2g = GroundToGround(40, 50)
    print(g2g.range)
    print(g2g.hmax)
    print(g2g.time_of_flight)
