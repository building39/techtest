#!/usr/bin/python
'''
Created on April 22, 2016

@author: mmartin
'''

import getopt
import random
import sys

from board import Board
from piece import PIECES, piece_factory
from knight_moves import KNIGHT_MOVES

VERSION = '1.0.0'

verbose = False

class Chessercise(object):
    '''
    Part 1 of the Inmar Technical Test
    '''
    _pawns = 0
    _rooks = 0
    _knights = 0
    _bishops = 0
    _queens = 0
    _kings = 0

    def __init__(self, board, piece, position):
        self.board = board
        self.piece = piece
        self.position = position
        self.pieces = PIECES.keys()

    def _create_random_piece(self):
        new_piece = self.pieces[random.randint(0, len(self.pieces) - 1)]
        if new_piece == 'pawn' and self._pawns < 8:
            self._pawns += 1
        elif new_piece == 'rook' and self._rooks < 2:
            self._rooks += 1
        elif new_piece == 'knight' and self._knights < 2:
            self._knights += 1
        elif new_piece == 'bishop' and self._bishops < 2:
            self._bishops += 1
        elif new_piece == 'queen' and self._queens < 1:
            self._queens += 1
        elif new_piece == 'king' and self._kings < 1:
            self._kings += 1
        else:
            return self._create_random_piece()
        return new_piece

    def _get_farthest_tile(self, position):

        row = int(self.position[1])
        col = ord(self.position[0]) - 0x60
        far_col = 0
        far_row = 0

        if self.piece.get_type().lower() == 'bishop':
            far_col = 8 if col < 5 else 1
            far_row = 8 if row < 5 else 1
            far_pos = '%c%d' % (chr(far_col + 0x60), far_row)
            if self.board.board[self.position]['color'] != self.board.board[far_pos]['color']:
                far_row = (far_row + 1) if far_row == 1 else (far_row - 1)
        elif self.piece.get_type().lower() == 'pawn':
            far_col = col
            if self.piece.get_color() == 'white' and row == 2:
                far_row = 4
            elif self.piece.get_color() == 'black' and row == 7:
                far_row = 5
            else:
                far_row = (row + 1) if row < 8 else row
        elif self.piece.get_type().lower() == 'king':
            far_col = col
            far_row = (row + 1) if row < 8 else (row - 1)
        elif self.piece.get_type().lower() == 'knight':
            # this one is tricky
            if row < 5 and col < 5:
                quadrant = 1
            elif row < 5 and col > 4:
                quadrant = 2
            elif row > 4 and col < 5:
                quadrant = 3
            else:
                quadrant = 4
            if quadrant == 1:
                while col < 7:
                    row += 1
                    col += 2
            elif quadrant == 2:
                while col > 2:
                    row += 1
                    col -= 2
            elif quadrant == 3:
                while col < 7:
                    col += 2
                    row -= 1
            else:
                while col > 2:
                    col -= 2
                    row -= 1
            new_pos = '%c%d' % (chr(col + 0x60), row)
            try:
                if position == 'f5':
                    print('position %s ended at new position %s' % (position, new_pos))
                for (col_inc, row_inc) in KNIGHT_MOVES[quadrant - 1][new_pos]:
                    col += col_inc
                    row += row_inc
            except:
                print('Exception in quadrant %d position %s' % (quadrant, new_pos))
            far_row = row
            far_col = col
        elif self.piece.get_type().lower() in ['rook', 'queen']:
            far_col = 8 if col < 5 else 1
            far_row = 8 if row < 5 else 1
        far_pos = '%c%d' % (chr(far_col + 0x60), far_row)
        return (far_col, far_row, far_pos)

    def _get_random_tile(self):
        row = random.randint(1, 8)
        col = random.randint(1, 8)
        if self.board.board['%c%d' % (chr(col + 0x60), row)]['piece']:  # already occupied?
            return self._get_random_tile()
        else:
            return '%c%d' % (chr(col + 0x60), row)

    def _populate_random(self, num):
        random.seed()
        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        for _i in range(1, num + 1):
            tile = self._get_random_tile()
            new_piece = self._create_random_piece()
            self.board.set_piece(piece_factory(new_piece, color='black'), tile)

    def show_moves(self, piece, position):
        '''
        Show all possible moves for this piece, from this position.
        '''

        return piece.legal_moves()

    def target(self, piece, position):
        self.piece = piece
        self.position = position
        self._populate_random(8)

        tilecolor = self.board.board[self.position]['color']

        # compute furthest tile from our piece
        (far_col, far_row, far_pos) = self._get_farthest_tile(self.position)

        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()



def usage():
    '''
    Usage instructions.
    '''
    print ('Just a lil ol code template.')
    print ('Version : %s' % VERSION)
    print ('')
    print ('Usage: '
           '%s <options>' % sys.argv[0])
    print ('')
    print (' Command Line options:')
    print ('  --help      - Print this enlightening message')
    print ('  --piece     - Chess piece name. one of "King", "Queen", "Bishop", "Knight", "Rook", or "Pawn".')
    print ('                Case insensitive.')
    print ('  --position  - Board position in standard notation.')
    print ('  --target    - Calculate and output the minimum set of moves to the most distant tile')
    print ('')

    sys.exit(0)

def main(argv):
    '''
    Main entry point
    '''

    in_piece = ''
    in_position = ''
    target = False

    if (len(argv) < 2):
        print "Number of args: %d" % len(argv)
        usage()

    try:
        opts, _args = getopt.getopt(argv, '',
                                    ['help',
                                     'piece=',
                                     'position=',
                                     'target'])
    except getopt.GetoptError, e:
        print ('opt error %s' % e)
        print ('')
        usage()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt == '--piece':
            in_piece = arg.lower()
        elif opt == '--position':
            in_position = arg
        elif opt == '--target':
            target = True

#    sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#    import pydevd; pydevd.settrace()

    if in_piece in PIECES:
        piece = piece_factory(in_piece)
    else:
        print("Unknown piece %s" % in_piece)
        sys.exit(1)

    board = Board(empty=True)

    if board.is_valid_position(in_position):
        board.set_piece(piece, in_position)
    else:
        print('Failed on position %s' % in_position)
        sys.exit(1)

    obj = Chessercise(board, piece, in_position)
    if target:
        obj.target(piece, in_position)
    else:
        moves = obj.show_moves(piece, in_position)
        print moves

if __name__ == '__main__':
    main(sys.argv[1:])
