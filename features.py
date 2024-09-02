import pygame
from colors import Colors

# initialize the UI features of the game
class Features:
    def __init__(self, screen, game, previous_scores, is_paused):
        self.screen = screen
        self.game = game # reference to the game object for accessing its state
        self.previous_scores = previous_scores
        self.is_paused = is_paused

        # fonts used for displaying text
        self.title_font = pygame.font.Font(None, 40)
        self.smaller_font = pygame.font.Font(None, 25)

        # captions and their positions on the screen
        self.captions = [
            {"text": "Score", "surface": self.title_font.render("Score", True, Colors.white), "pos": (365, 20)},
            {"text": "Next", "surface": self.title_font.render("Next", True, Colors.white), "pos": (375, 180)},
            {"text": "Guide", "surface": self.title_font.render("Guide", True, Colors.white), "pos": (900, 20)},
            {"text": "Scoreboard", "surface": self.title_font.render("Scoreboard", True, Colors.white), "pos": (570, 20)},
            {"text": "Move Left - L-Arrow", "surface": self.smaller_font.render("Move Left - L-Arrow", True, Colors.white), "pos": (833, 65)},
            {"text": "Move Right - R-Arrow", "surface": self.smaller_font.render("Move Right - R-Arrow", True, Colors.white), "pos": (833, 105)},
            {"text": "Rotate - UP-Arrow", "surface": self.smaller_font.render("Rotate - UP-Arrow", True, Colors.white), "pos": (833, 145)},
            {"text": "Drop - DOWN-Arrow", "surface": self.smaller_font.render("Drop - DOWN-Arrow", True, Colors.white), "pos": (833, 185)},
            {"text": "Pause/Resume - P", "surface": self.smaller_font.render("Pause/Resume - P", True, Colors.white), "pos": (833, 225)},
        ]

        # rectangles that serve as background elements for text and UI sections
        self.rectangles = [
            {"name": "scoreboard", "rect": pygame.Rect(525, 55, 250, 500)},
            {"name": "score", "rect": pygame.Rect(320, 55, 170, 60)},
            {"name": "next", "rect": pygame.Rect(320, 215, 170, 180)},
            {"name": "pause", "rect": pygame.Rect(320, 290, 170, 60)},
            {"name": "guide", "rect": pygame.Rect(813, 55, 250, 200)},
        ]

        # load the background image for the game
        self.background_image = pygame.image.load('background.png')

    def draw(self):
        # draw the background image on the screen
        self.screen.blit(self.background_image, (0, 0))

        # draw rectangles for UI sections
        for rect in self.rectangles:
            pygame.draw.rect(self.screen, Colors.dark_grey, rect["rect"], 0, 10)

         # draw captions for various UI elements
        for caption in self.captions:
            self.screen.blit(caption["surface"], caption["pos"])

        # display the current score inside the score rectangle
        score_value_surface = self.title_font.render(str(self.game.score), True, Colors.white)
        score_rect = self.rectangles[1]["rect"]  # The "score" rectangle
        self.screen.blit(score_value_surface,
                         score_value_surface.get_rect(centerx=score_rect.centerx, centery=score_rect.centery))

        # display "GAME OVER" text if the game is over
        if self.game.game_over:
            game_over_surface = self.title_font.render("GAME OVER", True, Colors.white)
            self.screen.blit(game_over_surface, (320, 450))
        # display "PAUSED" text if the game is paused
        elif self.is_paused:
            pause_surface = self.title_font.render("PAUSED", True, Colors.white)
            self.screen.blit(pause_surface, (320, 450))

        # display the top 10 previous scores on the scoreboard
        sorted_scores = sorted(self.previous_scores, reverse=True)
        for index, score in enumerate(sorted_scores[:10]):  # Display the top 10 scores
            score_text = self.title_font.render(f"Score {index + 1}: {score}", True, Colors.white)
            self.screen.blit(score_text, (530, 70 + index * 40))

        self.game.draw(self.screen)

        # update the display with all the drawn elements
        pygame.display.update()
