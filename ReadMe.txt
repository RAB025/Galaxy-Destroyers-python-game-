# 🚀 Space Invaders — Pygame Edition

A modern, feature-rich **Space Invaders–style arcade game** built using **Python and Pygame**, featuring menus, pause functionality, fullscreen support, sound controls, and responsive UI scaling.

This project demonstrates clean game architecture, state management, and interactive UI design using Pygame.

---

## 🎮 Features

- 🕹️ **Classic Space Invaders Gameplay**
- 📋 **Main Menu & Settings Screen**
- ⏸️ **Pause Menu (ESC key)**
- 🖱️ **Mouse-based UI buttons**
- 🔊 **Volume Slider for Background Music**
- 🖥️ **Borderless Fullscreen Support**
- 🔄 **Responsive UI & Sprite Positioning**
- ❌ **Custom Close Button**
- 🎵 Sound effects & background music

---

## 🧠 Game Architecture

The game uses a **state-based architecture**, keeping everything inside a **single main loop**, following Pygame best practices.

### Game States:
- `MENU` – Main menu with Play & Settings
- `SETTINGS` – Audio controls (volume slider)
- `GAME` – Core gameplay loop
- `PAUSE` – Pause overlay with Resume / Quit

This design makes the code easy to extend and maintain.

---

## 🖥️ Fullscreen & Scaling

- Uses **borderless fullscreen** (`pygame.NOFRAME`)
- Automatically adapts to **any screen resolution**
- Background, player, enemies, and UI elements scale dynamically
- Supports fast Alt-Tab and multi-monitor setups

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Library:** Pygame
- **Audio:** Pygame Mixer
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

