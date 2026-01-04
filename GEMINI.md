# Strathmore Roundup

## Project Overview
**Strathmore Roundup** is a simple 2D game written in Python using the `pygame` library. The player controls a "Nexus server" to round up escaped deer and return them to Strathmore Castle.

**Author:** Martin Davidson  
**Created:** March 2024

### Core Gameplay
*   **Objective:** Herd deer into the castle (left 1/3 of the screen).
*   **Controls:** Arrow keys to move the Nexus server.
*   **Mechanics:**
    *   Deer run away from the Nexus when close.
    *   Deer are "caught" if they reach the castle area.
    *   Deer are "lost" if they go off-screen.
    *   Upgrades (better Nexus hardware) are awarded for catching enough deer.
*   **Winning:** High scores trigger a special poem ending.

## Key Files
*   `strathmoregame.py`: The main source code containing the game loop, logic, and rendering.
*   `strathmoregame.spec`: Configuration file for PyInstaller to bundle the game into a standalone executable.
*   `V1.1/build.cmd`: Example batch script for building the executable.
*   **Assets (`*.png`):**
    *   `background.png`: Game background.
    *   `stag.png`, `roe.png`: Deer sprites.
    *   `pmec.png`, `rack3.png`, `rack10.png`: Player avatars (Nexus server levels).
    *   `splashscreen.png`: Intro screen.

## Setup and Running

### Prerequisites
*   Python 3.x
*   `pygame`
*   `numpy`

### Installation
1.  Ensure Python is installed.
2.  Install dependencies:
    ```bash
    pip install pygame numpy
    ```

### Running the Game
Execute the script directly with Python:
```bash
python strathmoregame.py
```

## Building the Executable
The project uses **PyInstaller** to create a standalone executable.

### Build Command
Run the following command in the project root:
```bash
pyinstaller --noconsole --onefile --add-data "*.png;." strathmoregame.py
```
*   `--noconsole`: Hides the console window.
*   `--onefile`: Bundles everything into a single `.exe`.
*   `--add-data "*.png;."`: Includes all PNG assets in the root of the bundle.

*Note: The `V1.1/build.cmd` file contains a hardcoded path to PyInstaller and may need adjustment for your specific environment.*

## Code Structure & Conventions
*   **Entry Point:** The script runs immediately; no `if __name__ == "__main__":` block is used (imperative style).
*   **Asset Loading:** Uses `sys._MEIPASS` to correctly locate assets whether running as a script or a frozen PyInstaller executable.
*   **State Management:** Game state (`GAME_STATE_INITLEVEL`, `GAME_STATE_RUNLEVEL`, etc.) is managed via global integer constants.
