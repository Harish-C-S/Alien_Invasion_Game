import pygame
from pygame.sprite import Sprite   #Sprite is used to group the related items

class Bullet(Sprite):
    """To managae Bullets"""
    def __init__(self,ai_game):
        """Create a bullet at ship current position"""
        super().__init__()   #super is used to inherit from sprite
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.color=self.settings.bullet_color

        #Create a bullet rect at(0,0) and then set correct position
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop=ai_game.ship.rect.midtop

        #store bullet position as an decimal value

        self.y=float(self.rect.y)
    def update(self):
        self.y-=self.settings.bullet_speed  #update decimal position of the bullet
        self.rect.y=self.y                  #Update rect position
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
