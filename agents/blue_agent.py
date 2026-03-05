class BlueCircle:
    def __init__(self, width, height):
        self.x = 100
        self.y = height // 3
        self.radius = 30
        self.color = (0, 0, 255)
        self.speed = 3
        self.direction = -1
        self.width = width

    def update(self):
        self.x += self.speed * self.direction
        if self.x + self.radius >= self.width or self.x - self.radius <= 0:
            self.direction *= -1

    def draw(self, surface):
        import pygame
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)