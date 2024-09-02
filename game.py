from grid import Grid
from blocks import *
import random

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(),JBlock(),LBlock(),OBlock(),SBlock(),TBlock(),ZBlock()]
        self.current_block = self.get_random_block() # the block currently falling
        self.next_block = self.get_random_block() # the next block to be dropped
        self.game_over = False
        self.score = 0

    def update_score(self,lines_cleared,move_down_points):
         # update the score based on the number of lines cleared and any points from moving down
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score+= 300
        elif lines_cleared == 3:
            self.score+= 500
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0,-1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0,1)

    def move_right(self):
        self.current_block.move(0,1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0,-1)

    def move_down(self):
        self.current_block.move(1,0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1,0)
            self.lock_block()

    # lock the current block into the grid and prepare the next block
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            # place the block's cells into the grid
            self.grid.grid[position.row][position.column] = self.current_block.id
        # replace the current block with the next block
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        # clear any full rows and update the score
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared,0)
        # check if the new block can be placed; if not, the game is over
        if self.block_fits() == False:
            self.game_over = True

    def reset(self):
        self.grid.reset()
        # reinitialize the list of blocks and select the first and next blocks
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        # check if the current block fits into the grid (no collisions)
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row,tile.column) ==  False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            # undo the rotation if it goes out of bounds or causes a collision
            self.current_block.undo_rotation()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row,tile.column) == False:
                return False
        return True
    
    def draw(self,screen):
        self.grid.draw(screen)
        self.current_block.draw(screen,11,11)

        if isinstance(self.next_block, IBlock):
            self.next_block.draw(screen, 255, 290)  # adjusted for IBlock
        elif isinstance(self.next_block, OBlock):
            self.next_block.draw(screen, 255, 285)  # adjusted for OBlock
        else:
            self.next_block.draw(screen, 270, 270) # default adjustment for other blocks