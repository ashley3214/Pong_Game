import pygame
import random

# Constants for the window's width and height values
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 620

# RGB values for the colors used in the game
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

def reset_game():
    global paddle_1_rect, paddle_2_rect, ball_rect, ball_accel_x, ball_accel_y, started, paddle_1_move, paddle_2_move
    # Reset the paddles' positions
    paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 - 50, 7, 100)

    # Reset the ball's position
    ball_rect = pygame.Rect(SCREEN_WIDTH / 2 - 12.5, SCREEN_HEIGHT / 2 - 12.5, 25, 25)

    # Determine the x and y speed of the ball 
    ball_accel_x = random.randint(2, 4) * 0.1
    ball_accel_y = random.randint(2, 4) * 0.1

    # Randomize the direction of the ball
    if random.randint(1, 2) == 1:
        ball_accel_x *= -1
    if random.randint(1, 2) == 1:
        ball_accel_y *= -1

    # Indicate that the game is not started
    started = False

    # Initialize the movement variables for the paddles
    paddle_1_move = 0
    paddle_2_move = 0

def main():
    global paddle_1_rect, paddle_2_rect, ball_rect, ball_accel_x, ball_accel_y, started, paddle_1_move, paddle_2_move

    # GAME SETUP
    
    # Initialize the PyGame library (this is absolutely necessary)
    pygame.init()

    # This creates the window for the game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Set the window's title
    pygame.display.set_caption('Pong')

    # Create the clock object to keep track of the time
    clock = pygame.time.Clock()
    
    # Reset the game to its initial state
    reset_game()

    # GAME LOOP
    while True:
        ''' 
        Set the background color to black
        needs to be called every time the game updates
        '''
        screen.fill(COLOR_BLACK)
        
        # Make the ball move after 3 seconds
        if not started:
            # Load the Consolas font
            font = pygame.font.SysFont('Consolas', 30)
            
            # Draw some text to the center of the screen
            text = font.render('Press Space to Start', True, COLOR_WHITE)
            text_rect = text.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_rect)
            
            # Update the display
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        started = True

            continue

        '''
        Get the time elapsed between now and the last frame
        60 is an arbitrary number but the game runs smoothly at 60 FPS
        '''
        delta_time = clock.tick(60)

        # Checking for events
        for event in pygame.event.get():
            # If the user exits the window
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # If the user is pressing a key
            if event.type == pygame.KEYDOWN:
                # PLAYER 1
                # If the key is W, set the movement of paddle_1 to go up
                if event.key == pygame.K_w:
                    paddle_1_move = -0.5

                # If the key is S, set the movement of paddle_1 to go down
                if event.key == pygame.K_s:
                    paddle_1_move = 0.5

                # PLAYER 2
                # If the key is the up arrow, set the movement of paddle_2 to go up
                if event.key == pygame.K_UP:
                    paddle_2_move = -0.5
                # If the key is the down arrow, set the movement of paddle_2 to go down
                if event.key == pygame.K_DOWN:
                    paddle_2_move = 0.5

            # If the player released a key
            if event.type == pygame.KEYUP:
                # If the key released is w or s, stop the movement of paddle_1
                if event.key == pygame.K_w or event.key == pygame.K_s: 
                    paddle_1_move = 0.0

                # If the key released is the up or down arrow, stop the movement of paddle_2
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle_2_move = 0.0

        '''
        Move paddle_1 and paddle_2 according to their `move` variables
        we also multiply the `move` variable by the delta time to keep movement consistent through frames
        '''
        paddle_1_rect.top += paddle_1_move * delta_time
        paddle_2_rect.top += paddle_2_move * delta_time

        # If paddle_1 is going out of the screen by the top, set it to the maximum to limit its movement
        if paddle_1_rect.top < 0:
            paddle_1_rect.top = 0
        
        # If paddle_1 is going out of the screen by the bottom, do the same thing   
        if paddle_1_rect.bottom > SCREEN_HEIGHT:
            paddle_1_rect.bottom = SCREEN_HEIGHT

        # Do the same thing with paddle_2
        if paddle_2_rect.top < 0:
            paddle_2_rect.top = 0
        if paddle_2_rect.bottom > SCREEN_HEIGHT:
            paddle_2_rect.bottom = SCREEN_HEIGHT      

        # If the ball is getting close to the top
        if ball_rect.top < 0:
            # Invert its vertical velocity 
            ball_accel_y *= -1
            # Add a bit of y to it to not trigger the above code again
            ball_rect.top = 0
        # Do the same thing with the bottom
        if ball_rect.bottom > SCREEN_HEIGHT:
            ball_accel_y *= -1
            ball_rect.bottom = SCREEN_HEIGHT

        # If the ball goes out of bounds, reset the game
        if ball_rect.left <= 0 or ball_rect.right >= SCREEN_WIDTH:
            reset_game()
            continue

        '''
        If paddle_1_rect collides with the ball and the ball is in front of it, 
        change the speed of the ball and make it move a little in the other way
        '''
        if paddle_1_rect.colliderect(ball_rect) and paddle_1_rect.left < ball_rect.left:
            ball_accel_x *= -1
            ball_rect.left += 5
        # Do the same with paddle_2_rect
        if paddle_2_rect.colliderect(ball_rect) and paddle_2_rect.left > ball_rect.left:
            ball_accel_x *= -1
            ball_rect.left -= 5

        # If the game is started
        if started:
            # Move the ball
            ball_rect.left += ball_accel_x * delta_time 
            ball_rect.top += ball_accel_y * delta_time

        # Draw player 1 and player 2's rects with the white color
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect)
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect)

        # Draw the ball with the white color
        pygame.draw.rect(screen, COLOR_WHITE, ball_rect)

        # Update the display (this is necessary for Pygame)
        pygame.display.update()

# Run the game
if __name__ == '__main__':
    main()
