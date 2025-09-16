import socket
import threading
import json
import time

HOST = "127.0.0.1"
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Game server started on {HOST}:{PORT}")

players = {}  # Store player data: {conn: {"id": player_id, "x": x, "y": y, "animation": "idle"}}
player_counter = 0

def handle_client(conn, addr):
    global player_counter
    player_id = player_counter
    player_counter += 1
    
    # Initialize player
    players[conn] = {
        "id": player_id,
        "x": 100 + (player_id * 50),  # Spawn players at different positions
        "y": 100,
        "animation": "idle"
    }
    
    print(f"Player {player_id} connected from {addr}")
    
    # Send initial game state to new player
    send_game_state(conn)
    
    while True:
        try:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
                
            # Parse player update
            player_data = json.loads(data)
            players[conn].update(player_data)
            
            # Broadcast updated game state to all players
            broadcast_game_state()
            
        except Exception as e:
            print(f"Error handling player {player_id}: {e}")
            break
    
    # Remove player when disconnected
    if conn in players:
        del players[conn]
    conn.close()
    print(f"Player {player_id} disconnected")

def send_game_state(conn):
    """Send current game state to a specific client"""
    game_state = {
        "players": [player_data for player_data in players.values()]
    }
    try:
        conn.sendall(json.dumps(game_state).encode("utf-8"))
    except:
        pass

def broadcast_game_state():
    """Send game state to all connected clients"""
    game_state = {
        "players": [player_data for player_data in players.values()]
    }
    message = json.dumps(game_state)
    
    disconnected = []
    for conn in players:
        try:
            conn.sendall(message.encode("utf-8"))
        except:
            disconnected.append(conn)
    
    # Remove disconnected players
    for conn in disconnected:
        if conn in players:
            del players[conn]

while True:
    conn, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()