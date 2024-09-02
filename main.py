import pygame, sys, asyncio
from game import Game
from features import Features

pygame.init()

# set up the display window for the game
screen = pygame.display.set_mode((1100, 620))
pygame.display.set_caption("Python Tetris")

# initialize the game clock for controlling the frame rate
clock = pygame.time.Clock()

async def main():
    game = Game()

    # list to store the scores from previous games for the scoreboard
    previous_scores = []

    # variable to track if the game is paused
    is_paused = False

    # instantiate the Features class to manage UI elements
    features = Features(screen, game, previous_scores, is_paused)

    # Custom event to update the game state at a regular interval
    GAME_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(GAME_UPDATE, 200)

    while True:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    is_paused = not is_paused  # Toggle the paused state
                    features.is_paused = is_paused  # Update the paused state in Features
                if not is_paused:  # Only allow controls if the game is not paused
                    if game.game_over:
                        previous_scores.append(game.score)  # adding scoreboard
                        game.game_over = False
                        game.reset()
                    # handle block movement and rotation based on arrow key inputs   
                    if event.key == pygame.K_LEFT and not game.game_over:
                        game.move_left()
                    if event.key == pygame.K_RIGHT and not game.game_over:
                        game.move_right()
                    if event.key == pygame.K_DOWN and not game.game_over:
                        game.move_down()
                        game.update_score(0, 1) # increase the score slightly for each move down
                    if event.key == pygame.K_UP and not game.game_over:
                        game.rotate()
            if event.type == GAME_UPDATE and not game.game_over and not is_paused:
                # automatically move the block down at each GAME_UPDATE event
                game.move_down()

        # draw the game and UI elements on the screen
        features.draw()
        clock.tick(60) # limit the frame rate to 60 FPS
        await asyncio.sleep(0)

asyncio.run(main())
