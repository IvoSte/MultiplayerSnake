class PowerUpViewBase:
    def __init__(self, screen, powerup):
        self.pos = powerup.pos
        self.image = None
        self.shape = None
        self.color = pygame.Color(0, 0, 0)

    def update(self):
        pass

    def draw(self):
        self.update()
        screen.blit(self.image)


class SpeedPowerUpView(PowerUpViewBase):
    def __init__(self, screen, powerup):
        super().__init__(screen)
        self.name = "speed"
        self.color = pygame.Color(255, 255, 0)
        self.shape = pygame.Rect(0, 0, 10, 10)
        self.image = pygame.Surface(self.shape.size)

    def update(self):
        pass

    def draw():
        pass
