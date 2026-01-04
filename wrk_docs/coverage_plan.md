# Code Coverage Improvement Plan

**Target:** 98% Coverage
**Strategy:** Refactor for Testability & Incremental Testing

## Stage 1: Infrastructure & Helper Extraction
**Goal:** Establish the testing framework and test the easiest components.
1.  **Setup:** Create a `tests/` directory and a basic `conftest.py`.
2.  **Refactoring:**
    *   Extract the `wrap_text` function to a separate module or static method to allow testing without `pygame` initialization.
    *   Extract `adjust_brightness` if possible, or mock `pygame.surfarray` interactions.
3.  **Testing:**
    *   Write unit tests for `wrap_text` covering edge cases (long words, exact width fits).
    *   Write basic tests for `adjust_brightness` using mock surfaces.

## Stage 2: Core Logic Decoupling
**Goal:** Test game rules without running the GUI.
1.  **Refactoring:**
    *   Create a `GameState` class to hold all global variables (`deerpos`, `nexuspos`, `score`, `level`, etc.).
    *   Extract the "Update" logic from the main `while True` loop into a method `GameState.update(dt, input_state)`.
    *   This method should take inputs (keys pressed) and time delta, and return the new state, without drawing anything.
2.  **Testing:**
    *   Test deer movement algorithms (randomness, repulsion from Nexus).
    *   Test collision detection (Deer vs Castle, Deer vs Edge).
    *   Test scoring logic and level progression.

## Stage 3: Event Loop & Integration
**Goal:** Verify the game flow.
1.  **Refactoring:**
    *   Wrap the main loop in a `GameEngine` class or `run_game()` function that accepts dependency injection for the "Display" and "Event Source".
    *   Allow the game to run for a fixed number of frames or until a condition is met during tests.
2.  **Testing:**
    *   Simulate a full level playthrough (fast-forwarded).
    *   Verify transitions between `INITLEVEL`, `RUNLEVEL`, and `ENDED` states.
    *   Test input handling (Key presses moving the Nexus).

## Stage 4: Visuals & Edge Cases (Final Polish)
**Goal:** Reach 98% coverage.
1.  **Refactoring:**
    *   Ensure `draw_led` and other drawing functions are isolated enough to be called with a mock surface.
2.  **Testing:**
    *   Test the "Poem Generation" logic (mocking the delays/display).
    *   Test `display_splash_screen` logic (mocking the event loop for exit conditions).
    *   Cover all branches in `main` (if `__name__ == "__main__":`).

## Execution Protocol
*   Run `pytest --cov=strathmoregame tests/` after each stage.
*   Refactor code *minimally* to enable testing, preserving original behavior.
