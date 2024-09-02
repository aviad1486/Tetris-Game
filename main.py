import pygame, sys
from game import Game
from features import Features

pygame.init()

screen = pygame.display.set_mode((1100, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

previous_scores = []

is_paused = False

features = Features(screen, game, previous_scores, is_paused)

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                is_paused = not is_paused  
                features.is_paused = is_paused  
            if not is_paused:  
                if game.game_over:
                    previous_scores.append(game.score) 
                    game.game_over = False
                    game.reset()
                if event.key == pygame.K_LEFT and not game.game_over:
                    game.move_left()
                if event.key == pygame.K_RIGHT and not game.game_over:
                    game.move_right()
                if event.key == pygame.K_DOWN and not game.game_over:
                    game.move_down()
                    game.update_score(0, 1) # increasing the score if the user dropping the blocks faster
                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate()
        if event.type == GAME_UPDATE and not game.game_over and not is_paused:
            game.move_down()

    # Drawing
    features.draw()
    clock.tick(60)
