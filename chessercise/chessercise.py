#!/usr/bin/python
'''
Created on April 22, 2016

@author: mmartin
'''

import copy
import getopt
import random
import sys

from board import Board
from piece import PIECES, piece_factory
from dns import reversename

VERSION = '1.0.0'

INCREMENT = [ (),
              (1, 1),
              (-1, 1),
              (1, -1),
             (-1, -1)
            ]

def get_next_cell(cell, inc_tuple):
    row = int(cell[1]) + 1
    col = ord(cell[0]) + 0x60 + 1
    if row > 0 and row < 9 and col > 0 and col < 9:
        return '%c%d' % (chr(col), row)
    else:
        return None

def split_list(l, idx):
    l1 = l[:idx]
    l2 = l[idx + 1:]
    return l1 + l2


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

    def __init__(self, board, piece, position, verbose=False):
        self.board = board
        self.piece = piece
        self.position = position
        self.verbose = verbose
        self.pieces = PIECES.keys()
        self.deadends = []
        self.path_list = []
        self.path = []
        self.cur_pos = ''
        self.recursion_depth = 0
        self.max_recursion_depth = 0
        self.shutting_down = False
        self.min_path_length = 0

    def _bishop_moves(self):
        # adjust target to match color of tile on which the bishop sits.
        if self.board.board[self.target_node]['color'] != self.board.board[self.orig_pos]['color']:
            row = int(self.target_node[1])
            if self.quadrant in [1, 2]:
                self.target_node = '%c%d' % (self.target_node[0], row - 1)
            else:
                self.target_node = '%c%d' % (self.target_node[0], row + 1)

        self.save_board = copy.deepcopy(self.board)
        moves = self.show_moves(self.piece, self.cur_pos)

        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)
        self.diagonal_shortest_path(moves)

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

    def _get_farthest_tile(self, pos):

        row = int(pos[1])
        col = ord(pos[0]) - 0x60
        quadrant = None
        target = None
        if row < 5 and col < 5:
            quadrant = 1
            target = 'h8'
        elif row < 5 and col > 4:
            quadrant = 2
            target = 'a8'
        elif row > 4 and col < 5:
            quadrant = 3
            target = 'h1'
        else:
            quadrant = 4
            target = 'a1'
        self.quadrant = quadrant
        self.target_node = target
        return (quadrant, target)

    def _get_max_horz(self, target):
        moves = self.piece.horizontal_moves(self.board)
        move = ''
        if moves[-1] == target:
            move = moves[-1]
        else:
            if self.board.board[moves[-1]]['piece']:
                if len(moves) > 1:
                    move = moves[-2]
                else:
                    return None
            else:
                move = moves[-1]
        if move > self.piece.get_position():
            return move
        else:
            return None

    def _get_max_vert(self, target):
        moves = self.piece.vertical_moves(self.board)
        move = ''
        if moves[-1] == target:
            move = moves[-1]
        else:
            if self.board.board[moves[-1]]['piece']:
                if len(moves) > 1:
                    move = moves[-2]
                else:
                    return None
            else:
                move = moves[-1]
        if move > self.piece.get_position():
            return move
        else:
            return None

    def _get_random_tile(self):
        row = random.randint(1, 8)
        col = random.randint(1, 8)
        if self.board.board['%c%d' % (chr(col + 0x60), row)]['piece']:  # already occupied?
            return self._get_random_tile()
        else:
            return '%c%d' % (chr(col + 0x60), row)

    def _knight_sort(self, moves):
        alist = []
        final_list = []

        if self.quadrant in [1, 3]:
            sort_columns_reverse = True
        else:
            sort_columns_reverse = False

        if self.quadrant in [1, 2]:
            sort_rows_reverse = True
        else:
            sort_rows_reverse = False

        for i in range(0, 8):
            alist.extend([[]])

        for i in range(0, len(moves)):
            x = ord(moves[i][0]) - 0x60
            alist[x - 1].extend([moves[i]])

        alist = sorted(alist, reverse=sort_columns_reverse)

        for l in alist:
            l = sorted(l, reverse=sort_rows_reverse)
            for e in l:
                final_list.extend([e])

        return final_list

    def _populate_random(self, num):
        random.seed()
        for _i in range(1, num + 1):
            tile = self._get_random_tile()
            new_piece = self._create_random_piece()
            self.board.set_piece(piece_factory(new_piece, color='black'), tile)
            print('%s at %s' % (new_piece, tile))

    def _target_bishop(self):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()

        self.cur_pos = self.orig_pos = self.piece.get_position()
        self.path.extend([self.cur_pos])

        self._bishop_moves()

        return(self.path_list)

    def _target_king(self):
        print('King not implemented')

    def _target_knight(self):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()

        self.cur_pos = self.orig_pos = self.piece.get_position()
        self.path.extend([self.cur_pos])

        self.save_board = copy.deepcopy(self.board)

        moves = self.remove_visited_nodes(self.show_moves(self.piece, self.cur_pos)[0])

        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)
        self.knights_shortest_path(moves)
        return(self.path_list)

    def _target_pawn(self):
        print('Pawn not implemented')

    def _target_queen(self):
        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        import pydevd; pydevd.settrace()

        target_piece = piece_factory('bishop')  # we're gonna try diagonals first
        self.board.set_piece(target_piece, self.target_node)
        target_path = self.show_moves(self.piece, self.target_node)[0]
        self.board.remove_piece(self.target_node)

        self.cur_pos = self.orig_pos = self.piece.get_position()
        self.path.extend([self.cur_pos])

        # try the bishop moves first
        self._bishop_moves()

        if len(self.path_list[0]) == 1:  # can't get any shorter!
            return(self.path_list)
        if self.orig_pos not in target_path and len(self.path_list[0]) == 2:  # shortest possible path if you
            return(self.path_list)  # didn't start on the same diagonal

        # now try the horizontal and vertical paths
        self.cur_pos = self.orig_pos
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)
        self.rook(self.show_moves(self.piece, self.cur_pos))
        if len(self.path_list[0]) == 2:
            return(self.path_list)  # Shortest possible path
        # Now try the bishop moves off of the rook moves
        self.cur_pos = self.orig_pos
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)

        return(self.path_list)

    def _target_rook(self):
        self.cur_pos = self.orig_pos = self.piece.get_position()
        self.rook(self.show_moves(self.piece, self.cur_pos))
        return(self.path_list)

    def check_cell_occupied(self, cell):
        if self.board.board[cell]['piece']:
            return (self.board.board[cell]['piece'].get_type(),
                    self.board.board[cell]['piece'].get_color())
        else:
            return None

    def diagonal_shortest_path(self, moves):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()
        self.recursion_depth += 1
        self.max_recursion_depth += 1
        path = list(self.path)
        (_, _, _, rpath, lpath) = moves
        rpath = self.remove_visited_nodes(rpath)
        lpath = self.remove_visited_nodes(lpath)
        rpath = self.sort_nodes(rpath)
        lpath = self.sort_nodes(lpath)
        sys.stdout.flush()
        if self.quadrant in [1, 4]:
            primary_path = list(rpath)
        else:
            primary_path = list(lpath)

        if self.quadrant in [1, 3]:
            primary_path = sorted(primary_path, reverse=True)
        else:
            primary_path = sorted(primary_path, reverse=False)

        for p in primary_path:
            self.path = list(path)
            if p == self.orig_pos:
                continue
            nodes = list(primary_path)
            if self.cur_pos not in nodes:
                nodes.extend([self.cur_pos])
                if self.quadrant in [1, 3]:
                    nodes = sorted(nodes, reverse=True)
                else:
                    nodes = sorted(nodes, reverse=False)
            opponents = self.find_opponents(p, nodes)
            self.path.extend(opponents)
            self.path.extend([p])
            self.cur_pos = p
            if p == self.target_node:
                if self.path_list:
                    if len(self.path) < len(self.path_list[0]):
                        self.path_list = list([self.path])
                else:
                    self.path_list = list([self.path])
                self.board = copy.deepcopy(self.save_board)
                return
            self.cur_pos = p
            self.board.set_piece(self.piece, self.cur_pos)
            self.board.visit_node(self.cur_pos)
            (_, _, _, secondary_rpath, secondary_lpath) = self.show_moves(self.piece, self.cur_pos)
            secondary_rpath = self.sort_nodes(self.remove_visited_nodes(secondary_rpath))
            secondary_lpath = self.sort_nodes(self.remove_visited_nodes(secondary_lpath))
            if self.quadrant in [1, 3]:
                secondary_path = list(secondary_lpath)
            else:
                secondary_path = list(secondary_rpath)
            sec_path = list(self.path)
            for s in secondary_path:
                if self.path_list and len(self.path) >= len(self.path_list[0]):
                    break
                sec_nodes = list(secondary_path)
                if self.cur_pos not in sec_nodes:
                    sec_nodes.extend([self.cur_pos])
                if self.quadrant in [1, 3]:
                    sec_nodes = sorted(sec_nodes, reverse=True)
                else:
                    secondary_path = sorted(secondary_path)
                opponents = self.find_opponents(s, sec_nodes)
                self.path = list(sec_path)
                self.path.extend(opponents)
                self.path.extend([s])
                self.cur_pos = s
                self.board.set_piece(self.piece, self.cur_pos)

                if s == self.target_node:
                    self.path_list.extend([self.path])
                    self.board = copy.deepcopy(self.save_board)
                    break
                self.board.visit_node(self.cur_pos)
                next_moves = self.show_moves(self.piece, self.cur_pos)
                self.diagonal_shortest_path(next_moves)
                break

        self.recursion_depth -= 1
        return

    def find_opponents(self, end, nodes):
        opponents = []
        bias = 1
        if self.cur_pos not in nodes:
            nodes.extend([self.cur_pos])
        sindex = nodes.index(self.cur_pos)
        findex = nodes.index(end)
        if findex < sindex:
            bias = -1
        for i in range(sindex, findex, bias):
            opponent = self.check_cell_occupied(nodes[i])
            if opponent and opponent[1] != self.piece.get_color():
                opponents.extend([nodes[i]])
        return opponents

    def get_diagonal_moves(self):
        '''
        Right diagonal proceeds from 'a1' to 'h8' (or a parallel diagonal path).
        Left diagonal proceeds from 'a8' to 'h1' (or a parallel diagonal path).
        '''
#        import sys; sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()
        (_, right_diag, left_diag) = self.piece.diagonal_moves()
        i = 0
        right_diag.extend([self.cur_pos])
        left_diag.extend([self.cur_pos])
        right_diag = sorted(right_diag)
        left_diag = sorted(left_diag)
        diags = list([right_diag])
        diags.extend([left_diag])
        for d in range(0, 2):
            moves = diags[d]
            i = moves.index(self.cur_pos)
            inc = 1
            while(True):
                if i < 0 or i > len(moves) - 1:
                    break
                m = moves[i]
                if m == self.cur_pos:
                    i += inc
                    continue
                if m == self.target_node:
                    inc = -1
                    i = moves.index(self.cur_pos) - 1
                    continue
                if m in self.path:
                    moves.pop(i)
                    continue
                if m in self.deadends:
                    moves.pop(i)
                    continue
                if self.board.board[m]['piece']:
                    if inc == 1:
                        diags[d] = list(moves[:(i - len(moves))])
                        moves = list(diags[d])
                        inc = -1
                        i = moves.index(self.cur_pos)
                        continue
                    else:
                        diags[d] = list(moves[i - len(moves) + 1:])
                        break
                row = int(m[1]) - 1
                if row > 0:
                    cell = "%c%d" % (m[0], row)
                    if not self.board.board[cell]['piece']:
                        i += inc
                        continue
                row = int(m[1]) + 1
                if row < 9:
                    cell = "%c%d" % (m[0], row)
                    if not self.board.board[cell]['piece']:
                        i += inc
                        continue
                col = ord(m[0]) - 0x60 - 1
                if col > 0:
                    cell = "%c%c" % (chr(col + 0x60), m[1])
                    if not self.board.board[cell]['piece']:
                        i += inc
                        continue
                col = ord(m[0]) - 0x60 + 1
                if col < 9:
                    cell = "%c%c" % (chr(col + 0x60), m[1])
                    if not self.board.board[cell]['piece']:
                        i += inc
                        continue
                moves.pop(i)  # no vertical moves in this column

        right_diag = list(diags[0])
        left_diag = list(diags[1])
        right_diag.pop(right_diag.index(self.cur_pos))
        left_diag.pop(left_diag.index(self.cur_pos))
        if self.quadrant in [1, 3]:
            return (sorted(right_diag, reverse=True), sorted(left_diag, reverse=False))
        else:
            return (sorted(right_diag, reverse=False), sorted(left_diag, reverse=True))

    def get_horizontal_moves(self):
        moves = self.piece.horizontal_moves(self.board)
        i = 0
        while(True):
            if i > len(moves) - 1:
                break
            m = moves[i]
            if m == self.target_node:
                i += 1
                continue
            if m in self.path:
                moves.pop(i)
                continue
            if m in self.deadends:
                moves.pop(i)
                continue
            if self.board.board[m]['piece']:
                moves.pop(i)
                continue
            row = int(m[1]) - 1
            if row > 0:
                cell = "%c%d" % (m[0], row)
                if not self.board.board[cell]['piece']:
                    i += 1
                    continue
            row = int(m[1]) + 1
            if row < 9:
                cell = "%c%d" % (m[0], row)
                if not self.board.board[cell]['piece']:
                    i += 1
                    continue
            moves.pop(i)  # no vertical moves in this column

        if self.quadrant in [1, 3]:
            return sorted(moves, reverse=True)
        else:
            return sorted(moves)

    def get_vertical_moves(self):
        moves = self.piece.vertical_moves(self.board)
        i = 0
        while(True):
            if i > len(moves) - 1:
                break
            m = moves[i]
            if m == self.target_node:
                i += 1
                continue
            if m in self.path:
                moves.pop(i)
                continue
            if m in self.deadends:
                moves.pop(i)
                continue
            if self.board.board[m]['piece']:
                moves.pop(i)
                continue
            col = ord(m[0]) - 0x60 - 1
            if col > 0:
                cell = "%c%c" % (chr(col + 0x60), m[1])
                if not self.board.board[cell]['piece']:
                    i += 1
                    continue
            col = ord(m[0]) - 0x60 + 1
            if col < 9:
                cell = "%c%c" % (chr(col + 0x60), m[1])
                if not self.board.board[cell]['piece']:
                    i += 1
                    continue
            moves.pop(i)  # no vertical moves in this column
        if self.quadrant in [1, 2]:
            return sorted(moves, reverse=True)
        else:
            return sorted(moves)

    def knights_shortest_path(self, moves):
        self.recursion_depth += 1
        self.max_recursion_depth += 1
        path = list(self.path)
        if len(path) < 2:
            print('bingo')
        moves = self._knight_sort(moves)
        my_board = copy.deepcopy(self.board)

        for m in moves:
            self.path = list(path)
            try:
                if path[0] == 'b5' and path[1] == 'c3':
                    print('bingo')
            except:
                pass
            if self.path_list and len(self.path) >= len(self.path_list[0]):
                break
            if m == self.orig_pos:
                continue
            self.path.extend([m])
            self.cur_pos = m
            print(self.path)
            if m == self.target_node:
                if self.path_list:
                    if len(self.path) < len(self.path_list[0]):
                        self.path_list = list([self.path])
                else:
                    self.path_list = list([self.path])
                self.board = copy.deepcopy(my_board)
                return
            self.board.set_piece(self.piece, self.cur_pos)
            self.board.visit_node(self.cur_pos)
            next_moves = self.remove_visited_nodes(self.show_moves(self.piece, self.cur_pos)[0])
            self.knights_shortest_path(next_moves)

        self.recursion_depth -= 1
        self.board = copy.deepcopy(my_board)
        return

    def remove_visited_nodes(self, nodes):
        culled_nodes = []
        for node in nodes:
            if not self.board.has_been_visited(node):
                culled_nodes.extend([node])
        return culled_nodes

    def rook(self, moves):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()

        self.save_board = copy.deepcopy(self.board)
        (_, _, vert, _, _) = moves
        vert = self.remove_visited_nodes(vert)
        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)

        vert.extend([self.cur_pos])

        if self.quadrant in [1, 2]:
            vert = sorted(vert, reverse=True)
        else:
            vert = sorted(vert)

        for v in vert:
            self.cur_pos = self.orig_pos
            if v != self.orig_pos:
                vnodes = list(vert)
                if self.cur_pos not in vnodes:
                    vnodes.extend([self.cur_pos])
                if self.quadrant in [1, 2]:
                    vnodes = list(vert)
                else:
                    vnodes = list(vert)
                opponents = self.find_opponents(v, vnodes)
                self.cur_pos = v
            if v == self.orig_pos:
                self.path = list([self.orig_pos])
            else:
                self.path = list([self.orig_pos])
                self.path.extend(opponents)
                self.path.extend([v])
            self.cur_pos = v
            self.board.set_piece(self.piece, self.cur_pos)
            self.board.visit_node(self.cur_pos)
            (_, horz, _, _, _) = self.show_moves(self.piece, self.cur_pos)
            horz = self.remove_visited_nodes(horz)
            if self.quadrant in [1, 3]:
                horz = sorted(horz, reverse=True)
            else:
                horz = sorted(horz)
            hpath = list(self.path)

            for h in horz:
                self.path = list(hpath)
                hnodes = list(horz)
                if self.cur_pos not in hnodes:
                    hnodes.extend([self.cur_pos])
                if self.quadrant in [1, 3]:
                    hnodes = sorted(hnodes, reverse=True)
                else:
                    hnodes = sorted(hnodes)
                opponents = self.find_opponents(h, hnodes)
                self.path.extend(opponents)
                if h == self.target_node:
                    self.path.extend([h])
                    if self.path_list:
                        if len(self.path) < len(self.path_list[0]):
                            self.path_list = list([self.path])
                    else:
                        self.path_list = list([self.path])
                    self.board = copy.deepcopy(self.save_board)
                    break

                self.cur_pos = h
                self.path.extend([self.cur_pos])
                self.board.set_piece(self.piece, self.cur_pos)
                self.board.visit_node(self.cur_pos)
                (_, _, vert2, _, _) = self.show_moves(self.piece, self.cur_pos)
                vert2 = self.remove_visited_nodes(vert2)
                self.vertical(vert2)

        return

    def queen1(self, moves):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()

        self.save_board = copy.deepcopy(self.board)
        (_, _, vert, _, _) = moves
        vert = self.remove_visited_nodes(vert)
        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)

        vert.extend([self.cur_pos])

        if self.quadrant in [1, 2]:
            vert = sorted(vert, reverse=True)
        else:
            vert = sorted(vert)

        for v in vert:
            self.cur_pos = self.orig_pos
            if v != self.orig_pos:
                vnodes = list(vert)
                if self.cur_pos not in vnodes:
                    vnodes.extend([self.cur_pos])
                if self.quadrant in [1, 2]:
                    vnodes = list(vert)
                else:
                    vnodes = list(vert)
                opponents = self.find_opponents(v, vnodes)
                self.cur_pos = v
            if v == self.orig_pos:
                self.path = list([self.orig_pos])
            else:
                self.path = list([self.orig_pos])
                self.path.extend(opponents)
                self.path.extend([v])
            self.cur_pos = v
            self.board.set_piece(self.piece, self.cur_pos)
            self.board.visit_node(self.cur_pos)
            (_, horz, _, _, _) = self.show_moves(self.piece, self.cur_pos)
            horz = self.remove_visited_nodes(horz)
            if self.quadrant in [1, 3]:
                horz = sorted(horz, reverse=True)
            else:
                horz = sorted(horz)
            hpath = list(self.path)

            for h in horz:
                self.path = list(hpath)
                hnodes = list(horz)
                if self.cur_pos not in hnodes:
                    hnodes.extend([self.cur_pos])
                if self.quadrant in [1, 3]:
                    hnodes = sorted(hnodes, reverse=True)
                else:
                    hnodes = sorted(hnodes)
                opponents = self.find_opponents(h, hnodes)
                self.path.extend(opponents)
                if h == self.target_node:
                    self.path.extend([h])
                    if self.path_list:
                        if len(self.path) < len(self.path_list[0]):
                            self.path_list = list([self.path])
                    else:
                        self.path_list = list([self.path])
                    self.board = copy.deepcopy(self.save_board)
                    break

                self.cur_pos = h
                self.path.extend([self.cur_pos])
                self.board.set_piece(self.piece, self.cur_pos)
                self.board.visit_node(self.cur_pos)
                (_, _, vert2, _, _) = self.show_moves(self.piece, self.cur_pos)
                vert2 = self.remove_visited_nodes(vert2)
                self.vertical(vert2)

        return


    def show_moves(self, piece, position):
        '''
        Show all possible moves for this piece, from this position.
        '''

        return piece.legal_moves(self.board)

    def sort_nodes(self, nodes):
        reverse = False
        if self.quadrant in [1, 3]:
            reverse = True
        elif self.quadrant in [2, 4]:
            reverse = False
        return sorted(nodes, reverse=reverse)

    def target(self, piece, position):
        self.piece = piece
        self.color = piece.get_color()
        self.position = position
        self._populate_random(8)

        # save the board state. Moving a piece onto a tile that has an opponent's piece
        # results in a capture of that piece, removing it from the board. We need to restore
        # the original state of the board after every target path is found.

        self.save_board = copy.deepcopy(self.board)


        # compute furthest tile from our piece
        (self.quadrant, self.target_node) = self._get_farthest_tile(self.position)

        if self.piece.get_type() == 'bishop':
            return self._target_bishop()
        elif self.piece.get_type() == 'king':
            return self._target_king()
        elif self.piece.get_type() == 'knight':
            return self._target_knight()
        elif self.piece.get_type() == 'pawn':
            return  self._target_pawn()
        elif self.piece.get_type() == 'queen':
            return self._target_queen()
        elif self.piece.get_type() == 'rook':
            return self._target_rook()

    def vertical(self, vmoves):

        if self.quadrant in [1, 2]:
            vmoves = sorted(vmoves, reverse=True)
        else:
            vmoves = sorted(vmoves)

        self.recursion_depth += 1
        self.max_recursion_depth += 1

        vpath = list(self.path)
        for v in vmoves:
            self.path = list(vpath)
            vnodes = list(vmoves)
            if self.cur_pos not in vnodes:
                vnodes.extend([self.cur_pos])
            if self.quadrant in [1, 2]:
                vnodes = sorted(vnodes, reverse=True)
            else:
                vnodes = sorted(vnodes)
            opponents = self.find_opponents(v, vnodes)
            self.path.extend(opponents)
            self.path.extend([v])
            self.cur_pos = v
            self.board.set_piece(self.piece, self.cur_pos)

            if v == self.target_node:
                if self.path_list:
                    if len(self.path) < len(self.path_list[0]):
                        self.path_list = list([self.path])
                else:
                    self.path_list = list([self.path])
                self.board = copy.deepcopy(self.save_board)
                return
            self.board.visit_node(self.cur_pos)
            (_, horz, _, _, _) = self.show_moves(self.piece, self.cur_pos)
            horz = self.remove_visited_nodes(horz)

            if self.quadrant in [1, 3]:
                horz = sorted(horz, reverse=True)
            else:
                horz = sorted(horz)
            hpath = list(self.path)
            for h in horz:
                hnodes = list(horz)
                if self.cur_pos not in hnodes:
                    hnodes.extend([self.cur_pos])
                if self.quadrant in [1, 3]:
                    hnodes = sorted(hnodes, reverse=True)
                else:
                    horz = sorted(horz)
                opponents = self.find_opponents(h, hnodes)
                self.path = list(hpath)
                self.path.extend(opponents)
                self.path.extend([h])
                self.cur_pos = h
                self.board.set_piece(self.piece, self.cur_pos)

                if h == self.target_node:
                    if self.path_list:
                        if len(self.path) < len(self.path_list[0]):
                            self.path_list = list([self.path])
                    else:
                        self.path_list = list([self.path])
                    self.board = copy.deepcopy(self.save_board)
                    break
                self.board.visit_node(self.cur_pos)
                (_, _, vert, _, _) = self.show_moves(self.piece, self.cur_pos)
                vert = self.remove_visited_nodes(vert)
                self.vertical(vert)
                break

        self.recursion_depth -= 1


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
    verbose = False

    if (len(argv) < 2):
        print "Number of args: %d" % len(argv)
        usage()

    try:
        opts, _args = getopt.getopt(argv, '',
                                    ['help',
                                     'piece=',
                                     'position=',
                                     'target',
                                     'verbose'])
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
        elif opt == '--verbose':
            verbose = True

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

    obj = Chessercise(board, piece, in_position, verbose)
    if target:
        path_list = obj.target(piece, in_position)
        shortest_paths = []
        min_moves = 0
        if path_list:
            plist = list(path_list)
            pth = plist.pop(0)
            min_moves = len(pth)
            for p in plist:
                if len(p) < min_moves:
                    min_moves = len(p)
            # min_moves now has length of shortest path

            for p in path_list:
                if len(p) == min_moves:
                    shortest_paths.extend([p])
        if len(shortest_paths) == 0:
            print('There were no paths to the destination')
        else:
            print('Found %d paths to the target' % len(path_list))
            if verbose:
                print('Maximum recursion depth: %d' % obj.max_recursion_depth)
                print('List of all paths:')
                for p in path_list:
                    print('    %s' % p)
            print('Shortest path is %d moves.' % (min_moves - 1))
            print('Found %s %d %s:' % ('this' if len(shortest_paths) == 1 else 'these',
                                       len(shortest_paths),
                                       'path' if len(shortest_paths) == 1 else 'paths'))
            for mp in shortest_paths:
                print(mp)

    else:
        moves = obj.show_moves(piece, in_position)[0]
        print moves

if __name__ == '__main__':
    main(sys.argv[1:])
