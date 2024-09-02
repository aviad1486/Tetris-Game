from block import Block
from position import Position

class LBlock(Block):
    def __init__(self):
        # initialize the L-shaped block with its specific rotations
        super().__init__(id = 1)
        # define the block's shape for each rotation state (0 to 3)
        self.cells = {
            0:[Position(0,2),Position(1,0),Position(1,1),Position(1,2)],
            1:[Position(0,1),Position(1,1),Position(2,1),Position(2,2)],
            2:[Position(1,0),Position(1,1),Position(1,2),Position(2,0)],
            3:[Position(0,0),Position(0,1),Position(1,1),Position(2,1)]
        }
        # initial position adjustment for the LBlock
        self.move(0,3)

class JBlock(Block):
    def __init__(self):
        # initialize the J-shaped block with its specific rotations
        super().__init__(id = 2)
        # define the block's shape for each rotation state (0 to 3)
        self.cells = {
            0:[Position(0,0),Position(1,0),Position(1,1),Position(1,2)],
            1:[Position(0,1),Position(0,2),Position(1,1),Position(2,1)],
            2:[Position(1,0),Position(1,1),Position(1,2),Position(2,2)],
            3:[Position(0,1),Position(1,1),Position(2,0),Position(2,1)]
        }
        # initial position adjustment for the JBlock
        self.move(0, 3)

class IBlock(Block):
    def __init__(self):
        # initialize the I-shaped block with its specific rotations
        super().__init__(id = 3)
        # define the block's shape for each rotation state (0 to 3)
        self.cells = {
            0:[Position(1,0),Position(1,1),Position(1,2),Position(1,3)],
            1: [Position(0, 2), Position(1, 2), Position(2, 2), Position(3, 2)],
            2: [Position(2, 0), Position(2, 1), Position(2, 2), Position(2, 3)],
            3: [Position(0, 1), Position(1, 1), Position(2, 1), Position(3, 1)]
        }
        # initial position adjustment for the IBlock
        self.move(-1, 3)

class OBlock(Block):
    def __init__(self):
        # initialize the O-shaped block with its specific rotations (only one)
        super().__init__(id = 4)
        # define the block's shape for the single rotation state
        self.cells = {
            0:[Position(0,0),Position(0,1),Position(1,0),Position(1,1)]
        }
        # initial position adjustment for the OBlock
        self.move(0, 4)

class SBlock(Block):
    def __init__(self):
        # initialize the S-shaped block with its specific rotations
        super().__init__(id = 5)
        # define the block's shape for each rotation state (0 to 3)
        self.cells = {
            0:[Position(0,1),Position(0,2),Position(1,0),Position(1,1)],
            1:[Position(0,1),Position(1,1),Position(1,2),Position(2,2)],
            2:[Position(1,1),Position(1,2),Position(2,0),Position(2,1)],
            3:[Position(0,0),Position(1,0),Position(1,1),Position(2,1)]
        }
        # initial position adjustment for the SBlock
        self.move(0, 3)

class TBlock(Block):
    def __init__(self):
        # initialize the T-shaped block with its specific rotations
        super().__init__(id = 6)
        # define the block's shape for each rotation state (0 to 3)
        self.cells = {
            0:[Position(0,1),Position(1,0),Position(1,1),Position(1,2)],
            1:[Position(0,1),Position(1,1),Position(1,2),Position(2,1)],
            2:[Position(1,0),Position(1,1),Position(1,2),Position(2,1)],
            3:[Position(0,1),Position(1,0),Position(1,1),Position(2,1)]
        }
        # initial position adjustment for the TBlock
        self.move(0, 3)

class ZBlock(Block):
    def __init__(self):
        # initialize the Z-shaped block with its specific rotations
        super().__init__(id = 7)
        # define the block's shape for each rotation state (0 to 3)
        self.cells = {
            0:[Position(0,0),Position(0,1),Position(1,1),Position(1,2)],
            1:[Position(0,2),Position(1,1),Position(1,2),Position(2,1)],
            2:[Position(1,0),Position(1,1),Position(2,1),Position(2,2)],
            3:[Position(0,1),Position(1,0),Position(1,1),Position(2,0)]
        }
        # initial position adjustment for the ZBlock
        self.move(0, 3)
