'''
Created on Apr 22, 2016

@author: mmartin
'''

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
    '''
    An object factory for chess pieces
    '''
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
        self.piece = piece
        self.color = color
        self.position = ''

    def get_color(self):
        return self.color

    def get_type(self):
        return self.piece

    def get_position(self):
        '''
        Get the board position of this piece
        '''
        return self.position

    def set_position(self, position):
        '''
        Set the board position of this piece
        '''
        self.position = position

    def diagonal_moves(self):
        '''
        Calculate all possible diagonal moves for this piece
        '''
        position = self.position
        from_col = ord(position[0]) - 0x60
        from_row = int(position[1])
        ldiag = []
        rdiag = []
        for move in range(1, 9):
            col = from_col + move
            row = from_row + move
            if col < 9 and col != from_col and row < 9:
                rdiag.append('%c%d' % (chr(col + 0x60), row))
            col = from_col - move
            row - from_row + move
            if col > 0 and col != from_col and row < 9:
                ldiag.append('%c%d' % (chr(col + 0x60), row))
            col = from_col + move
            row = from_row - move
            if col < 9 and col != from_col and row > 0:
                ldiag.append('%c%d' % (chr(col + 0x60), row))
            col = from_col - move
            row = from_row - move
            if col > 0 and col != from_col and row > 0:
                rdiag.append('%c%d' % (chr(col + 0x60), row))
        valid_moves = rdiag + ldiag
        return (sorted(valid_moves), sorted(rdiag), sorted(ldiag))

    def vertical_moves(self, board):
        '''
        Calculate all possible horizontal moves for this piece
        '''
        valid_moves = []
        position = self.position
        from_row = int(position[1])
        for move in range(from_row, 9):
            if move != from_row:  # Horizontal moves
                new_pos = '%c%d' % (position[0], move)
                valid_moves.append(new_pos)
        for move in range(from_row, 0, -1):
            if move != from_row:  # Horizontal moves
                new_pos = '%c%d' % (position[0], move)
                valid_moves.append(new_pos)
        return sorted(valid_moves)

    def horizontal_moves(self, board):
        '''
        Calculate all possible horizontal moves for this piece
        '''
        valid_moves = []
        position = self.position
        from_col = ord(position[0]) - 0x60
        from_row = int(position[1])
        for move in range(from_col, 9):
            if move != from_col:  # Vertical moves
                new_pos = '%c%d' % (chr(move + 0x60), from_row)
                valid_moves.append(new_pos)
        for move in range(from_col, 0, -1):
            if move != from_col:  # Vertical moves
                new_pos = '%c%d' % (chr(move + 0x60), from_row)
                valid_moves.append(new_pos)
        return sorted(valid_moves)

class King(Piece):
    '''
    A king piece
    '''

    def legal_moves(self, board):
        print('Not implemented')

class Queen(Piece):
    '''
    A queen piece
    '''

    def legal_moves(self, board):
        valid_moves = self.horizontal_moves(board)
        valid_moves.extend(self.vertical_moves(board))
        valid_moves.extend(self.diagonal_moves())
        return sorted(valid_moves)

class Bishop(Piece):
    '''
    a bishop piece
    '''

    def legal_moves(self, board):
        return self.diagonal_moves()


class Knight(Piece):
    '''
    a knight piece
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

    def legal_moves(self, board):
        valid_moves = []
        position = self.position
        from_col = ord(position[0]) - 0x60
        from_row = int(position[1])
        for move in self.MOVE_DIRECTIONS:
            row = from_row + int(move[1])
            col = chr((from_col + int(move[0]) + 0x60))
            if row in range(1, 9) and col in COLUMNS:
                valid_moves.append('%c%d' % (col, row))
        return sorted(valid_moves)

class Rook(Piece):
    '''
    A rook piece
    '''
    def legal_moves(self, board):
        valid_moves = self.horizontal_moves(board)
        valid_moves.extend(self.vertical_moves(board))
        return valid_moves


class Pawn(Piece):
    '''
    A pawn piece
    '''

    def legal_moves(self, board):
        print('Not implemented')
