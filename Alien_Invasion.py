############################################
# Harish C S
############################################
import sys #contains Exit function
from time import sleep       # To pause the game when the ships gets hitted
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    def __init__(self): #Initialize the game and create game resources   ---01---
        pygame.init()   #Initialize the pygame window
        self.settings=Settings()
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) 
        # We are passing the surface and it is updated by loop


        #self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.settings.screen_width=self.get_rect().width
        #self.settings.screen_height=self.get_rect().height
        #1000,680 define game dimensions #### 1200 width 800 height
        #is assigned in self.screen to be made available in all 
        

        pygame.display.set_caption("Aliens Invasion")
        #to store the game statistics
        self.stats=GameStats(self)
        self.ship=Ship(self) # Creating an instance of Ship class
        self.bullets=pygame.sprite.Group()  # Instance of Bullets
        self.aliens=pygame.sprite.Group()
        """  Sprite group is the collection of sprites that we can act at the same time"""

        self._create_fleet()

        self.bg_color=(230,230,0)  # Tuple used which is unmuttable
    #***************************************************************************************************
    def run_game(self):
        while 1:  # Start main loop for the game
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
                #print(len(self.bullets))
                self._update_screen()
    #******************************************************************************************************

    def _check_events(self):

        for event in pygame.event.get():   # event is declared to respond to the events that occur like pressing the keys
        #pygame.event.get()  to store the list of events and act accordinly
          if event.type==pygame.QUIT:  #if any event was to quit then sys.exit executed
            sys.exit()
          elif event.type==pygame.KEYDOWN:
              self._check_keydown_events(event)
          elif event.type==pygame.KEYUP: #KeyUp is used to know when the key is released
              self._check_keyup_events(event)

#*********************************************************************************************************
    def _check_keydown_events(self,event):

        if event.key==pygame.K_RIGHT:
                  #move to right
                  self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
                  self.ship.moving_left=True
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
        if event.key==pygame.K_RIGHT:
                  self.ship.moving_right=False  # is used to stop moving
        elif event.key==pygame.K_LEFT:
                  self.ship.moving_left=False


    def _fire_bullet(self):
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
#***************************************************************************************************
    def _create_fleet(self): 
        
               # To Create a Fleet of Aliens
        alien=Alien(self)      # To know the height and Width we create this
        alien_width,alien_height=alien.rect.size
        available_space_x=self.settings.screen_width-(2*alien_width) #Screen width minus two aliens width
        # We find the available space by screen width and 2* aliens width including the space provided
        number_aliens_x=available_space_x // (2*alien_width)  # Integer Division

        #Determine the number of rows aliens fit on the screen
        ship_height=self.ship.rect.height
        available_space_y=(self.settings.screen_height-(3*alien_height)-ship_height) #3 for space 1 from top 2 from bottom
        number_rows=available_space_y//(2*alien_height)

        #Create a Row of Aliens
        #Create a full fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                #create an alien place it in the row
                self._create_alien(alien_number,row_number)
    def _create_alien(self,alien_number,row_number):
        """Create an alien and place it in a row"""
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size
        alien.x=alien_width+2 *alien_width*alien_number # * 2 so as to give the space
        alien.rect.x=alien.x
        alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
        self.aliens.add(alien)
    """*****************************************************************"""
    def _ship_hit(self):
            """Response to the hit"""
            if self.stats.ships_left>0:
                #Decremeent the ships left
                self.stats.ships_left-=1
                #get rid of any remaining aliens and bullets
                self.aliens.empty()
                self.bullets.empty()

                #Create a new fleet and centre the ship

                self._create_fleet()
                self.ship.centre_ship()

                sleep(0.5) #To pause the game
            else:
                self.stats.game_active=False
    #*****************************************************************************************************
    def _check_aliens_bottom(self):
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                #Treat as the shiop got hit
                self._ship_hit()
                break
    def _update_aliens(self):
        """Update the positions of the aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        """To respond if the aliens reached the end"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entriee fleet and change the fleet directions"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _update_bullets(self):              # to get rid of old
        for bullet in self.bullets.copy():
                if bullet.rect.bottom<=0:
                    self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        #To check that have hit the aliens
    def _check_bullet_alien_collisions(self):
        collisions=pygame.sprite.groupcollide(self.bullets,self.aliens,1,True)
        if not self.aliens:
            #destroy bullet create a new fleet
            self.bullets.empty() # using empty method to remove the bullets
            self._create_fleet()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color) # To Fill
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip() # To Display the most recent screen

   
if __name__=='__main__':
    ai=AlienInvasion() # Making an game instance
    ai.run_game()