#!/usr/bin/env python
'''
Created on Apr 22, 2016

@author: mmartin
'''

from piece import piece_factory
import random

from statics import COLUMNS, PIECES

def is_odd(num):
    return num & 0x1

class Board(object):

    def __init__(self, empty=True):

        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        self._pawns = 0
        self._rooks = 0
        self._knights = 0
        self._bishops = 0
        self._queens = 0
        self._kings = 0
        self.pieces = PIECES.keys()
        self.board = {}
        if empty:
            for column in range(ord('a'), ord('i')):
                for row in range(1, 9):
                    node = '%c%d' % (chr(column), row)
                    if (is_odd(row) and is_odd(column)) or \
                       (not is_odd(row) and not is_odd(column)):
                        color = 'black'
                    else:
                        color = 'white'

                    self.board[node] = {'color': color, 'piece': None, 'visited': False}
        else:
            # here is where we would populate a brand new game on the board
            pass
        # print self.board

    def create_random_piece(self):
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
            return self.create_random_piece()
        return new_piece

    def get_random_node(self):
        row = random.randint(1, 8)
        col = random.randint(1, 8)
        if self.board['%c%d' % (chr(col + 0x60), row)]['piece']:  # already occupied?
            return self.get_random_node()
        else:
            return '%c%d' % (chr(col + 0x60), row)

    def has_been_visited(self, node):
        return self.board[node]['visited']

    def is_valid_move(self, from_node, to_node):
        ok_move = True

        if not self.is_valid_position(to_node):
            print('To position %s is off the board' % to_node)
            ok_move = False

        if not self.is_valid_position(from_node):
            print('From position %s is off the board' % from_node)
            ok_move = False

        return(ok_move)

    def is_valid_position(self, node):
        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        col = node[0]
        row = node[1]
        if (int(row) in range(1, 9)) and (ord(col) in range(ord('a'), ord('i'))):
            return True  # Position is OK
        else:
            print('Error: position %s is off the board' % node)
            return False

    def populate_random(self, num):
        random.seed()
        for _i in range(1, num + 1):
            node = self.get_random_node()
            new_piece = self.create_random_piece()
            self.set_piece(piece_factory(new_piece, color='black'), node)

    def print_board(self):
        cols = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        row = 0
        print('  +-------+-------+-------+-------+-------+-------+-------+--------+')
        for c in cols:
            print(' '),
            print('|       ') * 8,
            print('|')
            row += 1
            print(row),
            rowdict = {k: v for k, v in self.board.items() if k.startswith(c)}
            for r in sorted(rowdict):
                if rowdict[r]['piece']:
                    color = rowdict[r]['piece'].get_color()[0]
                    ptype = rowdict[r]['piece'].get_type()
                    if ptype == 'knight':
                        ptype = 'kn'
                    else:
                        ptype = '%c ' % ptype[0]
                    print('| %c %s ' % (color, ptype)),
                else:
                    print('|      '),
            print(' |')
            print(' '),
            print('|       ') * 8,
            print('|')
            print('  +-------+-------+-------+-------+-------+-------+-------+--------+')
        print('      A       B       C       D       E       F       G        H')

    def remove_piece(self, node):
        self.board[node]['piece'] = None

    def set_piece(self, piece, node):
        self.board[node]['piece'] = piece
        if piece.get_position():
            self.board[piece.get_position()]['piece'] = None
        piece.set_position(node)

    def visit_node(self, node):
        self.board[node]['visited'] = True
