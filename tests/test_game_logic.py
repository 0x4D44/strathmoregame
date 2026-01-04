import pytest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from strathmoregame import Game, GAME_STATE_RUNLEVEL, GAME_STATE_INITLEVEL, GAME_STATE_ENDED

@pytest.fixture
def game():
    return Game(1000, 700)

def test_initialization(game):
    assert game.gamestate == GAME_STATE_INITLEVEL
    assert game.score == 0

def test_level_start(game):
    game.update(100.0, {})
    assert game.gamestate == GAME_STATE_RUNLEVEL
    assert len(game.deerpos) == 15
    assert game.start_time == 100.0

def test_nexus_movement(game):
    game.update(100.0, {})
    initial_y = game.nexuspos[1]
    game.update(100.02, {'UP': True}) 
    assert game.nexuspos[1] == initial_y - game.nexus_speed

def test_bounds_nexus(game):
    game.update(0, {})
    
    game.nexuspos = [-100, 500]
    game.update(0.1, {'LEFT': True})
    assert game.nexuspos[0] == -25
    
    game.nexuspos = [2000, 500]
    game.update(0.2, {'RIGHT': True})
    assert game.nexuspos[0] == game.width - 25
    
    game.nexuspos = [500, -100]
    game.update(0.3, {'UP': True})
    assert game.nexuspos[1] == 300
    
    game.nexuspos = [500, 2000]
    game.update(0.4, {'DOWN': True})
    assert game.nexuspos[1] == game.height - 25

def test_deer_caught(game):
    game.update(0, {})
    game.deerlost = [True] * 15
    game.deerpos[0] = [100, 100]
    game.deerlost[0] = False
    game.score = 0
    game.update(0.1, {})
    assert game.deercaught[0] is True
    assert game.score > 0

def test_deer_lost(game):
    game.update(0, {})
    game.deerlost = [True] * 15
    game.deerpos[0] = [-100, 100]
    game.deerlost[0] = False
    game.score = 0
    game.update(0.1, {})
    assert game.deerlost[0] is True
    assert game.score == -25

def test_deer_lost_bounds_all(game):
    for i, pos in enumerate([[-100, 500], [2000, 500], [500, -100], [500, 2000]]):
        game.reset()
        game.update(0, {})
        game.deerlost = [True] * 15
        game.deerpos[0] = pos
        game.deerlost[0] = False
        game.score = 0
        game.update(0.1, {})
        assert game.deerlost[0] is True, f"Failed for pos {pos}"

def test_level_complete_logic(game):
    game.update(0, {})
    game.deercaught = [True] * 15
    complete, count = game.check_level_complete()
    assert complete is True
    assert count == 15
    res = game.next_level_logic()
    assert res == "upgrade"
    assert game.level == 2
    assert game.gamestate == GAME_STATE_INITLEVEL

def test_game_over(game):
    game.update(0, {})
    game.deercaught = [False] * 15
    game.deerlost = [True] * 15 
    res = game.next_level_logic()
    assert res == "fail"
    assert game.gamestate == GAME_STATE_ENDED

def test_cheat_keys(game):
    game.update(0, {})
    with patch('random.choice', return_value=0):
        game.update(0.01, {'CHEAT_L': True})
        assert game.deerpos[0][0] >= game.width + 50
        game.update(0.02, {'CHEAT_C': True})
        assert game.deerpos[0][0] < game.width / 3

def test_repulsion_logic(game):
    game.update(0, {})
    game.nexuspos = [500, 500]
    game.deerpos[0] = [500, 480] 
    initial_y = game.deerpos[0][1]
    with patch('random.randint', return_value=0):
        game.update(0.02, {})
        assert game.deerpos[0][1] < initial_y

def test_deer_directions(game):
    directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
    
    for direction in directions:
        game.reset()
        game.update(0, {}) # Init
        
        game.deerpos[0] = [500, 500]
        game.deerdir[0] = direction
        game.deerlost = [True] * 15
        game.deerlost[0] = False
        
        # side_effect: [delta=10, direction_change_check=500]
        with patch('random.randint', side_effect=[10, 500]): 
            game.update(0.1, {})
            
            x, y = game.deerpos[0]
            if direction == 'N':
                assert y == 490
            elif direction == 'S':
                assert y == 510
            elif direction == 'E':
                assert x == 490
            elif direction == 'W':
                assert x == 510
            elif direction == 'NE':
                assert x == 490 and y == 490
            elif direction == 'NW':
                assert x == 510 and y == 490
            elif direction == 'SE':
                assert x == 490 and y == 510
            elif direction == 'SW':
                assert x == 510 and y == 510