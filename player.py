import pygame

class Player():
    def __init__(self):
        self.image = pygame.image.load("./sprites/doux.png").convert_alpha()
        self.idle_frames = []
        self.run_frames = []
        
        self._load_frames()

    def _load_frames(self):
        # Load idle frames (frames 0-3)
        for i in range(4):
            frame = self._get_image(i, 24, 24)
            self.idle_frames.append(frame)
        
        # Load run frames (frames 4-7)
        for i in range(4, 8):
            frame = self._get_image(i, 24, 24)
            self.run_frames.append(frame)

    def _get_image(self, frame, width, height, scale=3, color=(0,0,0)):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.image, (0,0), ((frame*width), 0, width, height))
        image = pygame.transform.scale(image, (width*scale, height*scale))
        image.set_colorkey(color)  # Makes black transparent
        return image
    
    def get_idle_frames(self):
        return self.idle_frames

    def get_run_frames(self):
        return self.run_frames


class Player_movement():
    def __init__(self, position, speed, boundary_buffer, screen_width, screen_height, player_size):
        self.position = position
        self.speed = speed
        self.boundary_buffer = boundary_buffer
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_size = player_size

    def move(self, keys):
        is_moving = False
        
        if keys[pygame.K_LEFT] and self.position[0] > -self.boundary_buffer:
            self.position[0] -= self.speed
            is_moving = True
        if keys[pygame.K_RIGHT] and self.position[0] < self.screen_width - self.player_size + self.boundary_buffer:
            self.position[0] += self.speed
            is_moving = True
        if keys[pygame.K_UP] and self.position[1] > -self.boundary_buffer:
            self.position[1] -= self.speed
            is_moving = True
        if keys[pygame.K_DOWN] and self.position[1] < self.screen_height - self.player_size + self.boundary_buffer:
            self.position[1] += self.speed
            is_moving = True
        
        return is_moving