from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path so we can import strathmoregame
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strathmoregame import wrap_text

def test_wrap_text_simple():
    mock_font = MagicMock()
    # Mock font.size to return a width based on string length (10px per char)
    # The function calls font.size(current_line + ' ' + word)
    mock_font.size.side_effect = lambda text: (len(text) * 10, 20)
    
    text = "Hello World"
    # "Hello" is 50px. "Hello World" is 110px.
    # Max width 80.
    # Start: current="Hello"
    # Next word "World": check size("Hello World") -> 110. > 80? Yes.
    # Append "Hello". current="World".
    # End loop. Append "World".
    
    result = wrap_text(text, mock_font, 80)
    assert result == "Hello\nWorld"

def test_wrap_text_fits():
    mock_font = MagicMock()
    mock_font.size.side_effect = lambda text: (len(text) * 10, 20)
    
    text = "Hello World"
    # Max width 120. Fits.
    result = wrap_text(text, mock_font, 120)
    assert result == "Hello World"

def test_wrap_text_splot_keyword():
    mock_font = MagicMock()
    mock_font.size.return_value = (10, 20) # Everything fits size-wise
    
    text = "LineOne SPLOT LineTwo"
    # SPLOT forces a newline
    result = wrap_text(text, mock_font, 100)
    assert result == "LineOne\nLineTwo"

def test_wrap_text_long_word():
    # If a single word is longer than max_width, it should still be added (logic doesn't split words)
    mock_font = MagicMock()
    mock_font.size.side_effect = lambda text: (len(text) * 10, 20)
    
    text = "Supercalifragilistic"
    # Width 200. Max width 50.
    # current="Super..."
    # Loop doesn't run (no next word).
    # Appends.
    result = wrap_text(text, mock_font, 50)
    assert result == "Supercalifragilistic"

def test_adjust_brightness():
    from strathmoregame import adjust_brightness
    import numpy as np
    
    mock_image = MagicMock()
    
    # Create a real numpy array 1x1 pixel, red color (255, 0, 0)
    real_array = np.array([[[255, 0, 0]]], dtype=np.uint8)
    
    with patch('strathmoregame.pygame.surfarray.array3d', return_value=real_array):
        with patch('strathmoregame.pygame.surfarray.make_surface') as mock_make:
            adjust_brightness(mock_image, 0.5)
            
            # Check if make_surface was called with dimmed array
            args, _ = mock_make.call_args
            result_array = args[0]
            # 255 * 0.5 = 127.5 -> 127 (uint8)
            assert result_array[0][0][0] == 127
            assert result_array[0][0][1] == 0
