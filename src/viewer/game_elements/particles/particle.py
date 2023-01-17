import pygame


class Particle:
    def __init__(self, pos, color, size, duration, velocity):
        self.pos = pos
        self.color = color
        self.size = size
        self.duration = duration
        self.velocity = velocity

    def update(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])
        self.duration -= 1

    @property
    def is_expired(self):
        return self.duration <= 0

    def draw(self, particle_surface):
        pygame.draw.circle(particle_surface, self.color, self.pos, self.size)
        return particle_surface


class SquareParticle(Particle):
    def __init__(self, pos, color, size, duration, velocity):
        super().__init__(pos, color, size, duration, velocity)
        self.shape = "square"

    def draw(self, particle_surface):
        pygame.draw.rect(
            particle_surface,
            self.color,
            [
                self.pos[0] - (self.size / 2),
                self.pos[1] - (self.size / 2),
                self.pos[0] + (self.size / 2),
                self.pos[1] + (self.size / 2),
            ],
        )
        return particle_surface


class CircleParticle(Particle):
    def __init__(self, pos, color, size, duration, velocity):
        super().__init__(pos, color, size, duration, velocity)
        self.shape = "circle"

    def draw(self, particle_surface):
        pygame.draw.circle(particle_surface, self.color, self.pos, self.size)
        return particle_surface
