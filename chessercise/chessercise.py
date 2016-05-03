#!/usr/bin/python
'''
Created on April 22, 2016

@author: mmartin
'''

import copy
import getopt
import sys

from board import Board
from piece import piece_factory

VERSION = '1.0.0'

from statics import PIECES


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

    def __init__(self, piece, position, num_opponents=0, verbose=False):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()
        self.board = Board(empty=True)
        self.piece = piece_factory(piece)
        self.board.set_piece(self.piece, position)
        self.position = position
        self.verbose = verbose
        self.num_opponents = num_opponents
        self.deadends = []
        self.path_list = []
        self.path = []
        self.cur_pos = ''
        self.recursion_depth = 0
        self.max_recursion_depth = 0
        self.shutting_down = False
        self.min_path_length = 0
        self.board.populate_random(self.num_opponents)
        self.color = self.piece.get_color()

    def _bishop_moves(self):
        # adjust target to match color of tile on which the bishop sits.
        if self.board.board[self.target_node]['color'] != self.board.board[self.orig_pos]['color']:
            row = int(self.target_node[1])
            if self.quadrant in [1, 2]:
                self.target_node = '%c%d' % (self.target_node[0], row - 1)
            else:
                self.target_node = '%c%d' % (self.target_node[0], row + 1)

        self.save_board = copy.deepcopy(self.board)
        moves = self.show_moves()

        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)
        self.bishop_shortest_path(moves)

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

        moves = self.remove_visited_nodes(self.show_moves()[0])

        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)
        self.knights_shortest_path(moves)
        return(self.path_list)

    def _target_pawn(self):
        print('Pawn not implemented')

    def _target_queen(self):

        target_piece = piece_factory('bishop')  # we're gonna try diagonals first
        self.board.set_piece(target_piece, self.target_node)
        target_path = self.show_moves()[0]
        self.board.remove_piece(self.target_node)

        self.cur_pos = self.orig_pos = self.piece.get_position()
        self.path.extend([self.cur_pos])

        # try the bishop moves first
        if self.board.board[self.cur_pos]['color'] == self.board.board[self.target_node]['color']:
            self._bishop_moves()
            if len(self.path_list[0]) == 1:  # can't get any shorter!
                return(self.path_list)
            if self.orig_pos not in target_path and len(self.path_list[0]) == 2:  # shortest possible path if you
                return(self.path_list)  # didn't start on the same diagonal

        # now try the horizontal and vertical paths
        self.cur_pos = self.orig_pos
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)
        self.rook(self.show_moves())
        if len(self.path_list[0]) == 2:
            return(self.path_list)  # Shortest possible path

        # Now try the bishop moves off of the rook moves
        for vertical in [True, False]:
            self.cur_pos = self.orig_pos
            self.board.set_piece(self.piece, self.cur_pos)
            self.board.visit_node(self.cur_pos)
            self.queen_vh_diagonal(self.show_moves(), vertical)

        # Now try the rook  moves off of the bishop moves off of the horizontal moves
        for v1 in [True, False]:
            for v2 in [True, False]:
                self.cur_pos = self.orig_pos
                self.board.set_piece(self.piece, self.cur_pos)
                self.board.visit_node(self.cur_pos)
                self.queen_vh_diagonal_vh(self.show_moves(), v1, v2)

        return(self.path_list)

    def _target_rook(self):
        self.cur_pos = self.orig_pos = self.piece.get_position()
        self.rook(self.show_moves())
        return(self.path_list)

    def bishop_shortest_path(self, moves):
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
            (_, _, _, secondary_rpath, secondary_lpath) = self.show_moves()
            secondary_rpath = self.sort_nodes(self.remove_visited_nodes(secondary_rpath))
            secondary_lpath = self.sort_nodes(self.remove_visited_nodes(secondary_lpath))
            if self.quadrant in [1, 4]:
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
                for opponent in opponents:
                    self.board.visit_node(opponent)
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
                next_moves = self.show_moves()
                self.bishop_shortest_path(next_moves)
                break

        self.recursion_depth -= 1
        return

    def capture(self):
        pass

    def check_cell_occupied(self, cell):
        if self.board.board[cell]['piece']:
            return (self.board.board[cell]['piece'].get_type(),
                    self.board.board[cell]['piece'].get_color())
        else:
            return None

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
                moves.pop(i)  # no diagonal moves in this column

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
        moves = self._knight_sort(moves)
        my_board = copy.deepcopy(self.board)

        for m in moves:
            self.path = list(path)
            if self.path_list and len(self.path) >= len(self.path_list[0]):
                break
            if m == self.orig_pos:
                continue
            self.path.extend([m])
            self.cur_pos = m
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
            next_moves = self.remove_visited_nodes(self.show_moves()[0])
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
            (_, horz, _, _, _) = self.show_moves()
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
                (_, _, vert2, _, _) = self.show_moves()
                vert2 = self.remove_visited_nodes(vert2)
                self.vertical(vert2)

        return

    def queen_diagonal_path(self, moves):
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
            (_, _, _, secondary_rpath, secondary_lpath) = self.show_moves()
            secondary_rpath = self.sort_nodes(self.remove_visited_nodes(secondary_rpath))
            secondary_lpath = self.sort_nodes(self.remove_visited_nodes(secondary_lpath))
            if self.quadrant in [1, 3]:
                secondary_path = list(secondary_lpath)
                secondary_path = sorted(secondary_path, reverse=False)
            else:
                secondary_path = list(secondary_rpath)
                secondary_path = sorted(secondary_path, reverse=True)
            sec_path = list(self.path)
            for s in secondary_path:
                if self.path_list and len(self.path) >= len(self.path_list[0]):
                    break
                sec_nodes = list(secondary_path)
                if self.cur_pos not in sec_nodes:
                    sec_nodes.extend([self.cur_pos])
                if self.quadrant in [1, 3]:
                    sec_nodes = sorted(sec_nodes, reverse=False)
                else:
                    secondary_path = sorted(secondary_path, reverse=True)
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
                next_moves = self.show_moves()
                self.queen_diagonal_path(next_moves)
                break

        self.recursion_depth -= 1
        return

    def queen_diagonal_vh_path(self, moves, vertical):
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
            if vertical:
                (_, _, vhmoves, _, _) = self.show_moves()
            else:
                (_, vhmoves, _, _, _) = self.show_moves()
            if self.quadrant in [1, 3]:
                vhmoves = sorted(vhmoves, reverse=True)
            else:
                vhmoves = sorted(vhmoves, reverse=False)
            vh_path = list(self.path)
            for vh in vhmoves:
                if self.path_list and len(self.path) >= len(self.path_list[0]):
                    break
                sec_nodes = list(vhmoves)
                if self.cur_pos not in sec_nodes:
                    sec_nodes.extend([self.cur_pos])
                if self.quadrant in [1, 3]:
                    sec_nodes = sorted(sec_nodes, reverse=False)
                else:
                    vhmoves = sorted(vhmoves, reverse=True)
                opponents = self.find_opponents(vh, sec_nodes)
                self.path = list(vh_path)
                self.path.extend(opponents)
                self.path.extend([vh])
                self.cur_pos = vh
                self.board.set_piece(self.piece, self.cur_pos)

                if vh == self.target_node:
                    if self.path_list:
                        if len(self.path) < len(self.path_list[0]):
                            self.path_list = list([self.path])
                    else:
                        self.path_list = list([self.path])
                    self.board = copy.deepcopy(self.save_board)
                    break
                self.board.visit_node(self.cur_pos)
                next_moves = self.show_moves()
                self.queen_diagonal_vh_path(next_moves, vertical)
                break

        self.recursion_depth -= 1
        return

    def queen_vh_diagonal(self, moves, vertical):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()

        save_board = copy.deepcopy(self.board)
        if vertical:
            (_, moves, _, _, _) = moves
        else:
            (_, _, moves, _, _) = moves
        moves = self.remove_visited_nodes(moves)
        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)

        moves.extend([self.cur_pos])

        if self.quadrant in [1, 2]:
            moves = sorted(moves, reverse=False)
        else:
            moves = sorted(moves, reverse=True)

        for m in moves:
            if m == self.orig_pos:
                continue
            if self.board.board[m]['color'] != self.board.board[self.target_node]['color']:
                continue
            vnodes = list(moves)
            if self.cur_pos not in vnodes:
                vnodes.extend([self.cur_pos])
            vnodes = list(moves)
            opponents = self.find_opponents(m, vnodes)
            self.cur_pos = m
            self.path = list([self.orig_pos])
            self.path.extend(opponents)
            self.path.extend([m])
            self.cur_pos = m
            self.board.set_piece(self.piece, self.cur_pos)
            self.board.visit_node(self.cur_pos)
            self.queen_diagonal_path(self.show_moves())
            self.board = copy.deepcopy(save_board)

        return

    def queen_vh_diagonal_vh(self, moves, vertical1, vertical2):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()

        save_board = copy.deepcopy(self.board)
        if vertical1:
            (_, _, moves1, _, _) = moves
        else:
            (_, moves1, _, _, _) = moves
        moves1 = self.remove_visited_nodes(moves1)
        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)

        moves1.extend([self.cur_pos])

        if self.quadrant in [1, 2]:
            moves = sorted(moves1, reverse=False)
        else:
            moves = sorted(moves1, reverse=True)

        for m in moves1:
            if m == self.orig_pos:
                continue
            if self.board.board[m]['color'] != self.board.board[self.target_node]['color']:
                continue
            vnodes = list(moves1)
            if self.cur_pos not in vnodes:
                vnodes.extend([self.cur_pos])
            vnodes = list(moves1)
            opponents = self.find_opponents(m, vnodes)
            self.cur_pos = m
            self.path = list([self.orig_pos])
            self.path.extend(opponents)
            self.path.extend([m])
            self.cur_pos = m
            self.board.set_piece(self.piece, self.cur_pos)
            self.board.visit_node(self.cur_pos)
            self.queen_diagonal_vh_path(self.show_moves(), vertical2)
            self.board = copy.deepcopy(save_board)

        return
    def show_moves(self):
        '''
        Show all possible moves for this piece, from this position.
        '''
        return self.piece.legal_moves(self.board)

    def sort_nodes(self, nodes):
        reverse = False
        if self.quadrant in [1, 3]:
            reverse = True
        elif self.quadrant in [2, 4]:
            reverse = False
        return sorted(nodes, reverse=reverse)

    def target(self, piece, position):

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
            (_, horz, _, _, _) = self.show_moves()
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
                (_, _, vert, _, _) = self.show_moves()
                vert = self.remove_visited_nodes(vert)
                self.vertical(vert)
                break

        self.recursion_depth -= 1


def usage():
    '''
    Usage instructions.
    '''
    print ('Chessercise.')
    print ('Version : %s' % VERSION)
    print ('')
    print ('Usage: '
           '%s <options>' % sys.argv[0])
    print ('')
    print (' Command Line options:')
    print ('  --capture   - Compute minimum set of moves to capture all pieces on the board.')
    print ('  --help      - Print this enlightening message')
    print ('  --numpieces - Generate "numpieces" number of opponent pieces at random locations on the board.')
    print ('                Defaults to eight.')
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

    capture = False
    in_piece = ''
    in_position = ''
    num_opponents = 8
    target = False
    verbose = False

    if (len(argv) < 2):
        print "Number of args: %d" % len(argv)
        usage()

    try:
        opts, _args = getopt.getopt(argv, '',
                                    ['capture',
                                     'help',
                                     'numpieces=',
                                     'piece=',
                                     'position=',
                                     'target',
                                     'verbose'])
    except getopt.GetoptError, e:
        print ('opt error %s' % e)
        print ('')
        usage()

    for opt, arg in opts:
        if opt == '--capture':
            capture = True
        if opt in ("-h", "--help"):
            usage()
        if opt == 'numpieces':
            num_opponents = arg
        elif opt == '--piece':
            in_piece = arg.lower()
        elif opt == '--position':
            in_position = arg
        elif opt == '--target':
            target = True
        elif opt == '--verbose':
            verbose = True

    if target and capture:
        print('--capture and --target are mutually exclusive')
        usage()

    if in_piece not in PIECES:
        print("Unknown piece %s" % in_piece)
        sys.exit(1)

    col = ord(in_position[1]) - 0x60
    row = int(in_position[0])
    if col in range(1, 9) and row in range(1, 9):
        pass
    else:
        print('Failed on position %s' % in_position)
        sys.exit(1)

    obj = Chessercise(in_piece,
                      in_position,
                      num_opponents=num_opponents,
                      verbose=verbose)
    if capture:
        path_list = obj.capture()
        print(path_list)
    elif target:
        path_list = obj.target()
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
        moves = obj.show_moves()[0]
        print moves

if __name__ == '__main__':
    main(sys.argv[1:])
