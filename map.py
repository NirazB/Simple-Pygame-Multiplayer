from pytmx.util_pygame import load_pygame
import os
from settings import *
from sprites import Sprite
from entities import Player
from groups import AllSprites 

class Map:
    def __init__(self):
        self.tmx_maps = {'world': load_pygame(os.path.join('data', 'maps', 'world.tmx'))}
        self.all_sprites = AllSprites() # Group to hold all sprites

    def __str__(self):
        return f"Tile size: {self.tmx_maps['world'].tilewidth , self.tmx_maps['world'].tileheight}\n Tile count: {self.tmx_maps['world'].width , self.tmx_maps['world'].height} \nAll sprites: {self.all_sprites}"
    
    
    def setup(self,tmx_map,player_start_pos):
        # Terrain setup
        for x, y , surf in tmx_map.get_layer_by_name('Terrain').tiles():
            # 86 * 86 tiles count in terrain layer  = no . of sprites created
            Sprite((x*TILE_SIZE,y*TILE_SIZE),surf,self.all_sprites)

        # Objects setup
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x,obj.y),obj.image,self.all_sprites)

        # Entities setup
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos']=='house':
                self.player = Player((obj.x,obj.y),self.all_sprites)
        return self.player
