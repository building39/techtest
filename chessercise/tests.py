import unittest
import copy
from board import Board, is_odd
from piece import piece_factory, PIECES
from chessercise import Chessercise

class TestChessercise(unittest.TestCase):

    def testGetDiagonalMoves(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        opp1 = piece_factory('pawn', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('pawn', color='black')
        opp4 = piece_factory('pawn', color='black')

        pos = 'a1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'd3')
        c.cur_pos = pos
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['h8', 'g7', 'f6', 'e5', 'd4', 'c3', 'b2'])

        pos = 'a1'
        board = Board(empty=True)
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'c4')
        c.board.set_piece(opp2, 'd3')
        c.board.set_piece(opp3, 'd5')
        c.board.set_piece(opp4, 'e4')
        c.cur_pos = pos
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['h8', 'g7', 'f6', 'e5', 'c3', 'b2'])

        pos = 'a8'
        board = Board(empty=True)
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'd4')
        c.cur_pos = pos
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1'])


        pos = 'a8'
        board = Board(empty=True)
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'e5')
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1'])

        pos = 'e4'
        board = Board(empty=True)
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.cur_pos = pos
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['b1', 'c2', 'd3', 'f5', 'g6', 'h7', 'h1', 'g2', 'f3', 'd5', 'c6', 'b7', 'a8'])

    def testGetHorizontalMoves(self):

        board = Board(empty=True)
        piece = piece_factory('rook')
        opp1 = piece_factory('pawn', color='black')
        opp2 = piece_factory('pawn', color='black')

        pos = 'a1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'd2')
        moves = c.get_horizontal_moves()
        self.assertEqual(moves, ['h1', 'g1', 'f1', 'e1', 'c1', 'b1'])

        pos = 'a8'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'd7')
        moves = c.get_horizontal_moves()
        self.assertEqual(moves, ['h8', 'g8', 'f8', 'e8', 'c8', 'b8'])

        pos = 'a4'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'd3')
        c.board.set_piece(opp2, 'd5')
        c.path.extend(['f4'])
        c.deadends.extend(['h4'])
        moves = c.get_horizontal_moves()
        self.assertEqual(moves, ['g4', 'e4', 'c4', 'b4'])

    def testGetVerticalMoves(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        opp1 = piece_factory('pawn', color='black')
        opp2 = piece_factory('pawn', color='black')

        pos = 'a1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'b2')
        moves = c.get_vertical_moves()
        self.assertEqual(moves, ['a8', 'a7', 'a6', 'a5', 'a4', 'a3'])

        pos = 'h1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'g2')
        moves = c.get_vertical_moves()
        self.assertEqual(moves, ['h8', 'h7', 'h6', 'h5', 'h4', 'h3'])

        pos = 'd1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c._get_farthest_tile(pos)
        c.board.set_piece(opp1, 'c2')
        c.board.set_piece(opp2, 'e2')
        c.path.extend(['d4'])
        c.deadends.extend(['d6'])
        moves = c.get_vertical_moves()
        self.assertEqual(moves, ['d8', 'd7', 'd5', 'd3'])

    def testCreateRandomPiece(self):
        pieces = PIECES.keys()
        board = Board(empty=True)
        piece = piece_factory('knight')
        c = Chessercise(board, piece, 'a1')
        p = c._create_random_piece()
        self.assertTrue(p.lower() in pieces)

    def testGetRandomTile(self):
        board = Board(empty=True)
        piece = piece_factory('knight')
        c = Chessercise(board, piece, 'a1')
        tile = c._get_random_tile()
        row = int(tile[1])
        col = ord(tile[0]) - 0x60
        self.assertTrue(row in range(1, 9))
        self.assertTrue(col in range(1, 9))

    def testTargetBishopFromC1(self):
        board = Board(empty=True)
        piece = piece_factory('bishop')
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        pos = 'c1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.cur_pos = pos
        path_list = c._target_bishop()
        self.assertEqual(path_list[0], ['c1', 'h6', 'g7', 'h8'], "Path should be ['c1', 'h6', 'g7', 'h8'], not %s" % path_list[0])

    def testTargetBishopFromA8(self):
        board = Board(empty=True)
        piece = piece_factory('bishop')
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        pos = 'a8'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'd5')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.cur_pos = pos
        path_list = c._target_bishop()
        self.assertEqual(path_list[0], ['a8', 'd5', 'h1'], "Path should be ['a8', 'd5', 'h1'], not %s" % path_list[0])

    def testTargetKnightFromA1(self):
        board = Board(empty=True)
        piece = piece_factory('knight')
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        pos = 'a1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'f6')
        c.board.set_piece(opp2, 'h7')
        c.board.set_piece(opp3, 'd2')
        c.board.set_piece(opp4, 'e7')
        c.board.set_piece(opp5, 'b8')
        c.board.set_piece(opp6, 'd3')
        c.board.set_piece(opp7, 'h3')
        c.board.set_piece(opp8, 'd8')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.save_board = copy.deepcopy(board)
        path_list = c._target_knight()
        print(path_list[0])
        import sys; sys.stdout.flush()
        self.assertEqual(path_list[0],
                         ['a1', 'c2', 'e3', 'g4', 'h6', 'f7', 'h8'],
                         "Path should be ['a1', 'c2', 'e3', 'g4', 'h6', 'f7', 'h8'], not %s" % path_list[0])

    def testTargetQueenFromA1NoOpponents(self):
        board = Board(empty=True)
        piece = piece_factory('queen')
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        pos = 'a1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f7')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.cur_pos = pos
        path_list = c._target_queen()
        answer = ['a1', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromA1OneOpponent(self):
        board = Board(empty=True)
        piece = piece_factory('queen')
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        pos = 'a1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.cur_pos = pos
        path_list = c._target_queen()
        answer = ['a1', 'f6', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromA1TwoOpponents(self):
        board = Board(empty=True)
        piece = piece_factory('queen')
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        pos = 'a1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'd4')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.cur_pos = pos
        path_list = c._target_queen()
        answer = ['a1', 'f6', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromC1(self):
        board = Board(empty=True)
        piece = piece_factory('queen')
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        pos = 'c1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.cur_pos = pos
        path_list = c._target_queen()
        answer = ['c1', 'c8', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetKnightFromA3(self):
        board = Board(empty=True)
        piece = piece_factory('knight')
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        pos = 'a3'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'f6')
        c.board.set_piece(opp2, 'h7')
        c.board.set_piece(opp3, 'd2')
        c.board.set_piece(opp4, 'e7')
        c.board.set_piece(opp5, 'b8')
        c.board.set_piece(opp6, 'd3')
        c.board.set_piece(opp7, 'h3')
        c.board.set_piece(opp8, 'd8')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.save_board = copy.deepcopy(board)
        path_list = c._target_knight()
        self.assertEqual(path_list[0],
                         ['a3', 'c4', 'e5', 'g6', 'h8'],
                         "Path should be ['a3', 'c4', 'e5', 'g6', 'h8'], not %s" % path_list[0])

    def testTargetRookFromA1(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        pos = 'a1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'f6')
        c.board.set_piece(opp2, 'h7')
        c.board.set_piece(opp3, 'd2')
        c.board.set_piece(opp4, 'e7')
        c.board.set_piece(opp5, 'b8')
        c.board.set_piece(opp6, 'd3')
        c.board.set_piece(opp7, 'h3')
        c.board.set_piece(opp8, 'd8')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        c.color = piece.get_color()
        c.save_board = copy.deepcopy(board)
        path_list = c._target_rook()
        for p in path_list:
            print p
        self.assertEqual(path_list[0], ['a1', 'g1', 'g8', 'h8'], "Path should be ['a1', 'f1', 'f8', 'h8'], not %s" % path_list[0])

    def testTargetRookFromA8(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        pos = 'a8'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'd4')
        c.board.set_piece(opp2, 'b4')
        c.board.set_piece(opp3, 'b1')
        c.board.set_piece(opp4, 'g7')
        c.board.set_piece(opp5, 'a4')
        c.board.set_piece(opp6, 'e3')
        c.board.set_piece(opp7, 'd6')
        c.board.set_piece(opp8, 'b5')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        path_list = c._target_rook()
        answer = ['a8', 'h8', 'h1']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetRookFromB3(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        pos = 'b3'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'f7')
        c.board.set_piece(opp2, 'g4')
        c.board.set_piece(opp3, 'e8')
        c.board.set_piece(opp4, 'h4')
        c.board.set_piece(opp5, 'd4')
        c.board.set_piece(opp6, 'e7')
        c.board.set_piece(opp7, 'h2')
        c.board.set_piece(opp8, 'd2')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        path_list = c._target_rook()
        answer = ['b3', 'b8', 'e8', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetRookFromH1(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        pos = 'h1'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'd8')
        c.board.set_piece(opp2, 'g1')
        c.board.set_piece(opp3, 'a5')
        c.board.set_piece(opp4, 'd6')
        c.board.set_piece(opp5, 'h4')
        c.board.set_piece(opp6, 'g3')
        c.board.set_piece(opp7, 'c3')
        c.board.set_piece(opp8, 'a1')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        path_list = c._target_rook()
        answer = ['h1', 'h4', 'h8', 'd8', 'a8']
        self.assertEqual(path_list[0],
                         answer,
                         "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetRookFromH8(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        pos = 'h8'
        board.set_piece(piece, pos)
        c = Chessercise(board, piece, pos)
        c.board.set_piece(opp1, 'f6')
        c.board.set_piece(opp2, 'g6')
        c.board.set_piece(opp3, 'c4')
        c.board.set_piece(opp4, 'f8')
        c.board.set_piece(opp5, 'g3')
        c.board.set_piece(opp6, 'b3')
        c.board.set_piece(opp7, 'f2')
        c.board.set_piece(opp8, 'e1')
        (c.quadrant, c.far_pos) = c._get_farthest_tile(pos)
        c.verbose = True
        path_list = c._target_rook()
        answer = ['h8', 'h1', 'e1', 'a1']
        self.assertEqual(path_list[0],
                         answer,
                         "Path should be %s, not %s" % (answer, path_list[0]))

    def testGetFarthestTile(self):
        board = Board(empty=True)
        piece = piece_factory('knight')
        for pos in ['a1', 'a2', 'a3', 'a4',
                    'b1', 'b2', 'b3', 'b4',
                    'c1', 'c2', 'c3', 'c4',
                    'd1', 'd2', 'd3', 'd4',
                    ]:

            c = Chessercise(board, piece, pos)
            (quadrant, position) = c._get_farthest_tile(pos)
            self.assertEqual(position, 'h8',
                             'Got tile %s instead of h8 for position %s' % (position, pos))
            self.assertEqual(quadrant, 1, 'Got quadrant %d instead of 1' % quadrant)
        for pos in ['a5', 'a6', 'a7', 'a8',
                    'b5', 'b6', 'b7', 'b8',
                    'c5', 'c6', 'c7', 'c8',
                    'd5', 'd6', 'd7', 'd8',
                    ]:
            c = Chessercise(board, piece, pos)
            (quadrant, position) = c._get_farthest_tile(pos)
            self.assertEqual(position, 'h1',
                             'Got tile %s instead of h1 for position %s' % (position, pos))
            self.assertEqual(quadrant, 3, 'Got quadrant %d instead of 3' % quadrant)
        for pos in ['e1', 'f1', 'g1', 'h1',
                    'e2', 'f2', 'g2', 'h2',
                    'e3', 'f3', 'g3', 'h3',
                    'e4', 'f4', 'g4', 'h4',
                    ]:
            c = Chessercise(board, piece, pos)
            (quadrant, position) = c._get_farthest_tile(pos)
            self.assertEqual(position, 'a8',
                             'Got tile %s instead of h1 for position %s' % (position, pos))
            self.assertEqual(quadrant, 2, 'Got quadrant %d instead of 3' % quadrant)
        for pos in ['e5', 'f6', 'g7', 'h8',
                    'e5', 'f6', 'g7', 'h8',
                    'e5', 'f6', 'g7', 'h8',
                    'e5', 'f6', 'g7', 'h8',
                    ]:
            c = Chessercise(board, piece, pos)
            (quadrant, position) = c._get_farthest_tile(pos)
            self.assertEqual(position, 'a1',
                             'Got tile %s instead of a1 for position %s' % (position, pos))
            self.assertEqual(quadrant, 4, 'Got quadrant %d instead of 4' % quadrant)

    def testPopulateRandom(self):
        num_pieces = 8
        board = Board(empty=True)
        piece = piece_factory('knight')
        c = Chessercise(board, piece, 'a1')
        c._populate_random(num_pieces)
        count = 0
        for k, v in c.board.board.iteritems():
            if v['piece']:
                count += 1
                print("Found a %s at %s" % (v['piece'], k))
        self.assertEquals(count, num_pieces, "should have found %d pieces, but found %d instead." % (num_pieces, count))

    def testTileColor(self):
        board = Board(empty=True)
        for k, v in board.board.iteritems():
            row = int(k[1])
            col = ord(k[0]) - 0x60
            if (is_odd(row) and is_odd(col)) or \
                (not is_odd(row) and not is_odd(col)):
                    self.failUnlessEqual(v['color'], 'black')
            else:
                self.failUnlessEqual(v['color'], 'white')

    def testBoard(self):
        board = Board(empty=True)
        self.assertTrue(board.is_valid_move('a1', 'b2'))
        self.assertFalse(board.is_valid_move('z1', 'b2'))
        self.assertFalse(board.is_valid_move('a1', 'z2'))
        self.assertTrue(board.is_valid_position('a1'))
        self.assertFalse(board.is_valid_position('z1'))
        self.assertFalse(board.is_valid_position('a9'))

    def testPiece(self):
        piece = piece_factory('knight')
        self.failUnlessEqual(piece.get_type(), 'knight')
        self.failUnlessEqual(piece.get_color(), 'white')
        piece.set_position('b1')
        self.failUnlessEqual(piece.get_position(), 'b1')

    def testBishopMoves(self):
        board = Board(empty=True)
        piece = piece_factory('bishop')
        piece.set_position('c1')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['a3', 'b2', 'd2', 'e3', 'f4', 'g5', 'h6'])
        piece.set_position('d5')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['a2', 'a8', 'b3', 'b7', 'c4', 'c6', 'e4', 'e6', 'f3', 'f7', 'g2', 'g8', 'h1'])

    def testKnightMoves(self):
        board = Board(empty=True)
        piece = piece_factory('knight')
        piece.set_position('b1')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['a3', 'c3', 'd2'])
        piece.set_position('d5')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['b4', 'b6', 'c3', 'c7', 'e3', 'e7', 'f4', 'f6'])

    def testQueenMoves(self):
        board = Board(empty=True)
        piece = piece_factory('queen')
        piece.set_position('e5')
        self.failUnlessEqual(piece.legal_moves(board)[0],
                             ['a1', 'a5', 'b2', 'b5', 'b8', 'c3', 'c5', 'c7', 'd4', 'd5', 'd6', 'e1', 'e2', 'e3', 'e4', 'e6', 'e7', 'e8', 'f4', 'f5', 'f6', 'g3', 'g5', 'g7', 'h2', 'h5', 'h8'])

    def testRookMoves(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        piece.set_position('a1')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'])
        piece.set_position('d5')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['a5', 'b5', 'c5', 'e5', 'f5', 'g5', 'h5', 'd1', 'd2', 'd3', 'd4', 'd6', 'd7', 'd8'])

if __name__ == '__main__':
    unittest.main()
