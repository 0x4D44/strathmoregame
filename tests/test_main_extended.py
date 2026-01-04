import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import pygame

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from strathmoregame import main, NEXUS_TYPE_PMEC, NEXUS_TYPE_3RACK, NEXUS_TYPE_10RACK, GAME_STATE_ENDED, GAME_STATE_RUNLEVEL

def setup_mock_pg(mock_pg):
    mock_pg.QUIT = pygame.QUIT
    mock_pg.KEYDOWN = pygame.KEYDOWN
    mock_pg.K_RETURN = pygame.K_RETURN
    mock_pg.K_UP = pygame.K_UP
    mock_pg.K_DOWN = pygame.K_DOWN
    mock_pg.K_LEFT = pygame.K_LEFT
    mock_pg.K_RIGHT = pygame.K_RIGHT
    mock_pg.K_c = pygame.K_c
    mock_pg.K_l = pygame.K_l
    mock_pg.KMOD_CTRL = pygame.KMOD_CTRL
    mock_pg.K_SPACE = pygame.K_SPACE
    mock_pg.K_ESCAPE = pygame.K_ESCAPE
    mock_pg.key.get_mods.return_value = 0

def test_main_level_complete_upgrade():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    
    mock_key_return = MagicMock()
    mock_key_return.type = pygame.KEYDOWN
    mock_key_return.key = pygame.K_RETURN

    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        mock_pg.event.get.side_effect = [[], [mock_key_return], [mock_quit]]
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        } 

        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            instance.gamestate = GAME_STATE_RUNLEVEL
            instance.nexustype = NEXUS_TYPE_PMEC
            instance.check_level_complete.return_value = (True, 15)
            instance.next_level_logic.return_value = "upgrade"
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()
            
            assert instance.next_level_logic.called

def test_main_level_complete_10rack():
    # Covers the 10RACK branch in loop
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    mock_key_return = MagicMock()
    mock_key_return.type = pygame.KEYDOWN
    mock_key_return.key = pygame.K_RETURN

    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        mock_pg.event.get.side_effect = [[], [mock_key_return], [mock_quit]]
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        } 

        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            instance.gamestate = GAME_STATE_RUNLEVEL
            instance.nexustype = NEXUS_TYPE_10RACK
            instance.check_level_complete.return_value = (True, 15)
            instance.next_level_logic.return_value = "upgrade"
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()

def test_main_initlevel_fallthrough():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    
    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        mock_pg.event.get.side_effect = [[], [mock_quit]]
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        }
        
        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            # Force INITLEVEL
            instance.gamestate = 0 # INITLEVEL
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()
            
            # Verify update called
            assert instance.update.called
            # Verify flip called (logic falls through)
            assert mock_pg.display.flip.called

def test_main_game_over():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    
    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        mock_pg.event.get.side_effect = [[], [mock_quit]]
        
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        } 

        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            instance.gamestate = GAME_STATE_ENDED
            instance.score = 500 
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()

def test_main_game_over_poem():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    
    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        mock_pg.event.get.side_effect = [[], [mock_quit]]
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        } 

        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            instance.gamestate = GAME_STATE_ENDED
            instance.score = 15000 
            
            with patch('strathmoregame.display_splash_screen'):
                with patch('strathmoregame.generate_poem') as mock_poem:
                    with pytest.raises(SystemExit):
                        main()
                    assert mock_poem.called

def test_main_inputs():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    
    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        mock_pg.event.get.side_effect = [[], [mock_quit]]
        
        keys_dict = {
            pygame.K_UP: True, pygame.K_DOWN: True, 
            pygame.K_LEFT: True, pygame.K_RIGHT: True
        }
        mock_pg.key.get_pressed.return_value = MagicMock()
        mock_pg.key.get_pressed.return_value.__getitem__.side_effect = lambda k: keys_dict.get(k, False)
        
        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            instance.gamestate = GAME_STATE_RUNLEVEL
            instance.check_level_complete.return_value = (False, 0)
            instance.nexustype = NEXUS_TYPE_PMEC
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()
            
            args, _ = instance.update.call_args
            keys_passed = args[1]
            assert keys_passed['UP']

def test_main_cheat_keys_event():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    
    mock_cheat_c = MagicMock()
    mock_cheat_c.type = pygame.KEYDOWN
    mock_cheat_c.key = pygame.K_c
    
    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        # Sequence: Loop 1 (C key), Loop 2 (Quit)
        mock_pg.event.get.side_effect = [[mock_cheat_c], [mock_quit]]
        
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        }
        
        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            instance.gamestate = GAME_STATE_RUNLEVEL
            instance.check_level_complete.return_value = (False, 0)
            instance.nexustype = NEXUS_TYPE_PMEC
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()
            
            args, _ = instance.update.call_args
            keys_passed = args[1]
            assert keys_passed['CHEAT_C']

def test_main_runlevel_3rack():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    
    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        mock_pg.event.get.side_effect = [[], [mock_quit]]
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        } 
        
        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            instance.gamestate = GAME_STATE_RUNLEVEL
            instance.check_level_complete.return_value = (False, 0)
            instance.nexustype = NEXUS_TYPE_3RACK # Hits different branch
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()

def test_main_level_complete_pass():
    mock_quit = MagicMock()
    mock_quit.type = pygame.QUIT
    mock_key_return = MagicMock()
    mock_key_return.type = pygame.KEYDOWN
    mock_key_return.key = pygame.K_RETURN
    
    with patch('strathmoregame.pygame') as mock_pg:
        setup_mock_pg(mock_pg)
        mock_pg.event.get.side_effect = [[], [mock_key_return], [mock_quit]]
        mock_pg.key.get_pressed.return_value = {
            pygame.K_UP: False, pygame.K_DOWN: False,
            pygame.K_LEFT: False, pygame.K_RIGHT: False
        } 
        
        with patch('strathmoregame.Game') as MockGame:
            instance = MockGame.return_value
            instance.gamestate = GAME_STATE_RUNLEVEL
            instance.nexustype = NEXUS_TYPE_PMEC
            instance.check_level_complete.return_value = (True, 6)
            instance.next_level_logic.return_value = "pass"
            
            with patch('strathmoregame.display_splash_screen'):
                with pytest.raises(SystemExit):
                    main()
            assert instance.next_level_logic.called