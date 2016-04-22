'''
Created on Apr 22, 2016

@author: mmartin
'''

import sys
from board import COLUMNS


PIECES = {
    'bishop': 'B',
    'knight': 'Kt',
    'king': 'K',
    'queen': 'Q',
    'rook': 'R',
    'pawn': 'P',
}

def piece_factory(piece, color='white'):

        if piece == 'king':
            return King(piece, color)
        elif piece == 'queen':
            return Queen(piece, color)
        elif piece == 'bishop':
            return Bishop(piece, color)
        elif piece == 'knight':
            return Knight(piece, color)
        elif piece == 'rook':
            return Rook(piece, color)
        elif piece == 'pawn':
            return Pawn(piece, color)
        else:
            return None

class Piece(object):
    '''
    classdocs
    '''


    def __init__(self, piece, color='white'):
        '''
        Constructor
        '''
        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        self.piece = piece
        self.color = color
        self.position = ''

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position


class King(Piece):
    '''
    classdocs
    '''

class Queen(Piece):
    '''
    classdocs
    '''

    def legal_moves(self):
        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        valid_moves = []
        position = self.position
        from_col = ord(position[0]) - 0x60
        from_row = int(position[1])
        for move in range(1, 9):
            if move != from_row:  # Horizontal moves
                valid_moves.append('%c%d' % (position[0], move))
            if move != from_col:  # Vertical moves
                valid_moves.append('%c%d' % (chr(move + 0x60), from_row))
            if move != from_row and move != from_col:  # Diagonal moves
                print('move: %d from_row: %d from_col: %d' % (move, from_row, from_col))
                new_col = '%c%d' % (chr(move + 0x60), move)
                print('New col: %s' % new_col)
                valid_moves.append('%c%d' % (chr(move + 0x60), move))

        return sorted(valid_moves)

class Bishop(Piece):
    '''
    classdocs
    '''

class Knight(Piece):
    '''
    classdocs
    '''
#
    MOVE_DIRECTIONS = [(2, 1),
                       (2, -1),
                       (1, 2),
                       (1, -2),
                       (-2, 1),
                       (-2, -1),
                       (-1, 2),
                       (-1, -2)
                       ]
    def legal_moves(self):
        valid_moves = []
        position = self.position
        from_col = ord(position[0]) - 0x60
        from_row = int(position[1])
        for move in self.MOVE_DIRECTIONS:
            row = from_row + int(move[1])
            col = chr((from_col + int(move[0]) + 0x60))
            if row in range(1, 9) and col in COLUMNS:
                valid_moves.append('%c%d' % (col, row))
        return valid_moves

class Rook(Piece):
    '''
    classdocs
    '''
    def legal_moves(self):
        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        valid_moves = []
        position = self.position
        from_col = ord(position[0]) - 0x60
        from_row = int(position[1])
        for move in range(1, 9):
            if move != from_row:  # Horizontal moves
                valid_moves.append('%c%d' % (position[0], move))
            if move != from_col:  # Vertical moves
                valid_moves.append('%c%d' % (chr(move + 0x60), from_row))

        return sorted(valid_moves)

class Pawn(Piece):
    '''
    classdocs
    '''
