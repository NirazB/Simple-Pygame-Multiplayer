from settings import *

# Defining a custom sprite group to handle all sprites with camera 
# Also it contains all sprites in the game (terrain, objects, player)
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface() # Get the main display surface i.e. the map terrain from the specified screen size
        self.offset = vector() #for postion offset

    def draw(self,player_center):
        # if screen size is 800*600 and player is at (400,300) then offset is -(400 - 800 / 2, 300 - 600 / 2) = -(0, 0)
        self.offset.x = -(player_center[0] - SCREEN_WIDTH / 2)
        self.offset.y = -(player_center[1] - SCREEN_HEIGHT / 2)

        for sprite in self:
            self.display_surface.blit(sprite.image,sprite.rect.topleft + self.offset)
