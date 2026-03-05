# agents/circle_agent.py
class CircleAgent:
    def __init__(self, width, height):
        self.x = 50
        self.y = height // 2
        self.radius = 50
        self.color = (255, 0, 0)
        self.speed = 0
        self.direction = 1
        self.width = width
        self.height = height

    def update(self):
        self.x += self.speed * self.direction
        if self.x + self.radius >= self.width or self.x - self.radius <= 0:
            self.direction *= -1

    def draw(self, surface):
        import pygame
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)