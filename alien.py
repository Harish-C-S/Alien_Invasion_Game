import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class for single alien"""
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings

        # Load an image and set its rect attribute
        self.image=pygame.image.load('Resources\Alien_Book.bmp')
        self.rect=self.image.get_rect()

        #Starting each alien at the top left Corner of the Screen

        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        # Store the alien horizontal position
        self.x=float(self.rect.x)
    def check_edges(self):
        """Return true if the alien is the edge of the screen"""
        screen_rect=self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True
    
    def update(self):
        self.x+=(self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x=self.x