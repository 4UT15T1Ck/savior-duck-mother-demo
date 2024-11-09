import sys
import pygame
pygame.mixer.init()

class Sounds:

    def __init__(self) -> None:
        self.muted = False
        ext = "ogg"

        self.die = pygame.mixer.Sound(f"audio/die.{ext}")
        self.hit = pygame.mixer.Sound(f"audio/hit.{ext}")
        self.point = pygame.mixer.Sound(f"audio/point.{ext}")
        self.swoosh = pygame.mixer.Sound(f"audio/swoosh.{ext}")
        self.wing = pygame.mixer.Sound(f"audio/wing.{ext}")
        self.quack = pygame.mixer.Sound(f"audio/quack.mp3")
        self.chirp = pygame.mixer.Sound(f"audio/chirp.mp3")
        self.click = pygame.mixer.Sound(f"audio/click.mp3")
        self.set_vol()

    def set_vol(self):
        self.click.set_volume(1)
        self.chirp.set_volume(0.5)
        self.quack.set_volume(100)
        self.die.set_volume(0.2)
        self.hit.set_volume(0.1)
        self.point.set_volume(0.2)
        self.swoosh.set_volume(1)
        self.wing.set_volume(0.2)
        
    def mute(self):
        if self.muted:
            self.set_vol()
            self.muted = False
        else:
            self.click.set_volume(0)
            self.chirp.set_volume(0)
            self.quack.set_volume(0)
            self.die.set_volume(0)
            self.hit.set_volume(0)
            self.point.set_volume(0)
            self.swoosh.set_volume(0)
            self.wing.set_volume(0)
            self.muted = True