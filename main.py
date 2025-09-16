import pygame
from player import Player, Player_movement

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
ANIMATION_SPEED = 200  # milliseconds between frames
MOVEMENT_SPEED = 5
BOUNDARY_BUFFER = 10  # How far outside screen player can go
PLAYER_SIZE = 48  # Player sprite size after scaling (24 * 2)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Player Animation")
clock = pygame.time.Clock()
running = True

# Initialize player and animations
player_instance = Player()
idle_frames = player_instance.get_idle_frames()
run_frames = player_instance.get_run_frames()

# Initialize player movement
player_movement = Player_movement(
    position=[100, 100],
    speed=MOVEMENT_SPEED,
    boundary_buffer=BOUNDARY_BUFFER,
    screen_width=SCREEN_WIDTH,
    screen_height=SCREEN_HEIGHT,
    player_size=PLAYER_SIZE
)
current_frame = 0
last_update = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle movement with boundary checking
    keys = pygame.key.get_pressed()
    is_moving = player_movement.move(keys)
    
    # Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= ANIMATION_SPEED:
        current_frame = (current_frame + 1) % len(run_frames if is_moving else idle_frames)
        last_update = current_time
    
    # Render
    screen.fill("gray")
    active_frames = run_frames if is_moving else idle_frames
    screen.blit(active_frames[current_frame], player_movement.position)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()