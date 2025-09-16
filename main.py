import pygame
import socket
import threading
import json
from player import Player, Player_movement

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 720
FPS = 60
ANIMATION_SPEED = 200
MOVEMENT_SPEED = 5
BOUNDARY_BUFFER = 10
PLAYER_SIZE = 48

# Network configuration
HOST = "127.0.0.1"
PORT = 12345

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiplayer Game")
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

# Network variables
client_socket = None
other_players = []
my_player_id = None
last_sent_data = None

def connect_to_server():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        
        # Start receiving data in a separate thread
        receive_thread = threading.Thread(target=receive_game_data)
        receive_thread.daemon = True
        receive_thread.start()
        
        print("Connected to server!")
        return True
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return False

def receive_game_data():
    global other_players, my_player_id
    while running:
        try:
            data = client_socket.recv(1024).decode("utf-8")
            if data:
                game_state = json.loads(data)
                
                # Update other players' positions
                all_players = game_state.get("players", [])
                
                # If this is our first time receiving data, find our player ID
                if my_player_id is None and all_players:
                    # The last player in the list is usually the newest (us)
                    my_player_id = all_players[-1]["id"]
                    print(f"My player ID is: {my_player_id}")
                    
                
                # Filter out our own player from other_players list
                other_players = []
                for player_data in all_players:
                    if player_data["id"] != my_player_id:
                        other_players.append(player_data)
                        
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def send_player_data(x, y, animation):
    global last_sent_data
    if client_socket:
        try:
            player_data = {"x": x, "y": y, "animation": animation}
            
            # Only send if data has changed
            if player_data != last_sent_data:
                client_socket.sendall(json.dumps(player_data).encode("utf-8"))
                last_sent_data = player_data.copy()
        except Exception as e:
            print(f"Error sending data: {e}")

# Try to connect to server
connected = connect_to_server()

current_frame = 0
last_update = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle movement
    keys = pygame.key.get_pressed()
    is_moving = player_movement.move(keys)
    
    # Send player data to server
    if connected:
        animation_state = "run" if is_moving else "idle"
        send_player_data(player_movement.position[0], player_movement.position[1], animation_state)
    
    # Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= ANIMATION_SPEED:
        current_frame = (current_frame + 1) % len(run_frames if is_moving else idle_frames)
        last_update = current_time
    
    # Render
    screen.fill("gray")
    
    # Draw our player
    active_frames = run_frames if is_moving else idle_frames
    screen.blit(active_frames[current_frame], player_movement.position)
    
    # Draw other players
    for other_player in other_players:
        other_animation = other_player.get("animation", "idle")
        other_frames = run_frames if other_animation == "run" else idle_frames
        # Use current_frame for simplicity (in production, each player should have their own frame counter)
        frame_index = current_frame % len(other_frames)
        screen.blit(other_frames[frame_index], (other_player["x"], other_player["y"]))
    
    pygame.display.flip()
    clock.tick(FPS)

# Cleanup
if client_socket:
    client_socket.close()
pygame.quit()