#!/usr/bin/python
'''
Created on April 22, 2016

@author: mmartin
'''

import getopt
import sys

from board import Board
from piece import Piece, PIECES, piece_factory

VERSION = '1.0.0'

verbose = False

class Chessercise(object):
    '''
    Part 1 of the Inmar Technical Test
    '''
    def __init__(self, board, piece, position):
        self.board = board
        self.piece = piece
        self.position = position

    def show_moves(self, piece, position):
        '''
        Show all possible moves for this piece, from this position.
        '''
        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        return piece.legal_moves()

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
        piece.set_position(in_position)
    else:
        print('Failed on position %s' % in_position)
        sys.exit(1)

    obj = Chessercise(board, piece, in_position)
    if target:
        pass
    else:
        moves = obj.show_moves(piece, in_position)

    print moves

if __name__ == '__main__':
    main(sys.argv[1:])
