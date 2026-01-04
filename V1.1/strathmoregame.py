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

def display_splash_screen():
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
        elif font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
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

def draw_led(x, y, type):
    if type == NEXUS_TYPE_PMEC:
        light_color = (0, 255, 0)
        draw_led_int(x + 20, y + 20, 4, light_color)
    elif type == NEXUS_TYPE_3RACK:
        light_color = (255, 0, 0)
        draw_led_int(x + 37, y + 27, 8, light_color)
        draw_led_int(x + 50, y + 23, 8, light_color)
        draw_led_int(x + 62, y + 19, 8, light_color)
    elif type == NEXUS_TYPE_10RACK:
        light_color = (255, 255, 0)
        draw_led_int(x + 7, y + 33, 9, light_color)
        draw_led_int(x + 14, y + 37, 9, light_color)
        draw_led_int(x + 33, y + 43, 9, light_color)
        draw_led_int(x + 40, y + 47, 9, light_color)
        draw_led_int(x + 57, y + 47, 9, light_color)
        draw_led_int(x + 64, y + 43, 9, light_color)
        draw_led_int(x + 83, y + 37, 9, light_color)
        draw_led_int(x + 90, y + 33, 9, light_color)

def draw_led_int(x, y, count, light_color):
    for i in range(count):
        if random.uniform(0, 1) < 0.5:
            light_rect = pygame.Rect(x, y + i * 5, 3, 3)
            pygame.draw.rect(window, light_color, light_rect)

def generate_poem():
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
display_splash_screen()

# Load and scale the background image
application_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
image_path = os.path.join(application_path, 'background.png')    
background_image = pygame.image.load(image_path)
background_image = pygame.transform.scale(background_image, (window_width, window_height))
window.blit(background_image, (0, 0))

# Load and scale the deer image
image_path = os.path.join(application_path, 'stag.png')    
stag_image = pygame.image.load(image_path).convert_alpha()
stag_image = pygame.transform.scale(stag_image, (50, 50))
image_path = os.path.join(application_path, 'roe.png')    
roe_image = pygame.image.load(image_path).convert_alpha()
roe_image = pygame.transform.scale(roe_image, (50, 50))

# Load and scale the pmec image
image_path = os.path.join(application_path, 'pmec.png')    
pmec_image = pygame.image.load(image_path).convert_alpha()
pmec_image = pygame.transform.scale(pmec_image, (50, 50))

# Load and scale the pmec image
image_path = os.path.join(application_path, 'rack3.png')    
rack3_image = pygame.image.load(image_path).convert_alpha()
rack3_image = pygame.transform.scale(rack3_image, (75, 75))

# Load and scale the pmec image
image_path = os.path.join(application_path, 'rack10.png')    
rack10_image = pygame.image.load(image_path).convert_alpha()
rack10_image = pygame.transform.scale(rack10_image, (100, 100))

# Init game variables
GAME_STATE_INITLEVEL = 0
GAME_STATE_RUNLEVEL = 1
GAME_STATE_ENDED = 2
gamestate = GAME_STATE_INITLEVEL
level = 1
score = 0
start_time = 0

NEXUS_TYPE_PMEC = 0
NEXUS_TYPE_3RACK = 1
NEXUS_TYPE_10RACK = 2
nexustype = NEXUS_TYPE_PMEC
nexus_speed = 5
nexus_magnitude = 5

# Define the font
level_font = pygame.font.Font(None, 40)

# Game loop
while True:
    ###############
    # Update the position of deer
    if gamestate == GAME_STATE_INITLEVEL:
        # Initial starting position of the deer
        deerpos = []
        deerdir = []
        deerlost = []
        deercaught = []
        deersex = []
        for i in range(15):
            for i in range(15):
                deerpos.append([random.randint(200, window_width - 200), random.randint(int(window_height / 2) + 50, window_height - 200)])
                deerdir.append(random.choice(['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']))
                deerlost.append(False)
                deercaught.append(False)
                deersex.append(random.choice(['M', 'F']))
                
        # Initial position of the Nexus server
        nexuspos = [random.randint((int(window_width * 3 / 4)), window_width - 50), random.randint(int(window_height * 3 / 4), window_height - 50)]

        start_time = time.time()
        last_update_time = 0

        gamestate = GAME_STATE_RUNLEVEL
    elif gamestate == GAME_STATE_RUNLEVEL:
        # Only update once every 100ms
        if time.time() - last_update_time < 0.01:
            continue

        last_update_time = time.time()

        # Get the current state of the keyboard
        keys = pygame.key.get_pressed()

        # Move the Nexus server
        if keys[pygame.K_UP]:
            nexuspos[1] -= nexus_speed
        if keys[pygame.K_DOWN]:
            nexuspos[1] += nexus_speed
        if keys[pygame.K_LEFT]:
            nexuspos[0] -= nexus_speed
        if keys[pygame.K_RIGHT]:
            nexuspos[0] += nexus_speed

        # Ensure the Nexus server stays within the screen boundaries
        if nexuspos[0] < -25:
            nexuspos[0] = -25
        if nexuspos[0] > window_width - 25:
            nexuspos[0] = window_width - 25
        if nexuspos[1] < window_height / 2 - 50:
            nexuspos[1] = window_height / 2 - 50
        if nexuspos[1] > window_height - 25:
            nexuspos[1] = window_height - 25
            
        # Update the position of the deer
        delta = random.randint(0, (2 + level))
        for i in range(15):
            if deerlost[i] or deercaught[i]:
                continue
                
            if deerdir[i] == 'N':
                deerpos[i][1] -= delta
            elif deerdir[i] == 'S':
                deerpos[i][1] += delta
            elif deerdir[i] == 'E':
                deerpos[i][0] -= delta
            elif deerdir[i] == 'W':
                deerpos[i][0] += delta
            elif deerdir[i] == 'NE':
                deerpos[i][0] -= delta
                deerpos[i][1] -= delta
            elif deerdir[i] == 'NW':
                deerpos[i][0] += delta
                deerpos[i][1] -= delta
            elif deerdir[i] == 'SE':
                deerpos[i][0] -= delta
                deerpos[i][1] += delta
            elif deerdir[i] == 'SW':
                deerpos[i][0] += delta
                deerpos[i][1] += delta

            # Change the direction randomly
            if random.randint(0, 50) == 0:  # 2% chance to change direction
                deerdir[i] = random.choice(['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW'])

            # Calculate the direction for each deer to run away from the Nexus server
            distance = np.sqrt((deerpos[i][0] - nexuspos[0])**2 + (deerpos[i][1] - nexuspos[1])**2)                
            if distance <= 150:  # Check if deer is within 150 pixels of the Nexus server
                dx = deerpos[i][0] - nexuspos[0]
                dy = deerpos[i][1] - nexuspos[1]
                magnitude = np.sqrt(dx**2 + dy**2)
                if magnitude != 0:
                    deerpos[i][0] += (nexus_magnitude * dx) / magnitude
                    deerpos[i][1] += (nexus_magnitude * dy) / magnitude

            # Check if deer is outside the window boundaries
            if deerpos[i][0] < -50 or deerpos[i][0] > window_width or deerpos[i][1] < -50 or deerpos[i][1] > window_height:
                deerlost[i] = True
                score -= 25

            # Check if deer are in the left 3rd of the screen at the top
            if deerpos[i][0] < window_width / 3 and deerpos[i][1] < window_height / 2:
                # Move the deer into the castle
                deercaught[i] = True
                score += int(100 + 20 * level * level + max((time.time() - start_time) * 10, 0) + nexustype * 250)

            # Keep the deer within the bottom half of the window
            if deerpos[i][1] < window_height / 2:
                deerpos[i][1] = window_height / 2

    ###############
    # DRAWING OBJECTS

    if gamestate == GAME_STATE_RUNLEVEL:
        # Clear the window
        window.blit(background_image, (0, 0))

        # Draw the deer
        for i in range(15):
            if not deerlost[i] and not deercaught[i]:  # Check if deer is not lost
                if deersex[i] == 'M':
                    deer_image = stag_image
                else:
                    deer_image = roe_image
                
                # Blit the deer image onto the window
                if deerdir[i] in ['W', 'NW', 'SW']:
                    flipped_deer_image = pygame.transform.flip(deer_image, True, False)
                    window.blit(flipped_deer_image, deerpos[i])
                else:
                    window.blit(deer_image, deerpos[i])

        # Draw the Nexus server
        if nexustype == NEXUS_TYPE_PMEC:
            image = pmec_image
        elif nexustype == NEXUS_TYPE_3RACK:
            image = rack3_image
        elif nexustype == NEXUS_TYPE_10RACK:
            image = rack10_image

        window.blit(image, nexuspos)
        
        draw_led(nexuspos[0], nexuspos[1], nexustype)

        # Level indicator and counts
        level_text = level_font.render("Level: " + str(level) + " - Caught: " + str(sum(deercaught)) + " - Lost: " + str(sum(deerlost)), True, (0, 0, 0))
        level_pos = level_text.get_rect(topleft=(10, 10))
        window.blit(level_text, level_pos)

        # Display the score
        lost_text = level_font.render("Score: " + str(score), True, (0, 0, 0))
        lost_pos = lost_text.get_rect(topright=(window_width - 10, 10))
        window.blit(lost_text, lost_pos)
    elif gamestate == GAME_STATE_ENDED:
        if score > 10000:
            generate_poem()
        else:
            dim_image = adjust_brightness(background_image, 0.3)
            window.blit(dim_image, (0, 0))

            game_over_font = pygame.font.Font(None, 150)
            score_text = game_over_font.render("Score: " + str(score), True, (255, 255, 255))
            score_pos = score_text.get_rect(center=(window_width / 2, window_height / 6))
            window.blit(score_text, score_pos)

            game_over_font = pygame.font.Font(None, 150)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            game_over_pos = game_over_text.get_rect(center=(window_width / 2, window_height / 2))
            window.blit(game_over_text, game_over_pos)

            enter_text = level_font.render("Press Enter or left-click to try again", True, (255, 255, 255))
            enter_pos = enter_text.get_rect(center=(window_width/2, window_height*3/4))
            window.blit(enter_text, enter_pos)

            # Update the display
            pygame.display.flip()

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
                    if event.button == 1:  # Left mouse button
                        key_wait = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
        level = 0
        score = 0
        nexustype = NEXUS_TYPE_PMEC
        nexus_speed = 5
        nexus_magnitude = 5
        gamestate = GAME_STATE_INITLEVEL

    ###############
    # Check how the player is doing
    if gamestate == GAME_STATE_RUNLEVEL and sum(deercaught) + sum(deerlost) == 15:
        # This level is complete!
        # Animation of the Nexus server growing larger
        scale_factor = 1
        brightness = 1
        while scale_factor < 5.0:
            # Clear the window
            dim_image = adjust_brightness(background_image, brightness)
            window.blit(dim_image, (0, 0))
            brightness -= 0.04

            # Draw the Nexus server with the scaled size
            if nexustype == NEXUS_TYPE_PMEC:
                image = pmec_image
            elif nexustype == NEXUS_TYPE_3RACK:
                image = rack3_image
            elif nexustype == NEXUS_TYPE_10RACK:
                image = rack10_image

            scaled_nexus_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), (int(image.get_width() * scale_factor))))

            # Calculate the position to center the Nexus
            nexus_x = window_width / 2 - scaled_nexus_image.get_width() / 2
            nexus_y = window_height / 2 - scaled_nexus_image.get_height() / 2

            # Blit the scaled Nexus image onto the window
            window.blit(scaled_nexus_image, (nexus_x, nexus_y))

            # Update the display
            pygame.display.flip()

            # Increase the scale factor
            scale_factor += 0.5
            time.sleep(0.01)

        # Display "Level Complete!" text
        level_complete_font = pygame.font.Font(None, 100)
        level_complete_text = level_complete_font.render("Level Complete!", True, (255, 255, 255))
        level_complete_pos = level_complete_text.get_rect(center=(window_width / 2, window_height / 6))
        window.blit(level_complete_text, level_complete_pos)
        
        # Display "You caught: x deer" text in the center of the screen in a medium sized font
        caught_text = level_font.render("You caught: " + str(sum(deercaught)) + " deer", True, (255, 255, 255))
        caught_pos = caught_text.get_rect(center=(window_width / 2, window_height * 3 / 4))
        window.blit(caught_text, caught_pos)

        if sum(deercaught) >= 8:
            if nexustype == NEXUS_TYPE_PMEC:
                summary_text = level_font.render("has arrived for you to use next time.", True, (255, 255, 255))         
                summary_pos = summary_text.get_rect(center=(window_width / 2, window_height * 3 / 4 + 60))
                window.blit(summary_text, summary_pos)
                summary_text = level_font.render("That's pretty good! A 3-rack Nexus", True, (255, 255, 255))         
            elif nexustype == NEXUS_TYPE_3RACK:
                summary_text = level_font.render("has arrived for you to use next time.", True, (255, 255, 255))         
                summary_pos = summary_text.get_rect(center=(window_width / 2, window_height * 3 / 4 + 60))
                window.blit(summary_text, summary_pos)
                summary_text = level_font.render("Feel the power of Nexus! A big Nexus", True, (255, 255, 255))
            else:
                summary_text = level_font.render("Good stuff!", True, (255, 255, 255))
            summary_pos = summary_text.get_rect(center=(window_width / 2, window_height * 3 / 4 + 30))
            window.blit(summary_text, summary_pos)

            level += 1
            nexustype += 1
            nexustype = min(nexustype, NEXUS_TYPE_10RACK)
            nexus_speed += 2
            nexus_magnitude += 5
            score += 1000 + 500 * level
            gamestate = GAME_STATE_INITLEVEL
        elif sum(deercaught) > 5:
            summary_text = level_font.render("Not so good - no upgrades for you.", True, (255, 255, 255))
            summary_pos = summary_text.get_rect(center=(window_width / 2, window_height * 3 / 4 + 60))
            window.blit(summary_text, summary_pos)
            level += 1
            score += 500
            gamestate = GAME_STATE_INITLEVEL
        else:
            summary_text = level_font.render("Lost your glasses? Your journey ends here.", True, (255, 255, 255))
            summary_pos = summary_text.get_rect(center=(window_width / 2, window_height * 3 / 4 + 60))
            window.blit(summary_text, summary_pos)
            gamestate = GAME_STATE_ENDED

        enter_text = level_font.render("Press Enter or left-click.", True, (255, 255, 255))
        enter_pos = enter_text.get_rect(center=(window_width/2, window_height*3/4 + 120))
        window.blit(enter_text, enter_pos)

        # Update the display
        pygame.display.flip()

        key_wait = True
        while key_wait:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        key_wait = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        key_wait = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    ###############
    # HANDLE EVENTS
    for event in pygame.event.get():
        # Handle the quit event
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and ((event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL) or event.key == pygame.K_q)):
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            # Find a deer that is not caught and not lost
            available_deer = [i for i in range(15) if not deercaught[i] and not deerlost[i]]
            if available_deer:
                # Select a random deer from the available ones
                selected_deer = random.choice(available_deer)
                # Move the selected deer next to the castle
                deerpos[selected_deer] = [random.randint(0, int(window_width / 3 - 50)), random.randint(0, int(window_height / 2 - 50))]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            # Find a deer that is not caught and not lost
            available_deer = [i for i in range(15) if not deercaught[i] and not deerlost[i]]
            if available_deer:
                # Select a random deer from the available ones
                selected_deer = random.choice(available_deer)
                # Move the selected deer next to the castle
                deerpos[selected_deer] = [window_width + 60, window_height + 60]

    # Update the display
    pygame.display.flip()