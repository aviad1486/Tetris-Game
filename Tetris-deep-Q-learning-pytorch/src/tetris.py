import numpy as np
from PIL import Image
import cv2
from matplotlib import style
import torch
import random

style.use("ggplot")


class Tetris:
    piece_colors = [
        (0, 0, 0),  # Black
        (255, 255, 0),  # Yellow
        (147, 88, 254),  # Purple
        (54, 175, 144),  # Green
        (255, 0, 0),  # Red
        (102, 217, 238),  # Cyan
        (254, 151, 32),  # Orange
        (0, 0, 255)  # Blue
    ]
    # define the shapes of the pieces
    pieces = [
        [[1, 1],
         [1, 1]],

        [[0, 5, 0],
         [5, 5, 5]],

        [[0, 2, 2],
         [2, 2, 0]],

        [[7, 7, 0],
         [0, 7, 7]],

        [[6, 6, 6, 6]],

        [[0, 0, 3],
         [3, 3, 3]],

        [[4, 0, 0],
         [4, 4, 4]]
    ]

    def __init__(self, height=20, width=10, block_size=20):
        self.height = height
        self.width = width
        self.block_size = block_size

        # creating an extra board for displaying additional information
        self.extra_board = np.full((self.height * self.block_size, self.width * (self.block_size // 2), 3),
                                   fill_value=255, dtype=np.uint8)
        self.text_color = (0, 0, 0)
        self.reset()

    def reset(self):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.score = 0
        self.tetrominoes = 0
        self.cleared_lines = 0
        self.bag = list(range(len(self.pieces)))
        random.shuffle(self.bag)
        self.ind = self.bag.pop()
        self.piece = [row[:] for row in self.pieces[self.ind]]
        self.current_pos = {"x": self.width // 2 - len(self.piece[0]) // 2, "y": 0}
        self.gameover = False
        return self.get_state_properties(self.board)

    def rotate(self, piece):
        num_rows_orig = len(piece)
        num_cols_new = len(piece[0])
        rotated_array = []

        for i in range(num_cols_new):
            new_row = [0] * num_rows_orig
            for j in range(num_rows_orig):
                new_row[j] = piece[num_rows_orig - 1 - j][i]
            rotated_array.append(new_row)
        return rotated_array

    # This function calculates important features of the current game state,
    # which are passed to the Q-Learning agent.
    # these features help the agent decide what actions to take.
    def get_state_properties(self, board):
        lines_cleared, board = self.check_cleared_rows(board)
        holes = self.get_holes(board)
        bumpiness, height = self.get_bumpiness_and_height(board)

        return torch.FloatTensor([lines_cleared, holes, bumpiness, height])

    def get_holes(self, board):
        num_holes = 0
        for col in zip(*board):
            row = 0
            while row < self.height and col[row] == 0:
                row += 1
            num_holes += sum(1 for x in col[row + 1:] if x == 0) # count empty spaces below blocks
        return num_holes

    # Calculating the "bumpiness" (differences in column heights) and the total height of the board
    def get_bumpiness_and_height(self, board):
        board = np.array(board)
        mask = board != 0
        invert_heights = np.where(mask.any(axis=0), np.argmax(mask, axis=0), self.height)
        heights = self.height - invert_heights
        total_height = np.sum(heights)
        currs = heights[:-1]
        nexts = heights[1:]
        diffs = np.abs(currs - nexts)
        total_bumpiness = np.sum(diffs)
        return total_bumpiness, total_height

    # getting all possible states resulting from different piece positions and rotations
    def get_next_states(self):
        states = {}
        piece_id = self.ind
        curr_piece = [row[:] for row in self.piece]
        if piece_id == 0:  # O piece
            num_rotations = 1
        elif piece_id in (2, 3, 4): # S, Z, I pieces
            num_rotations = 2
        else: # T, L, J pieces
            num_rotations = 4

        for i in range(num_rotations):
            valid_xs = self.width - len(curr_piece[0])
            for x in range(valid_xs + 1):
                piece = [row[:] for row in curr_piece]
                pos = {"x": x, "y": 0}
                while not self.check_collision(piece, pos):
                    pos["y"] += 1
                self.truncate(piece, pos)
                board = self.store(piece, pos)
                states[(x, i)] = self.get_state_properties(board)
            curr_piece = self.rotate(curr_piece)
        return states

    def get_current_board_state(self):
        board = [row[:] for row in self.board]
        for y in range(len(self.piece)):
            for x in range(len(self.piece[y])):
                board[y + self.current_pos["y"]][x + self.current_pos["x"]] = self.piece[y][x]
        return board

    def new_piece(self):
        if not len(self.bag):
            self.bag = list(range(len(self.pieces)))
            random.shuffle(self.bag)
        self.ind = self.bag.pop()
        self.piece = [row[:] for row in self.pieces[self.ind]]
        self.current_pos = {"x": self.width // 2 - len(self.piece[0]) // 2,
                            "y": 0
                            }
        if self.check_collision(self.piece, self.current_pos):
            self.gameover = True

    # check if the piece collides with existing blocks on the board or the bottom of the grid
    def check_collision(self, piece, pos):
        future_y = pos["y"] + 1
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if future_y + y >= self.height or (self.board[future_y + y][pos["x"] + x] and piece[y][x]):
                    return True
        return False

    # handle situations where a piece overlaps with existing blocks on the board (game over scenario)
    def truncate(self, piece, pos):
        gameover = False
        last_collision_row = -1
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if self.board[pos["y"] + y][pos["x"] + x] and piece[y][x]:
                    if y > last_collision_row:
                        last_collision_row = y

        if pos["y"] - (len(piece) - last_collision_row) < 0 and last_collision_row > -1:
            while last_collision_row >= 0 and len(piece) > 1:
                gameover = True
                last_collision_row = -1
                del piece[0]
                for y in range(len(piece)):
                    for x in range(len(piece[y])):
                        if self.board[pos["y"] + y][pos["x"] + x] and piece[y][x] and y > last_collision_row:
                            last_collision_row = y
        return gameover

    # store the piece on the board once it has landed
    def store(self, piece, pos):
        board = [row[:] for row in self.board]
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x] and not board[y + pos["y"]][x + pos["x"]]:
                    board[y + pos["y"]][x + pos["x"]] = piece[y][x]
        return board

    def check_cleared_rows(self, board):
        to_delete = []
        for i, row in enumerate(board[::-1]):
            if 0 not in row:
                to_delete.append(len(board) - 1 - i)
        if to_delete:
            board = self.remove_row(board, to_delete)
        return len(to_delete), board

    # remove cleared rows and add empty rows at the top
    def remove_row(self, board, indices):
        for i in indices[::-1]:
            del board[i]
            board = [[0] * self.width] + board
        return board

    def step(self, action, render=True, video=None):
        # unpack the action tuple into x (horizontal position) and num_rotations (number of rotations to apply)
        x, num_rotations = action

        # set the initial position of the current piece based on the provided x-coordinate
        self.current_pos = {"x": x, "y": 0}

        # apply the specified number of rotations to the current piece
        for i in range(num_rotations):
            self.piece = self.rotate(self.piece)

        # move the piece down until it collides with either another piece or the bottom of the grid
        while not self.check_collision(self.piece, self.current_pos):
            self.current_pos["y"] += 1
            if render:
                self.render(video)  # render the game state at each step if rendering is enabled

        # once a collision is detected, handle potential overflow (if the piece extends beyond the top of the grid)
        overflow = self.truncate(self.piece, self.current_pos)
        if overflow:
            self.gameover = True  # mark the game as over if there's an overflow

        # store the piece on the board in its final position
        self.board = self.store(self.piece, self.current_pos)

        # check for any full rows and clear them; update the board and count of cleared lines
        lines_cleared, self.board = self.check_cleared_rows(self.board)

        # calculate the score for this step:
        # - the base score is 1 point for placing a piece
        # - additional points are awarded based on the square of the number of cleared lines
        score = 1 + (lines_cleared ** 2) * self.width
        self.score += score  # update the total score
        self.tetrominoes += 1  # increment the count of placed tetrominoes
        self.cleared_lines += lines_cleared  # update the total cleared lines

        # if the game is not over, generate a new piece
        if not self.gameover:
            self.new_piece()

        # apply a penalty if the game is over
        if self.gameover:
            self.score -= 2

        # return the score for this step and the game over status
        return score, self.gameover

    def render(self, video=None):
        if not self.gameover:
            img = [self.piece_colors[p] for row in self.get_current_board_state() for p in row]
        else:
            img = [self.piece_colors[p] for row in self.board for p in row]
        img = np.array(img).reshape((self.height, self.width, 3)).astype(np.uint8)
        img = img[..., ::-1]  # convert RGB to BGR for OpenCV
        img = Image.fromarray(img, "RGB")

        img = img.resize((self.width * self.block_size, self.height * self.block_size), 0)
        img = np.array(img)
        img[[i * self.block_size for i in range(self.height)], :, :] = 0
        img[:, [i * self.block_size for i in range(self.width)], :] = 0

        img = np.concatenate((img, self.extra_board), axis=1)

        cv2.putText(img, "Score:", (self.width * self.block_size + self.block_size // 2, self.block_size),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=self.text_color)
        cv2.putText(img, str(self.score),
                    (self.width * self.block_size + self.block_size // 2, 2 * self.block_size),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=self.text_color)

        cv2.putText(img, "Blocks:", (self.width * self.block_size + self.block_size // 2, 4 * self.block_size),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=self.text_color)
        cv2.putText(img, str(self.tetrominoes),
                    (self.width * self.block_size + self.block_size // 2, 5 * self.block_size),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=self.text_color)

        cv2.putText(img, "Clears:", (self.width * self.block_size + self.block_size // 2, 7 * self.block_size),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=self.text_color)
        cv2.putText(img, str(self.cleared_lines),
                    (self.width * self.block_size + self.block_size // 2, 8 * self.block_size),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.0, color=self.text_color)

        if video:
            video.write(img)

        cv2.imshow("Deep Q-Learning Tetris", img)
        cv2.waitKey(1)
