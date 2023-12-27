from pygame import Rect
from random import randint, uniform

"""
params:

[mass] : massa della particella 
[vel_x] : velocità della particella lungo l'asse x
[vel_y] : velocità della particella lungo l'asse y
[color] : colore della particella (rgb)

"""


def get_random_color():
    return (68, randint(0, 255), randint(0, 255))


class Particle(Rect):
    K = 3

    MIN_MASS = 15
    MAX_MASS = 60

    MIN_VEL = 1
    MAX_VEL = 7

    def __init__(self, mass, vel_x, vel_y, rgb_color: tuple):
        self.mass = mass
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = rgb_color

        super().__init__(randint(1, 100), randint(1, 100), self.mass/self.K,
                         self.mass/self.K + (self.mass/self.MIN_MASS))

    def update_velocity(self, new_vel_x, new_vel_y):
        self.vel_x = new_vel_x
        self.vel_y = new_vel_y

    @classmethod
    def get_particle(cls):
        return Particle(randint(cls.MIN_MASS, cls.MAX_MASS), randint(cls.MIN_VEL, cls.MAX_VEL), randint(cls.MIN_VEL, cls.MAX_VEL), (get_random_color()))


def main():
    particle = Particle.get_particle()


if __name__ == '__main__':
    main()
