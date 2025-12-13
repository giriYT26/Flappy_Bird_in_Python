# 🐦 Flappy Bird in Python

A simple clone of the classic **Flappy Bird** game written in **Python using Pygame**. This project includes clean, beginner‑friendly game code along with sprite assets, sound effects, and a retro bitmap font for an authentic arcade feel.

> Play, flap, and try to beat your high score!

---

## 📑 Table of Contents

* [Demo](#demo)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Running the Game](#running-the-game)
* [Controls](#controls)
* [Project Structure](#project-structure)
* [Customization](#customization)
* [Contributing](#contributing)
* [Troubleshooting](#troubleshooting)
* [Notes About the Source](#notes-about-the-source)
* [License](#license)
* [Credits](#credits)

---

## 🎮 Demo

A short demo showcasing gameplay and controls:

```markdown
https://github.com/user-attachments/assets/bde74736-d4d3-408f-b830-bbd13676917a
```
---

## ✨ Features

* Classic Flappy Bird gameplay (tap/flap to stay airborne, avoid pipes)
* Score tracking system
* Retro bitmap font (**04B_19.TTF**)
* Sprite and audio assets included
* Simple, readable code — great for learning Pygame basics

---

## 🧰 Requirements

* Python **3.8+** (should also work on Python 3.7)
* Pygame

Install Pygame using pip:

```bash
pip install pygame
```

### Using a virtual environment (if u want)

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
pip install pygame
```

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/giriYT26/Flappy_Bird_in_Python.git
cd Flappy_Bird_in_Python
```

2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

---

## ▶️ Running the Game

From the project root directory, run:

```bash
python main.py
```

The game window will open and the main game loop will start automatically.

---

## 🎮 Controls

* **Spacebar** — Flap / Jump
* **Up Arrow** — Flap (alternative)
* **Mouse Left Click** — Flap (alternative)
* **Esc / Window Close** — Quit the game

---

## 🗂 Project Structure

```
Flappy_Bird_in_Python/
│
├── main.py            # Main game script (entry point)
├── sprites/            # Image assets (bird, pipes, background, base)
├── audio/              # Sound effects (wing, hit, point, etc.)
├── 04B_19.TTF          # Retro bitmap font
├── favicon.ico         # Repository icon
├── updates.txt         # Changelog / updates
```

---

## 🎨 Customization

You can easily tweak or expand the game:

* Replace images inside `sprites/` to change the look
* Add or replace sounds inside `audio/`
* Modify game constants in `main.py` (gravity, pipe gap, speed, spawn rate)
* Swap `04B_19.TTF` with another `.ttf` font by changing the font load section

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome!

**How to contribute:**

* Fork the repository
* Create a feature branch
* Commit your changes
* Open a pull request with a clear explanation

**Guidelines:**

* Keep changes focused and minimal
* Update the README if behavior changes
* Ensure the game runs on a clean Python + Pygame setup

---

## 🛠 Troubleshooting

* **Pygame import errors**: Ensure Pygame is installed in the correct Python environment
* **Blank window / freezes**: Run the game from a terminal to see error messages
* **Missing assets**: Verify that `sprites/` and `audio/` directories exist and are not renamed

When opening an issue, please include:

* Your OS
* Python version
* Pygame version
* Full error traceback

---

## 📝 Notes About the Source

This project is intended for **learning and educational purposes**. The code is kept simple and readable so beginners can understand game loops, events, collisions, and basic animations in Pygame.

---

## 📜 License

This project is released under the **MIT License** (for now).

---

## 🙏 Credits

* **Project Author**: giriYT26 (S Giridharan)
* **Original Flappy Bird Concept**: Dong Nguyen
* **Font**: 04B_19
* **Sprites & Audio**: Included in the repository (check individual files for attribution if sourced externally)

