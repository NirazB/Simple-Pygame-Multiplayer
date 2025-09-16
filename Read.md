# Multiplayer Pygame Project
-A real-time multiplayer 2D game built with Python using Pygame for the client and socket programming for networking.

## Features
- Real-time multiplayer**: Multiple players can connect and play simultaneously
- Animated sprites**: Players have idle and running animations
- Smooth movement**: Arrow key controls with boundary checking
- Client-server architecture**: Dedicated server handles game state synchronization

## Screenshots
-Players can see each other move in real-time with synchronized animations.

## Requirements
- Python 3.7+
- Pygame
- Socket (built-in)
- Threading (built-in)
- JSON (built-in)

## Installation
1. Clone or download this project
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Ensure you have the sprite file at `./sprites/doux.png`

## How to Run
### 1. Start the Server
```bash
cd "project 1"
python server.py
```
You should see: `Game server started on 127.0.0.1:12345`
### 2. Start Client(s)
In separate terminal windows:
```bash
cd "project 1"
python main.py
```
## Controls
- **Arrow Keys**: Move your player
- **Close Window**: Disconnect from game

### Data Flow
```
Client 1 → Server → All Clients (including Client 1)
Client 2 → Server → All Clients (including Client 2)
```

### Network Protocol

**Client to Server:**
```json
{"x": 150, "y": 200, "animation": "run"}
```

**Server to Clients:**
```json
{
  "players": [
    {"id": 0, "x": 150, "y": 200, "animation": "run"},
    {"id": 1, "x": 300, "y": 100, "animation": "idle"}
  ]
}
```

## Future Improvements

- [ ] Add player names/colors
- [ ] Implement lag compensation
- [ ] Add game rooms/lobbies  
- [ ] Create a more robust player ID system
- [ ] Add sound effects
- [ ] Implement collision detection
- [ ] Add chat functionality

