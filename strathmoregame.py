# Strathmore Roundup game
#
# Martin Davidson (0x6D64), 2024-03-03
#
# Shrunk screen to 1000x700, 2024-03-12
#
# An experiment with Github copilot and pygame to create a simple game.
#
import pygame
import numpy as np
import sys
import random  # Add import statement for the random module
import time
import os 

# Constants
NEXUS_TYPE_PMEC = 0
NEXUS_TYPE_3RACK = 1
NEXUS_TYPE_10RACK = 2

GAME_STATE_INITLEVEL = 0
GAME_STATE_RUNLEVEL = 1
GAME_STATE_ENDED = 2

def display_splash_screen(window, window_width, window_height):
    application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(application_path, 'splashscreen.png')    

    splash_image = pygame.image.load(image_path).convert_alpha()
    splash_image = pygame.transform.scale(splash_image, (window_width, window_height))
    window.blit(splash_image, (0, 0))
    pygame.display.flip()

    dim_image = adjust_brightness(splash_image, 0.5)  # Decrease brightness by 50%    
    pygame.time.delay(250)  # Add a delay of 1000 milliseconds (1 second)
    window.blit(dim_image, (0, 0))
    pygame.display.flip()

    # Define the fonts
    large_font = pygame.font.Font(None, 80)
    small_font = pygame.font.Font(None, 40)
    medium_font = pygame.font.Font(None, 60)
    
    # Define the texts
    title_text = large_font.render("Welcome to Strathmore Roundup!", True, (255, 255, 255))
    start_text = medium_font.render("Press Enter or left-click to start. Good luck!", True, (255, 255, 255))
    
    # Calculate the positions
    title_pos = title_text.get_rect(center=(window_width/2, window_height/4))
    start_pos = start_text.get_rect(center=(window_width/2, window_height*7/8))

    # Blit the texts onto the screen
    window.blit(title_text, title_pos)
    window.blit(start_text, start_pos)

    # Modify the info text to wrap on the screen
    text = wrap_text("The deer have escaped from Strathmore Castle and are running wild. Use the arrow keys to return as many deer back to the castle before they wander away! SPLOT SPLOT The deer will automatically go into the castle if they get close enough. In the first level, you'll use a PMEC Nexus to round them up, but if you roundup enough deer, you'll get access to better hardware!", small_font, 0.8*window_width)
    
    # Split the text into lines
    lines = text.split('\n')

    # Render each line and blit it onto the screen
    for i, line in enumerate(lines):
        line_surface = small_font.render(line, True, (255, 255, 255))
        line_rect = line_surface.get_rect(center=(window_width/2, window_height/2+(i * 30)-50))
        window.blit(line_surface, line_rect)

    # Update the display
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    return
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = words[0]
    for word in words[1:]:
        if word == "SPLOT":
            lines.append(current_line)
            current_line = ""
        elif font.size((current_line + ' ' + word) if current_line else word)[0] <= max_width:
            if current_line:
                current_line += ' ' + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return '\n'.join(lines)

def adjust_brightness(image, brightness):
    # Convert the image to a NumPy array
    array = pygame.surfarray.array3d(image)

    # Adjust the brightness
    array = np.clip(array * brightness, 0, 255).astype(np.uint8)

    # Convert the array back to a Pygame surface and return it
    return pygame.surfarray.make_surface(array)

def draw_led(window, x, y, type):
    if type == NEXUS_TYPE_PMEC:
        light_color = (0, 255, 0)
        draw_led_int(window, x + 20, y + 20, 4, light_color)
    elif type == NEXUS_TYPE_3RACK:
        light_color = (255, 0, 0)
        draw_led_int(window, x + 37, y + 27, 8, light_color)
        draw_led_int(window, x + 50, y + 23, 8, light_color)
        draw_led_int(window, x + 62, y + 19, 8, light_color)
    elif type == NEXUS_TYPE_10RACK:
        light_color = (255, 255, 0)
        draw_led_int(window, x + 7, y + 33, 9, light_color)
        draw_led_int(window, x + 14, y + 37, 9, light_color)
        draw_led_int(window, x + 33, y + 43, 9, light_color)
        draw_led_int(window, x + 40, y + 47, 9, light_color)
        draw_led_int(window, x + 57, y + 47, 9, light_color)
        draw_led_int(window, x + 64, y + 43, 9, light_color)
        draw_led_int(window, x + 83, y + 37, 9, light_color)
        draw_led_int(window, x + 90, y + 33, 9, light_color)

def draw_led_int(window, x, y, count, light_color):
    for i in range(count):
        if random.uniform(0, 1) < 0.5:
            light_rect = pygame.Rect(x, y + i * 5, 3, 3)
            pygame.draw.rect(window, light_color, light_rect)

def generate_poem(window, window_width, window_height):
    application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    image_path = os.path.join(application_path, 'splashscreen.png')    

    splash_image = pygame.image.load(image_path).convert_alpha()
    splash_image = pygame.transform.scale(splash_image, (window_width, window_height))
    dim_image = adjust_brightness(splash_image, 0.5)  # Decrease brightness by 50%    
    window.blit(dim_image, (0, 0))

    # Print the poem to the screen
    large_font = pygame.font.Font(None, 80)
    header_text = large_font.render("Your score deserves a treat...", True, (255, 255, 255))
    header_pos = header_text.get_rect(center=(window_width/2, window_height/6))
    window.blit(header_text, header_pos)
    pygame.display.flip()

    # Wait for 1.5 seconds
    pygame.time.delay(1500)

    window.blit(dim_image, (0, 0))

    header_text = large_font.render("An ode to AFO Nexus", True, (255, 255, 255))
    header_pos = header_text.get_rect(center=(window_width/2, window_height/6))
    window.blit(header_text, header_pos)

    # Split the text into lines
    poem = "There once was a Nexus so grand.\nIts power spanned both sea and land.\nSDM threads it wove,\nInnovation it drove,\nA digital revolution firsthand."
    lines = poem.split('\n')

    # Render each line and blit it onto the screen
    medium_font = pygame.font.Font(None, 60)
    for i, line in enumerate(lines):
        # Split the line into words and then draw 1 word, then 2 words, then 3 words, then 4 words etc
        words = line.split()
        curtext = ""

        for j in range(len(words)):
            curtext = " ".join(words[:j+1])
            line_surface = medium_font.render(curtext, True, (255, 255, 255))
            line_rect = line_surface.get_rect(topleft=(150, window_height/2 - 180 + (i * 60)))
            window.blit(line_surface, line_rect)
            pygame.display.flip()
            pygame.time.delay(120)
     
    enter_text = medium_font.render("Press Enter or left-click to try again", True, (255, 255, 255))
    enter_pos = enter_text.get_rect(center=(window_width/2, window_height*3/4 + 40))
    window.blit(enter_text, enter_pos)

    pygame.display.flip()

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()
        self.last_update_time = 0

    def reset(self):
        self.gamestate = GAME_STATE_INITLEVEL
        self.level = 1
        self.score = 0
        self.start_time = 0
        self.nexustype = NEXUS_TYPE_PMEC
        self.nexus_speed = 5
        self.nexus_magnitude = 5
        
        self.nexuspos = [0, 0]
        self.deerpos = []
        self.deerdir = []
        self.deerlost = []
        self.deercaught = []
        self.deersex = []

    def init_level_data(self, current_time):
        self.deerpos = []
        self.deerdir = []
        self.deerlost = []
        self.deercaught = []
        self.deersex = []
        for i in range(15):
            self.deerpos.append([random.randint(200, self.width - 200), random.randint(int(self.height / 2) + 50, self.height - 200)])
            self.deerdir.append(random.choice(['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']))
            self.deerlost.append(False)
            self.deercaught.append(False)
            self.deersex.append(random.choice(['M', 'F']))
                
        # Initial position of the Nexus server
        self.nexuspos = [random.randint((int(self.width * 3 / 4)), self.width - 50), random.randint(int(self.height * 3 / 4), self.height - 50)]
        self.start_time = current_time
        self.last_update_time = 0
        self.gamestate = GAME_STATE_RUNLEVEL

    def update(self, current_time, keys):
        if self.gamestate == GAME_STATE_INITLEVEL:
            self.init_level_data(current_time)
            return

        if self.gamestate != GAME_STATE_RUNLEVEL:
            return

        # Handle CHEAT keys (logic moved from event loop for separation)
        if keys.get('CHEAT_C'):
            available_deer = [i for i in range(15) if not self.deercaught[i] and not self.deerlost[i]]
            if available_deer:
                selected_deer = random.choice(available_deer)
                self.deerpos[selected_deer] = [random.randint(0, int(self.width / 3 - 50)), random.randint(0, int(self.height / 2 - 50))]
        
        if keys.get('CHEAT_L'):
            available_deer = [i for i in range(15) if not self.deercaught[i] and not self.deerlost[i]]
            if available_deer:
                selected_deer = random.choice(available_deer)
                self.deerpos[selected_deer] = [self.width + 60, self.height + 60]

        # Only update physics once every 10ms
        if current_time - self.last_update_time < 0.01:
            return

        self.last_update_time = current_time

        # Move the Nexus server
        if keys.get('UP'):
            self.nexuspos[1] -= self.nexus_speed
        if keys.get('DOWN'):
            self.nexuspos[1] += self.nexus_speed
        if keys.get('LEFT'):
            self.nexuspos[0] -= self.nexus_speed
        if keys.get('RIGHT'):
            self.nexuspos[0] += self.nexus_speed

        # Ensure the Nexus server stays within the screen boundaries
        if self.nexuspos[0] < -25:
            self.nexuspos[0] = -25
        if self.nexuspos[0] > self.width - 25:
            self.nexuspos[0] = self.width - 25
        if self.nexuspos[1] < self.height / 2 - 50:
            self.nexuspos[1] = self.height / 2 - 50
        if self.nexuspos[1] > self.height - 25:
            self.nexuspos[1] = self.height - 25
            
        # Update the position of the deer
        delta = random.randint(0, (2 + self.level))
        for i in range(15):
            if self.deerlost[i] or self.deercaught[i]:
                continue
                
            if self.deerdir[i] == 'N':
                self.deerpos[i][1] -= delta
            elif self.deerdir[i] == 'S':
                self.deerpos[i][1] += delta
            elif self.deerdir[i] == 'E':
                self.deerpos[i][0] -= delta
            elif self.deerdir[i] == 'W':
                self.deerpos[i][0] += delta
            elif self.deerdir[i] == 'NE':
                self.deerpos[i][0] -= delta
                self.deerpos[i][1] -= delta
            elif self.deerdir[i] == 'NW':
                self.deerpos[i][0] += delta
                self.deerpos[i][1] -= delta
            elif self.deerdir[i] == 'SE':
                self.deerpos[i][0] -= delta
                self.deerpos[i][1] += delta
            elif self.deerdir[i] == 'SW':
                self.deerpos[i][0] += delta
                self.deerpos[i][1] += delta

            # Change the direction randomly
            if random.randint(0, 50) == 0:  # 2% chance to change direction
                self.deerdir[i] = random.choice(['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'])

            # Calculate the direction for each deer to run away from the Nexus server
            distance = np.sqrt((self.deerpos[i][0] - self.nexuspos[0])**2 + (self.deerpos[i][1] - self.nexuspos[1])**2)                
            if distance <= 150:  # Check if deer is within 150 pixels of the Nexus server
                dx = self.deerpos[i][0] - self.nexuspos[0]
                dy = self.deerpos[i][1] - self.nexuspos[1]
                magnitude = np.sqrt(dx**2 + dy**2)
                if magnitude != 0:
                    self.deerpos[i][0] += (self.nexus_magnitude * dx) / magnitude
                    self.deerpos[i][1] += (self.nexus_magnitude * dy) / magnitude

            # Check if deer is outside the window boundaries
            if self.deerpos[i][0] < -50 or self.deerpos[i][0] > self.width or self.deerpos[i][1] < -50 or self.deerpos[i][1] > self.height:
                self.deerlost[i] = True
                self.score -= 25

            # Check if deer are in the left 3rd of the screen at the top
            if not self.deerlost[i] and self.deerpos[i][0] < self.width / 3 and self.deerpos[i][1] < self.height / 2:
                # Move the deer into the castle
                self.deercaught[i] = True
                self.score += int(100 + 20 * self.level * self.level + max((current_time - self.start_time) * 10, 0) + self.nexustype * 250)

            # Keep the deer within the bottom half of the window
            if self.deerpos[i][1] < self.height / 2:
                self.deerpos[i][1] = self.height / 2
    
    def check_level_complete(self):
        # Returns (Completed?, LevelUp?, Message)
        if sum(self.deercaught) + sum(self.deerlost) == 15:
            caught_count = sum(self.deercaught)
            return True, caught_count
        return False, 0

    def next_level_logic(self):
        caught = sum(self.deercaught)
        if caught >= 8:
            self.level += 1
            self.nexustype += 1
            self.nexustype = min(self.nexustype, NEXUS_TYPE_10RACK)
            self.nexus_speed += 2
            self.nexus_magnitude += 5
            self.score += 1000 + 500 * self.level
            self.gamestate = GAME_STATE_INITLEVEL
            return "upgrade"
        elif caught > 5:
            self.level += 1
            self.score += 500
            self.gamestate = GAME_STATE_INITLEVEL
            return "pass"
        else:
            self.gamestate = GAME_STATE_ENDED
            return "fail"

def main():
    ##########################################################################################
    # Main program
    ##########################################################################################
    
    # Initialize pygame
    pygame.init()

    # Set up the window
    window_width = 1000
    window_height = 700
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Strathmore Roundup")

    # Display the splash screen
    display_splash_screen(window, window_width, window_height)

    # Load assets
    application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    
    def load_img(name, size=None):
        path = os.path.join(application_path, name)
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        else:
            # background special case (no convert_alpha usually for bg but fine here)
            img = pygame.image.load(path) # re-load without alpha for bg if needed, or just standard
            img = pygame.transform.scale(img, (window_width, window_height))
        return img

    background_image = load_img('background.png')
    stag_image = load_img('stag.png', (50, 50))
    roe_image = load_img('roe.png', (50, 50))
    pmec_image = load_img('pmec.png', (50, 50))
    rack3_image = load_img('rack3.png', (75, 75))
    rack10_image = load_img('rack10.png', (100, 100))

    # Define the font
    level_font = pygame.font.Font(None, 40)

    # Initialize Game
    game = Game(window_width, window_height)

    # Game loop
    while True:
        # Input handling
        keys_pressed = {}
        # Poll events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and ((event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL) or event.key == pygame.K_q)):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    keys_pressed['CHEAT_C'] = True
                if event.key == pygame.K_l:
                    keys_pressed['CHEAT_L'] = True

        # Poll keys state
        pygame_keys = pygame.key.get_pressed()
        if pygame_keys[pygame.K_UP]:
            keys_pressed['UP'] = True
        if pygame_keys[pygame.K_DOWN]:
            keys_pressed['DOWN'] = True
        if pygame_keys[pygame.K_LEFT]:
            keys_pressed['LEFT'] = True
        if pygame_keys[pygame.K_RIGHT]:
            keys_pressed['RIGHT'] = True
        
        # Update
        game.update(time.time(), keys_pressed)

        # Drawing & Logic that requires UI interaction (like level complete screen)
        # Note: logic for checking level complete is in Game, but UI transition is here.
        
        if game.gamestate == GAME_STATE_RUNLEVEL:
            # Check for level complete
            is_complete, caught_count = game.check_level_complete()
            if is_complete:
                # This level is complete! Animation...
                scale_factor = 1
                brightness = 1
                while scale_factor < 5.0:
                    dim_image = adjust_brightness(background_image, brightness)
                    window.blit(dim_image, (0, 0))
                    brightness -= 0.04

                    if game.nexustype == NEXUS_TYPE_PMEC:
                        image = pmec_image
                    elif game.nexustype == NEXUS_TYPE_3RACK:
                        image = rack3_image
                    elif game.nexustype == NEXUS_TYPE_10RACK:
                        image = rack10_image

                    scaled_nexus_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), (int(image.get_width() * scale_factor))))
                    nexus_x = window_width / 2 - scaled_nexus_image.get_width() / 2
                    nexus_y = window_height / 2 - scaled_nexus_image.get_height() / 2
                    window.blit(scaled_nexus_image, (nexus_x, nexus_y))
                    pygame.display.flip()
                    scale_factor += 0.5
                    time.sleep(0.01)

                # Texts
                level_complete_font = pygame.font.Font(None, 100)
                level_complete_text = level_complete_font.render("Level Complete!", True, (255, 255, 255))
                window.blit(level_complete_text, level_complete_text.get_rect(center=(window_width / 2, window_height / 6)))
                
                caught_text = level_font.render("You caught: " + str(caught_count) + " deer", True, (255, 255, 255))
                window.blit(caught_text, caught_text.get_rect(center=(window_width / 2, window_height * 3 / 4)))

                # Next Level Logic
                result = game.next_level_logic()
                
                summary_text_str = ""
                extra_text_str = ""
                if result == "upgrade":
                    summary_text_str = "has arrived for you to use next time."
                    if game.nexustype - 1 == NEXUS_TYPE_PMEC: # It was incremented already
                        extra_text_str = "That's pretty good! A 3-rack Nexus"
                    else: # 3RACK or 10RACK
                        extra_text_str = "Feel the power of Nexus! A big Nexus"
                elif result == "pass":
                    summary_text_str = "Not so good - no upgrades for you."
                else: # fail
                    summary_text_str = "Lost your glasses? Your journey ends here."

                if extra_text_str:
                     st = level_font.render(summary_text_str, True, (255, 255, 255))
                     window.blit(st, st.get_rect(center=(window_width / 2, window_height * 3 / 4 + 60)))
                     et = level_font.render(extra_text_str, True, (255, 255, 255))
                     window.blit(et, et.get_rect(center=(window_width / 2, window_height * 3 / 4 + 30)))
                else:
                     st = level_font.render(summary_text_str, True, (255, 255, 255))
                     window.blit(st, st.get_rect(center=(window_width / 2, window_height * 3 / 4 + 60)))

                enter_text = level_font.render("Press Enter or left-click.", True, (255, 255, 255))
                window.blit(enter_text, enter_text.get_rect(center=(window_width/2, window_height*3/4 + 120)))
                pygame.display.flip()

                # Wait for input
                key_wait = True
                while key_wait:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                                key_wait = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                key_wait = False
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                continue # Skip drawing this frame

            # Standard Drawing
            window.blit(background_image, (0, 0))
            for i in range(15):
                if not game.deerlost[i] and not game.deercaught[i]:
                    img = stag_image if game.deersex[i] == 'M' else roe_image
                    if game.deerdir[i] in ['W', 'NW', 'SW']:
                        img = pygame.transform.flip(img, True, False)
                    window.blit(img, game.deerpos[i])

            if game.nexustype == NEXUS_TYPE_PMEC:
                image = pmec_image
            elif game.nexustype == NEXUS_TYPE_3RACK:
                image = rack3_image
            elif game.nexustype == NEXUS_TYPE_10RACK:
                image = rack10_image
            window.blit(image, game.nexuspos)
            draw_led(window, game.nexuspos[0], game.nexuspos[1], game.nexustype)

            level_text = level_font.render("Level: " + str(game.level) + " - Caught: " + str(sum(game.deercaught)) + " - Lost: " + str(sum(game.deerlost)), True, (0, 0, 0))
            window.blit(level_text, (10, 10))
            lost_text = level_font.render("Score: " + str(game.score), True, (0, 0, 0))
            window.blit(lost_text, lost_text.get_rect(topright=(window_width - 10, 10)))

        elif game.gamestate == GAME_STATE_ENDED:
            if game.score > 10000:
                generate_poem(window, window_width, window_height)
            else:
                dim_image = adjust_brightness(background_image, 0.3)
                window.blit(dim_image, (0, 0))
                
                game_over_font = pygame.font.Font(None, 150)
                score_text = game_over_font.render("Score: " + str(game.score), True, (255, 255, 255))
                window.blit(score_text, score_text.get_rect(center=(window_width / 2, window_height / 6)))
                
                game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
                window.blit(game_over_text, game_over_text.get_rect(center=(window_width / 2, window_height / 2)))

                enter_text = level_font.render("Press Enter or left-click to try again", True, (255, 255, 255))
                window.blit(enter_text, enter_text.get_rect(center=(window_width/2, window_height*3/4)))
                pygame.display.flip()

            # Wait for input
            key_wait = True
            while key_wait:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                            key_wait = False
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            key_wait = False
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            
            game.reset()

        pygame.display.flip()

if __name__ == "__main__":
    main()