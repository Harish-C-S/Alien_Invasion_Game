class GameStats:
    """Track statistics for the alien invasion"""
    def __init__(self,ai_game):
        """Intialise the statisticcs"""
        self.settings=ai_game.settings
        self.reset_stats()
        # Start game in-active state
        self.game_active=True # alien invasion in a n active state
    def reset_stats(self):  # only instance is to be created so most of the statistics are in the reset stats
        """Statistics that can change duiring the game"""
        self.ships_left=self.settings.ship_limit