import socket
import threading
import json
from settings import *
from map import Map
from entities import Player

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Multiplayer Game")
clock = pygame.time.Clock()
running = True

# Initialize map and player
map_instance = Map()
player = map_instance.setup(map_instance.tmx_maps['world'], 'house')

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
                all_players = game_state.get("players", [])
                
                # If this is our first time receiving data, find our player ID
                if my_player_id is None and all_players:
                    my_player_id = all_players[-1]["id"]
                
                # Filter out our own player from other_players list
                other_players = [p for p in all_players if p["id"] != my_player_id]
                        
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

def send_player_data(x, y, animation):
    global last_sent_data
    if client_socket:
        try:
            player_data = {"x": x, "y": y, "animation": animation}
            if player_data != last_sent_data:
                client_socket.sendall(json.dumps(player_data).encode("utf-8"))
                last_sent_data = player_data.copy()
        except Exception as e:
            print(f"Error sending data: {e}")

# Try to connect to server
connected = connect_to_server()

while running:
    # Calculate delta time
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    map_instance.all_sprites.update(dt)
    
    # Send player data to server if connected
    if connected:
        send_player_data(
            player.rect.centerx, 
            player.rect.centery, 
            "run" if player.is_moving else "idle"
        )
    
    # Render
    screen.fill("gray")
    
    # Draw all sprites (includes map and player)
    map_instance.all_sprites.draw(player.rect.center)
    
    # Draw other players
    for other_player in other_players:
        x, y = other_player["x"], other_player["y"]
        is_running = other_player.get("animation") == "run"
        frames = player.run_frames if is_running else player.idle_frames
        frame_index = int(player.frame_index) % len(frames)
        
        # Calculate screen position using the same offset as main player
        offset = map_instance.all_sprites.offset
        screen_pos = vector(x, y) + offset
        screen.blit(frames[frame_index], screen_pos)
    
    pygame.display.flip()

# Cleanup
if client_socket:
    client_socket.close()
pygame.quit()