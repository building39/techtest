#!/usr/bin/env python
'''
Created on Apr 22, 2016

@author: mmartin
'''

import sys

COLUMNS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

class Board(object):

    def __init__(self, empty):

        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        self.board = {}
        if empty:
            for column in range(ord('a'), ord('i')):
                for row in range(1, 9):
                    self.board['%c%d' % (chr(column), row)] = None
        else:
            # here is where we would populate a brand new game on the board
            pass
        # print self.board

    def is_valid_position(self, pos):
        # sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        # import pydevd; pydevd.settrace()
        col = pos[0]
        row = pos[1]
        if (int(row) in range(1, 9)) and (ord(col) in range(ord('a'), ord('i'))):
            return True  # Position is OK
        else:
            print('Error: position %s is off the board' % pos)
            return False

    def is_valid_move(self, from_pos, to_pos):
        ok_move = True

        if not self.is_valid_position(to_pos):
            print('To position %s is off the board' % to_pos)
            ok_move = False

        if not self.is_valid_position(from_pos):
            print('From position %s is off the board' % from_pos)
            ok_move = False

        return(ok_move)

    def set_piece(self, piece, position):
        self.board[position] = piece
        piece.set_position(position)
