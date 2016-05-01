#!/usr/bin/env python
'''
Created on Apr 22, 2016

@author: mmartin
'''

import sys

COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

def is_odd(num):
    return num & 0x1

class Board(object):

    def __init__(self, empty):

        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
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

    def visit_node(self, node):
        self.board[node]['visited'] = True

    def has_been_visited(self, node):
        return self.board[node]['visited']

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

    def is_valid_move(self, from_node, to_node):
        ok_move = True

        if not self.is_valid_position(to_node):
            print('To position %s is off the board' % to_node)
            ok_move = False

        if not self.is_valid_position(from_node):
            print('From position %s is off the board' % from_node)
            ok_move = False

        return(ok_move)

    def set_piece(self, piece, node):
        self.board[node]['piece'] = piece
        if piece.get_position():
            self.board[piece.get_position()]['piece'] = None
        piece.set_position(node)
