# Strathmore Roundup

**Strathmore Roundup** is a 2D arcade-style game built with Python and Pygame. The deer have escaped from Strathmore Castle, and it's up to you to herd them back to safety using the sheer computing presence of a Nexus server!

## 🎮 Gameplay

### Objective
The goal is to herd 15 deer per level back into **Strathmore Castle**, located in the top-left area of the screen.

*   **Herd:** Move your Nexus server close to the deer to scare them in the opposite direction.
*   **Catch:** Guide them into the top-left "safe zone" to catch them.
*   **Avoid Loss:** If a deer runs off the screen boundaries, it is "lost" forever.

### Progression
Your performance determines your hardware upgrades:
*   **Catch 8+ Deer:** Advance to the next level and upgrade your Nexus server (Visual upgrade: PMEC -> 3-Rack -> 10-Rack).
*   **Catch 5-7 Deer:** Advance to the next level with no upgrade.
*   **Catch < 5 Deer:** Game Over.

### Controls
*   **Arrow Keys:** Move the Nexus server (Up, Down, Left, Right).
*   **Enter / Left Click:** Navigate menus and splash screens.
*   **Esc / Q:** Quit the game.

## 🛠️ Installation & Running

### Prerequisites
*   Python 3.8+
*   pip

### Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/strathmore-roundup.git
    cd strathmore-roundup
    ```

2.  Install dependencies:
    ```bash
    pip install pygame numpy
    ```

3.  Run the game:
    ```bash
    python strathmoregame.py
    ```

## 📦 Building Executable

To create a standalone Windows executable (`.exe`):

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Run the build command:
    ```bash
    pyinstaller --noconsole --onefile --add-data "*.png;." strathmoregame.py
    ```

3.  The executable will be located in the `dist/` directory.

## 🧪 Development

The project maintains high code quality and test coverage standards.

### Running Tests
The project uses `pytest` for unit and integration testing. The test suite covers game logic, collision detection, and rendering helpers.

```bash
pip install pytest pytest-cov
pytest --cov=strathmoregame tests/
```

*Current Coverage Target: >98%*

### Linting
The project uses `ruff` for fast and strict linting.

```bash
pip install ruff
ruff check .
```

## 📂 Project Structure

*   `strathmoregame.py`: Main entry point and game logic (Game class, render loop).
*   `tests/`: Comprehensive test suite.
*   `assets/*.png`: Game assets (sprites, background).
*   `wrk_docs/`: Development documentation and coverage reports.

## 📜 Credits

**Author:** Martin Davidson (0x6D64)  
**Created:** March 2024
