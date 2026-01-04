import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from strathmoregame import draw_led, generate_poem, NEXUS_TYPE_PMEC, main, draw_led_int

def test_draw_led():
    mock_window = MagicMock()
    # draw_led calls draw_led_int which calls pygame.draw.rect
    # We can mock draw_led_int to verify draw_led logic
    with patch('strathmoregame.draw_led_int') as mock_int:
        draw_led(mock_window, 0, 0, NEXUS_TYPE_PMEC)
        assert mock_int.called
        # Check args
        mock_int.assert_called_with(mock_window, 20, 20, 4, (0, 255, 0))

def test_draw_led_int():
    mock_window = MagicMock()
    # Forces randomness to draw
    with patch('random.uniform', return_value=0.0): 
        with patch('strathmoregame.pygame.draw.rect') as mock_rect:
            draw_led_int(mock_window, 0, 0, 1, (255,0,0))
            assert mock_rect.called

def test_draw_led_int_off():
    mock_window = MagicMock()
    # Forces randomness to NOT draw (>= 0.5)
    with patch('random.uniform', return_value=0.6): 
        with patch('strathmoregame.pygame.draw.rect') as mock_rect:
            draw_led_int(mock_window, 0, 0, 1, (255,0,0))
            assert not mock_rect.called

def test_generate_poem():
    mock_window = MagicMock()
    with patch('strathmoregame.pygame') as mock_pg:
        # Mock font render
        mock_font = MagicMock()
        mock_pg.font.Font.return_value = mock_font
        
        generate_poem(mock_window, 1000, 700)
        
        assert mock_pg.display.flip.called

def test_main_quit_immediately():
    # Setup QUIT event
    mock_event = MagicMock()
    mock_event.type = pygame.QUIT
    
    with patch('strathmoregame.pygame') as mock_pg:
        mock_pg.event.get.return_value = [mock_event]
        mock_pg.QUIT = pygame.QUIT
        mock_pg.KEYDOWN = pygame.KEYDOWN
        
        # Mock display splash screen to avoid delay
        with patch('strathmoregame.display_splash_screen'):
            with pytest.raises(SystemExit):
                main()
            
            # Verify init was called
            assert mock_pg.init.called
            assert mock_pg.display.set_mode.called

def test_display_splash_screen():
    mock_window = MagicMock()
    with patch('strathmoregame.pygame') as mock_pg:
        # Need to mock event loop to exit: KEYDOWN -> RETURN
        mock_event = MagicMock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_RETURN
        mock_pg.event.get.return_value = [mock_event]
        mock_pg.KEYDOWN = pygame.KEYDOWN
        mock_pg.K_RETURN = pygame.K_RETURN
        mock_pg.K_SPACE = pygame.K_SPACE
        mock_pg.K_ESCAPE = pygame.K_ESCAPE
        mock_pg.image.load.return_value.convert_alpha.return_value = MagicMock()
        
        # Configure font mock for wrap_text
        mock_font_instance = MagicMock()
        mock_font_instance.size.return_value = (10, 10)
        mock_pg.font.Font.return_value = mock_font_instance

        from strathmoregame import display_splash_screen
        display_splash_screen(mock_window, 1000, 700)
        
        assert mock_pg.display.flip.called

def test_draw_led_types():
    mock_window = MagicMock()
    with patch('strathmoregame.draw_led_int') as mock_int:
        from strathmoregame import NEXUS_TYPE_3RACK, NEXUS_TYPE_10RACK
        draw_led(mock_window, 0, 0, NEXUS_TYPE_3RACK)
        assert mock_int.call_count == 3
        
        mock_int.reset_mock()
        draw_led(mock_window, 0, 0, NEXUS_TYPE_10RACK)
        assert mock_int.call_count == 8

def test_main_loop_iteration():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    
    with patch('strathmoregame.pygame') as mock_pg:
        # First call: No events (game runs). Second call: Quit.
        mock_pg.event.get.side_effect = [[], [mock_quit]]
        mock_pg.QUIT = pygame.QUIT
        mock_pg.KEYDOWN = pygame.KEYDOWN
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False, 
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        }
        mock_pg.K_UP = pygame.K_UP
        mock_pg.K_DOWN = pygame.K_DOWN
        mock_pg.K_LEFT = pygame.K_LEFT
        mock_pg.K_RIGHT = pygame.K_RIGHT
        mock_pg.K_c = pygame.K_c
        mock_pg.K_l = pygame.K_l
        mock_pg.KMOD_CTRL = pygame.KMOD_CTRL
        mock_pg.key.get_mods.return_value = 0

        # Mock Game to avoid logic
        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            # Use real constant for safety if import fails
            instance.gamestate = 1 # RUNLEVEL
            instance.check_level_complete.return_value = (False, 0)
            instance.nexustype = NEXUS_TYPE_PMEC # Ensure image is selected
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()
            
            # Verify update was called
            assert instance.update.called