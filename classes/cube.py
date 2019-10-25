import pygame
from math import sin, cos, radians

class Cube:
    def __init__(self, pos, color):
        self.x, self.y, self.width, self.height = pos
        self.color = color

        self.x_vel = 0
        self.y_vel = 0
        self.vel = 0

    def get_center(self):
        return self.x + (self.width / 2), self.y + (self.height / 2)

    def calculate_distance(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
