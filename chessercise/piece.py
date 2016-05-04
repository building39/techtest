'''
Created on Apr 22, 2016

@author: mmartin
'''
from statics import COLUMNS


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
        self.node = ''

    def get_color(self):
        return self.color

    def get_type(self):
        return self.piece

    def get_node(self):
        '''
        Get the board node of this piece
        '''
        return self.node

    def set_node(self, node):
        '''
        Set the board node of this piece
        '''
        self.node = node

    def diagonal_moves(self):
        '''
        Calculate all possible diagonal moves for this piece
        '''
        node = self.node
        from_col = ord(node[0]) - 0x60
        from_row = int(node[1])
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
        node = self.node
        from_row = int(node[1])
        for move in range(from_row, 9):
            if move != from_row:  # Horizontal moves
                new_pos = '%c%d' % (node[0], move)
                valid_moves.append(new_pos)
        for move in range(from_row, 0, -1):
            if move != from_row:  # Horizontal moves
                new_pos = '%c%d' % (node[0], move)
                valid_moves.append(new_pos)
        return sorted(valid_moves)

    def horizontal_moves(self, board):
        '''
        Calculate all possible horizontal moves for this piece
        '''
        valid_moves = []
        node = self.node
        from_col = ord(node[0]) - 0x60
        from_row = int(node[1])
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
        horz = self.horizontal_moves(board)
        vert = self.vertical_moves(board)
        (_, rdiag, ldiag) = self.diagonal_moves()
        allm = horz + vert + rdiag + ldiag
        horz = sorted(horz)
        vert = sorted(vert)
        rdiag = sorted(rdiag)
        ldiag = sorted(ldiag)
        allm = sorted(allm)
        return (allm, horz, vert, rdiag, ldiag)

class Bishop(Piece):
    '''
    a bishop piece
    '''

    def legal_moves(self, board):
        (allm, rdiag, ldiag) = self.diagonal_moves()
        return (allm, [], [], rdiag, ldiag)


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
        node = self.node
        from_col = ord(node[0]) - 0x60
        from_row = int(node[1])
        for move in self.MOVE_DIRECTIONS:
            row = from_row + int(move[1])
            col = chr((from_col + int(move[0]) + 0x60))
            if row in range(1, 9) and col in COLUMNS:
                valid_moves.append('%c%d' % (col, row))
        return (sorted(valid_moves), [], [], [], [])

class Rook(Piece):
    '''
    A rook piece
    '''
    def legal_moves(self, board):
        horz = self.horizontal_moves(board)
        vert = self.vertical_moves(board)
        allm = horz + vert
        return (allm, horz, vert, [], [])


class Pawn(Piece):
    '''
    A pawn piece
    '''

    def legal_moves(self, board):
        print('Not implemented')
