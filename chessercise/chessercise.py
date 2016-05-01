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

    def _populate_random(self, num):
        random.seed()
        for _i in range(1, num + 1):
            tile = self._get_random_tile()
            new_piece = self._create_random_piece()
            self.board.set_piece(piece_factory(new_piece, color='black'), tile)
            print('%s at %s' % (new_piece, tile))

    def _target_bishop(self):
        import sys; sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
        import pydevd; pydevd.settrace()
        self.total_paths = 0
        self.cur_pos = self.orig_pos = self.piece.get_position()
        self.path.extend([self.cur_pos])
        # adjust target to match color of tile on which the bishop sits.
        if self.board.board[self.target_node]['color'] != self.board.board[self.orig_pos]['color']:
            row = int(self.target_node[1])
            if self.quadrant in [1, 2]:
                self.target_node = '%c%d' % (self.target_node[0], row - 1)
            else:
                self.target_node = '%c%d' % (self.target_node[0], row + 1)
        self.diagonal()

        return(self.path_list)

    def _target_king(self):
        print('King not implemented')

    def _target_knight(self):
        print('Knight not implemented')

    def _target_pawn(self):
        print('Pawn not implemented')

    def _target_queen(self):
        print('Queen not implemented')

    def _split_horz_vert(self, moves):
        horz = []
        vert = []
        for m in moves:
            if m[0] == self.cur_pos[0]:
                vert.extend([m])
            else:
                horz.extend([m])
        return list([horz, vert])

    def _target_rook(self):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()
        self.total_paths = 0
        self.cur_pos = self.orig_pos = self.piece.get_position()

        self.horizontal()

        return(self.path_list)

    def check_cell_occupied(self, cell):
        if self.board.board[cell]['piece']:
            return (self.board.board[cell]['piece'].get_type(),
                    self.board.board[cell]['piece'].get_color())
        else:
            return None

    def find_opponents(self, start, end, nodes):
        opponents = []
        if self.cur_pos in nodes:
            nodes = nodes.pop(nodes.index(self.cur_pos))
        for node in nodes:
            opponent = self.check_cell_occupied(node)
            if opponent and opponent[1] != self.piece.get_color():
                opponents.extend([node])
        return opponents

    def horizontal(self):
        path = []
        self.save_board = copy.deepcopy(self.board)
        (_, vert) = self._split_horz_vert(self.remove_visited_nodes(self.show_moves(self.piece, self.cur_pos)))
        self.path = list([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)
        self.board.visit_node(self.cur_pos)

        vert.extend([self.cur_pos])

        if self.quadrant in [1, 2]:
            vert = sorted(vert, reverse=True)
            bias = -1
        else:
            vert = sorted(vert)
            bias = 1

        for v in vert:
            if v == self.orig_pos:
                self.path = list([self.orig_pos])
            else:
                self.path = list([self.orig_pos, v])
            path = list(self.path)
            self.cur_pos = v
            self.board.set_piece(self.piece, self.cur_pos)
            self.board.visit_node(self.cur_pos)
            (horz, _) = self._split_horz_vert(self.remove_visited_nodes(self.show_moves(self.piece, self.cur_pos)))
            if self.quadrant in [1, 3]:
                horz = sorted(horz, reverse=True)
                bias = -1
            else:
                horz = sorted(horz)
                bias = 1
            hpath = list(self.path)
            for h in horz:
                self.path = list(hpath)
                if h == self.target_node:
#                    print('Found target %s' % h)
                    self.path.extend([h])
                    self.path_list.extend([self.path])
                    self.board = copy.deepcopy(self.save_board)
                    break
    #            print('1. Visited node %s' % h))
                self.cur_pos = h
                self.path.extend([self.cur_pos])
                self.board.set_piece(self.piece, self.cur_pos)
                self.board.visit_node(self.cur_pos)
                (_, vert) = self._split_horz_vert(self.remove_visited_nodes(self.show_moves(self.piece, self.cur_pos)))
                self.vertical(vert)

        '''
        When the above for loop ends, we are done
        '''
        return

    def remove_visited_nodes(self, nodes):
        culled_nodes = []
        for node in nodes:
            if not self.board.has_been_visited(node):
                culled_nodes.extend([node])
        return culled_nodes

    def vertical(self, vmoves):

        if self.quadrant in [1, 2]:
            vmoves = sorted(vmoves, reverse=True)
            bias = -1
        else:
            vmoves = sorted(vmoves)
            bias = 1

        path = list(self.path)
        self.recursion_depth += 1
        self.max_recursion_depth += 1

#        index = vmoves.index(self.cur_pos)

#        print('Vertical moves: %s' % vmoves)
        vpath = list(self.path)
        for v in vmoves:
            self.path = list(vpath)
            self.path.extend([v])
#            if v != self.cur_pos:
#                print('Visited vertical node %s' % v)
            self.cur_pos = v
            self.board.set_piece(self.piece, self.cur_pos)

            if v == self.target_node:
                self.path_list.extend([self.path])
                self.board = copy.deepcopy(self.save_board)
                return
            self.board.visit_node(self.cur_pos)
            (horz, _) = self._split_horz_vert(self.remove_visited_nodes(self.show_moves(self.piece, self.cur_pos)))
            if self.quadrant in [1, 3]:
                horz = sorted(horz, reverse=True)
                bias = -1
            else:
                horz = sorted(horz)
                bias = 1
            hpath = list(self.path)
            for h in horz:
                self.path = list(hpath)
                self.path.extend([h])
                self.cur_pos = h
                self.board.set_piece(self.piece, self.cur_pos)

                if h == self.target_node:
                    self.path_list.extend([self.path])
                    self.board = copy.deepcopy(self.save_board)
                    break
                self.board.visit_node(self.cur_pos)
                (_, vert) = self._split_horz_vert(self.remove_visited_nodes(self.show_moves(self.piece, self.cur_pos)))
                self.vertical(vert)
                break

    def show_moves(self, piece, position):
        '''
        Show all possible moves for this piece, from this position.
        '''

        return piece.legal_moves(self.board)

    def target(self, piece, position):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()
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
            self._target_bishop()
        elif self.piece.get_type() == 'king':
            self._target_king()
        elif self.piece.get_type() == 'knight':
            self._target_knight()
        elif self.piece.get_type() == 'pawn':
            self._target_pawn()
        elif self.piece.get_type() == 'queen':
            self._target_queen()
        elif self.piece.get_type() == 'rook':
            return self._target_rook()


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
        moves = obj.show_moves(piece, in_position)
        print moves

if __name__ == '__main__':
    main(sys.argv[1:])
