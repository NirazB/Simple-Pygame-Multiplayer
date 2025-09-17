from settings import *
import os

# sprite containing the player with movement and animation
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # Load sprite sheet
        self.sprite_sheet = pygame.image.load(os.path.join("sprites", "doux.png")).convert_alpha()
        
        # Animation frames
        self.idle_frames = []
        self.run_frames = []
        self._load_frames()
        
        # Set initial image and rect
        self.frame_index = 0
        self.image = self.idle_frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movement
        self.direction = vector()

        self.is_moving = False

    def _get_image(self, frame, width=24, height=24, scale=3, color=(0,0,0)):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sprite_sheet, (0,0), ((frame*width), 0, width, height))
        image = pygame.transform.scale(image, (width*scale, height*scale))
        image.set_colorkey(color)
        return image

    def _load_frames(self):
        # Load idle frames (frames 0-3)
        for i in range(4):
            frame = self._get_image(i)
            self.idle_frames.append(frame)
        
        # Load run frames (frames 4-7)
        for i in range(4, 8):
            frame = self._get_image(i)
            self.run_frames.append(frame)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt * 60  # Multiply by 60 to normalize for 60 FPS
        
        animation_list = self.run_frames if self.is_moving else self.idle_frames
        
        # Loop animation
        if self.frame_index >= len(animation_list):
            self.frame_index = 0
            
        # Set image
        self.image = animation_list[int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()
        
        if keys[pygame.K_UP]:
            input_vector.y = -1
        if keys[pygame.K_DOWN]:
            input_vector.y = 1
        if keys[pygame.K_LEFT]:
            input_vector.x = -1
        if keys[pygame.K_RIGHT]:
            input_vector.x = 1

        # Normalize diagonal movement
        if input_vector.magnitude() > 0:
            self.direction = input_vector.normalize()
            self.is_moving = True
        else:
            self.direction = input_vector
            self.is_moving = False

    def move(self, dt):
        self.rect.center += self.direction * SPEED * dt
     
    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)