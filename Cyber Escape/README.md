# 🛡️ CYBER ESCAPE // SECURITY BREACH

> **A neon-themed cybersecurity escape game built with Python and Pygame.**

**Cyber Escape // Security Breach** is an interactive 2D cybersecurity-themed game where the player must navigate through security environments, collect important items, avoid intelligent security bots, and reach the exit before the security system catches them.

The game combines **game development, pathfinding, cybersecurity concepts, and interactive UI design** into a single project.

---

## 🎮 Game Overview

You are inside a compromised cyber-security environment.

Your objective is simple:

**🔑 Find the key → 🛡️ Survive security bots → 🚪 Reach the exit → ⚡ Escape the system**

Each level becomes progressively more challenging, requiring faster movement and better decision-making.

The game features a futuristic **cyber/neon interface** designed to give the experience of a security operations terminal.

---

## ✨ Features

- 🔐 Cybersecurity-themed gameplay
- 🎮 Interactive keyboard controls
- 🤖 Security bots with **BFS pathfinding**
- 🗺️ Grid-based game environment
- 🔑 Key collection system
- 🚪 Locked exit system
- 🪙 Collectible coins
- 🛡️ Shield power-up
- ❤️ Multiple lives
- ⏱️ Level timer
- 📈 Score system
- ⚡ Particle effects
- 🌐 Multiple progressive levels
- ⏸️ Pause and resume system
- 🔄 Replay completed levels
- 🏆 Final victory screen
- 💀 Game-over screen
- 🎨 Neon cybersecurity interface
- 📊 High-score support

---

## 🤖 Artificial Intelligence

The security bots use **Breadth-First Search (BFS)** pathfinding to navigate the game grid.

The bots continuously calculate paths toward the player, creating a dynamic challenge.

### Simplified concept

```text
Player
  ↓
Security Grid
  ↓
BFS Pathfinding
  ↓
Security Bot
  ↓
Player Detection
```

This demonstrates how a classical AI search algorithm can be integrated into an interactive game.

---

## 🎯 Level System

The game contains **10 levels**.

As the player progresses, the challenge increases through changes in the game environment and security behavior.

After completing a level, the game pauses and displays:

```text
LEVEL 1 COMPLETED!

SECURITY NODE SUCCESSFULLY BREACHED

[R] REPLAY LEVEL
[ENTER] NEXT LEVEL
[ESC] MAIN MENU
```

The player can choose whether to replay the current level or continue.

After completing **Level 10**, the game displays the final victory screen.

---

## 🕹️ Controls

| Key | Action |
|---|---|
| `W` / `↑` | Move Up |
| `S` / `↓` | Move Down |
| `A` / `←` | Move Left |
| `D` / `→` | Move Right |
| `P` | Pause / Resume |
| `R` | Replay / Restart |
| `ENTER` | Continue to Next Level |
| `ESC` | Return to Main Menu |

---

## 🪙 Game Elements

### 🔑 Key
Collect the key to unlock the exit.

### 🚪 Exit
Reach the exit after collecting the required key to complete the level.

### 🪙 Coins
Collect coins to increase your score.

### 🛡️ Shield
Provides temporary protection against security threats.

### 🤖 Security Bots
AI-controlled enemies that use pathfinding to pursue the player.

### ❤️ Lives
The player has a limited number of lives. Avoid security bots and survive as long as possible.

---

## 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Main programming language |
| **Pygame** | Game development and graphics |
| **BFS** | Security bot pathfinding |
| **OOP / Functions** | Game architecture |
| **File Handling** | High-score storage |

---

## 📁 Project Structure

```text
Cyber-Escape/
│
├── Cyber_Escape_Level_Complete.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── screenshots/
    └── game.png
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/cyber-escape-security-breach.git
```

### 2. Open the project

```bash
cd cyber-escape-security-breach
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install Pygame directly:

```bash
pip install pygame
```

### 4. Run the game

```bash
python Cyber_Escape_Level_Complete.py
```

---

## 📦 Requirements

Create a `requirements.txt` file containing:

```text
pygame
```

---

## 🖥️ System Requirements

- Python 3.x
- Pygame
- Windows / Linux / macOS
- Keyboard
- Basic graphics support

---

## 🎮 Gameplay Flow

```text
          ┌──────────────┐
          │   MAIN MENU  │
          └──────┬───────┘
                 ↓
          ┌──────────────┐
          │   LEVEL 1    │
          └──────┬───────┘
                 ↓
        ┌──────────────────┐
        │ Find Key & Escape│
        └────────┬─────────┘
                 ↓
        ┌──────────────────┐
        │ LEVEL COMPLETED  │
        └───────┬──────────┘
                ↓
       ┌────────┴────────┐
       ↓                 ↓
    REPLAY           NEXT LEVEL
                         ↓
                    LEVEL 2
                         ↓
                        ...
                         ↓
                    LEVEL 10
                         ↓
                  🏆 VICTORY
```

---

## 🔐 Cybersecurity Theme

The project uses cybersecurity concepts as part of its game design.

The visual interface is inspired by:

- Security monitoring systems
- Cyber operation dashboards
- Network security environments
- System breach scenarios
- Threat detection interfaces

The project is designed primarily as an **educational game-development project** and does not perform real-world system intrusion.

---

## 🧩 Key Concepts Demonstrated

This project demonstrates practical implementation of:

- 🎮 Game loops
- 🧠 AI search algorithms
- 🔎 Breadth-First Search
- 🗺️ Grid traversal
- 💥 Collision detection
- ⏱️ Timers
- 🎯 Score management
- ❤️ Life management
- 🖥️ GUI design
- 🎨 Particle effects
- 📂 File handling
- ⌨️ Keyboard event handling
- 🔄 State management
- 🏆 Level progression

---

## 🚀 Future Improvements

Possible future versions could include:

- 🌐 Multiplayer mode
- 🧠 More advanced AI algorithms
- 🔊 Sound effects and background music
- 🎵 Dynamic cybersecurity alerts
- 🏅 Online leaderboard
- 💾 Save/load game progress
- 👤 Player customization
- 🗺️ More maps
- 🔥 Boss security levels
- 🌐 Network-based multiplayer
- 📱 Controller support

---

## 📸 Screenshots

Add your game screenshots inside the `screenshots` folder.

Example:

```text
screenshots/
├── main-menu.png
├── level-1.png
├── level-completed.png
└── victory.png
```

Then display them in this section:

```markdown
![Main Menu](screenshots/main-menu.png)

![Gameplay](screenshots/level-1.png)

![Level Completed](screenshots/level-completed.png)
```

---

## 👨‍💻 Author

**Your Name**

Cybersecurity / Computer Science Student

---

## ⭐ Project

If you find this project interesting, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is created for **educational and academic purposes**.

You may modify and improve the project for learning and personal development.