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

VERSION = '1.0.0'


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

    def get_diagonal_moves(self):
#        import sys; sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()
        (_, right_diag, left_diag) = self.piece.diagonal_moves(self.board)
        i = 0
        diags = list([right_diag])
        diags.extend([left_diag])
        for d in range(0, 2):
            moves = diags[d]
            while(True):
                if i > len(moves) - 1:
                    break
                m = moves[i]
                if m == self.far_pos:
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

        if self.quadrant in [1, 3]:
            return (sorted(right_diag, reverse=True), sorted(left_diag, reverse=True))
        else:
            return (sorted(right_diag), sorted(left_diag))

    def get_horizontal_moves(self):
        moves = self.piece.horizontal_moves(self.board)
        i = 0
        while(True):
            if i > len(moves) - 1:
                break
            m = moves[i]
            if m == self.far_pos:
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
            if m == self.far_pos:
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
        far_pos = None
        if row < 5 and col < 5:
            quadrant = 1
            far_pos = 'h8'
        elif row < 5 and col > 4:
            quadrant = 2
            far_pos = 'a8'
        elif row > 4 and col < 5:
            quadrant = 3
            far_pos = 'h1'
        else:
            quadrant = 4
            far_pos = 'a1'
        self.quadrant = quadrant
        self.far_pos = far_pos
        return (quadrant, far_pos)

    def _get_max_horz(self, far_pos):
        moves = self.piece.horizontal_moves(self.board)
        move = ''
        if moves[-1] == far_pos:
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

    def _get_max_vert(self, far_pos):
        moves = self.piece.vertical_moves(self.board)
        move = ''
        if moves[-1] == far_pos:
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

    def _target_bishop(self, quadrant, far_pos):
        print('Bishop not implemented')

    def _target_king(self, quadrant, far_pos):
        print('King not implemented')

    def _target_knight(self, quadrant, far_pos):
        print('Knight not implemented')

    def _target_pawn(self, quadrant, far_pos):
        print('Pawn not implemented')

    def _target_queen(self, quadrant, far_pos):
        print('Queen not implemented')

    def _target_rook_horz(self, moves, far_pos, path):
        start = 0 if self.quadrant in [1, 3] else len(moves) - 1
        for i in range(start, (len(moves) - 1) if self.hstep == 1 else 0, self.hstep):
            if moves[i] == far_pos:
                return path
            self.board.set_piece(self.piece, moves[i])
            vert_moves = self.piece.vertical_moves(self.board)
            return self._target_rook_vert(vert_moves, far_pos, path)

    def _target_rook_vert(self, moves, far_pos, path):
        start = 0 if self.quadrant in [1, 2] else len(moves) - 1
        for i in range(start, (len(moves) - 1) if self.vstep == 1 else 0, self.vstep):
            if moves[i] == far_pos:
                return path
            self.board.set_piece(self.piece, moves[i])
            path.extend([moves[i]])
            new_horz = self.piece.horizontal_moves(self.board)
            if new_horz[-1] == moves[i]:
                new_horz = new_horz[:-1]
            return self._target_rook_horz(new_horz, far_pos, path)

    def horizontal(self, hmoves):
        self.path.extend([self.cur_pos])
        self.board.set_piece(self.piece, self.cur_pos)

        '''
        Origin position is not in the list of horizontal moves.
        We process the verticals for this position first, then
        move on to the remaining horizontals.
        '''
        self.vertical()

        for h in hmoves:
            self.path = [self.orig_pos, h]
            self.cur_pos = h
            self.board.set_piece(self.piece, self.cur_pos)
            self.vertical()

        '''
        When the above for loop ends, we are done
        '''
        return


    def vertical(self):
        vmoves = self.get_vertical_moves()
        path = []
        self.recursion_depth += 1
        self.max_recursion_depth += 1
        if len(self.path_list) > 50000:
            return
        for v in vmoves:
            if v in self.path or v in self.deadends:
                continue
            if v == self.far_pos:  # found the holy grail - do something about it
                self.path.extend([v])
                self.path_list.extend([self.path])
                self.total_paths += 1
                self.path = []
                return
            self.cur_pos = v
            self.board.set_piece(self.piece, self.cur_pos)
            self.path.extend([v])
            hmoves = self.get_horizontal_moves()
            if hmoves:
                for h in hmoves:
                    if h in self.path or h in self.deadends:
                        continue
                    self.cur_pos = h
                    if self.cur_pos == self.far_pos:
                        self.path.extend([self.cur_pos])
                        self.path_list.extend([self.path])
                        self.total_paths += 1
                        self.path = []
                        return
                    self.path.extend([self.cur_pos])
                    self.board.set_piece(self.piece, self.cur_pos)
                    path = list(self.path)
                    self.vertical()
                    self.recursion_depth -= 1
                    path = path[:-1]
                    self.path = list(path)
                    break
            else:
                self.deadends.extend([self.path[-1]])
                self.path = self.path[:-1]  # remove last path element
                continue


    def _target_rook(self):
#        import sys; sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()

        if self.quadrant == 1:
            self.hstep = 1
            self.vstep = 1
        elif self.quadrant == 2:
            self.hstep = -1
            self.vstep = 1
        elif self.quadrant == 3:
            self.hstep = 1
            self.vstep = -1
        else:
            self.hstep = -1
            self.vstep = -1

        self.total_paths = 0

        self.cur_pos = self.orig_pos = self.piece.get_position()
        self.horizontal(self.get_horizontal_moves())

        return(self.path_list)

    def show_moves(self, piece, position):
        '''
        Show all possible moves for this piece, from this position.
        '''

        return piece.legal_moves(self.board)

    def target(self, piece, position):
#        sys.path.append('/opt/eclipse/plugins/org.python.pydev_4.5.5.201603221110/pysrc/')
#        import pydevd; pydevd.settrace()
        self.piece = piece
        self.position = position
        self._populate_random(8)


        # compute furthest tile from our piece
        (self.quadrant, self.far_pos) = self._get_farthest_tile(self.position)

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
