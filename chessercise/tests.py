import unittest
import copy
from board import Board, is_odd
from piece import piece_factory
from statics import  PIECES
from chessercise import Chessercise

class TestChessercise(unittest.TestCase):

    def testBishopMoves(self):
        board = Board(empty=True)
        piece = piece_factory('bishop')
        piece.set_node('c1')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['a3', 'b2', 'd2', 'e3', 'f4', 'g5', 'h6'])
        piece.set_node('d5')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['a2', 'a8', 'b3', 'b7', 'c4', 'c6', 'e4',
                                                           'e6', 'f3', 'f7', 'g2', 'g8', 'h1'])

    def testBoard(self):
        board = Board(empty=True)
        self.assertTrue(board.is_valid_move('a1', 'b2'))
        self.assertFalse(board.is_valid_move('z1', 'b2'))
        self.assertFalse(board.is_valid_move('a1', 'z2'))
        self.assertTrue(board.is_valid_node('a1'))
        self.assertFalse(board.is_valid_node('z1'))
        self.assertFalse(board.is_valid_node('a9'))

    def testCaptureByQueenC1(self):
        piece = 'queen'
        node = 'c1'

        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')

        c = Chessercise(piece, node, num_opponents=0)

        c.board.set_piece(opp1, 'a8')
        c.board.set_piece(opp2, 'b8')
        c.board.set_piece(opp3, 'd6')
        c.board.set_piece(opp4, 'a5')
        c.board.set_piece(opp5, 'e5')
        c.board.set_piece(opp6, 'b3')
        c.board.set_piece(opp7, 'f3')
        c.board.set_piece(opp8, 'e1')

        c.verbose = True

        path_list = c.capture()

        answer = ['a1', 'h8']

        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testCaptureByKnightC1(self):
        piece = 'knight'
        node = 'c1'

        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')

        c = Chessercise(piece, node, num_opponents=0)

        c.board.set_piece(opp1, 'a8')
        c.board.set_piece(opp2, 'b8')
        c.board.set_piece(opp3, 'd6')
        c.board.set_piece(opp4, 'a5')
        c.board.set_piece(opp5, 'e5')
        c.board.set_piece(opp6, 'b3')
        c.board.set_piece(opp7, 'f3')
        c.board.set_piece(opp8, 'e1')

        c.verbose = True

        path_list = c.capture()

        answer = ['a1', 'h8']

        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testCreateRandomPiece(self):
        pieces = PIECES.keys()
        board = Board(empty=True)
        p = board.create_random_piece()
        self.assertTrue(p.lower() in pieces)

    def testGetDiagonalMoves(self):
        piece = 'rook'
        opp1 = piece_factory('pawn', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('pawn', color='black')
        opp4 = piece_factory('pawn', color='black')

        node = 'a1'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'd3')
        c.cur_node = node
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['h8', 'g7', 'f6', 'e5', 'd4', 'c3', 'b2'])

        node = 'a1'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'c4')
        c.board.set_piece(opp2, 'd3')
        c.board.set_piece(opp3, 'd5')
        c.board.set_piece(opp4, 'e4')
        c.cur_node = node
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['h8', 'g7', 'f6', 'e5', 'c3', 'b2'])

        node = 'a8'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'd4')
        c.cur_node = node
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1'])

        node = 'a8'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'e5')
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1'])

        node = 'e4'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.cur_node = node
        (rdiag, ldiag) = c.get_diagonal_moves()
        moves = rdiag + ldiag
        self.assertEqual(moves, ['b1', 'c2', 'd3', 'f5', 'g6', 'h7', 'h1', 'g2', 'f3', 'd5', 'c6', 'b7', 'a8'])

    def testGetFarthestNode(self):
        piece = 'knight'
        for node in ['a1', 'a2', 'a3', 'a4',
                    'b1', 'b2', 'b3', 'b4',
                    'c1', 'c2', 'c3', 'c4',
                    'd1', 'd2', 'd3', 'd4',
                    ]:

            c = Chessercise(piece, node)
            (c.quadrant, c.target_node) = c._get_farthest_node(node)
            self.assertEqual(c.target_node, 'h8',
                             'Got tile %s instead of %s for node %s' % (c.target_node, node, node))
            self.assertEqual(c.quadrant, 1, 'Got quadrant %d instead of 1' % c.quadrant)
        for node in ['a5', 'a6', 'a7', 'a8',
                    'b5', 'b6', 'b7', 'b8',
                    'c5', 'c6', 'c7', 'c8',
                    'd5', 'd6', 'd7', 'd8',
                    ]:
            c = Chessercise(piece, node)
            (c.quadrant, c.target_node) = c._get_farthest_node(node)
            self.assertEqual(c.target_node, 'h1',
                             'Got tile %s instead of %s for node %s' % (c.target_node, node, node))
            self.assertEqual(c.quadrant, 3, 'Got quadrant %d instead of 3' % c.quadrant)
        for node in ['e1', 'f1', 'g1', 'h1',
                    'e2', 'f2', 'g2', 'h2',
                    'e3', 'f3', 'g3', 'h3',
                    'e4', 'f4', 'g4', 'h4',
                    ]:
            c = Chessercise(piece, node)
            (c.quadrant, c.target_node) = c._get_farthest_node(node)
            self.assertEqual(c.target_node, 'a8',
                             'Got tile %s instead of %s for node %s' % (c.target_node, node, node))
            self.assertEqual(c.quadrant, 2, 'Got quadrant %d instead of 3' % c.quadrant)
        for node in ['e5', 'f6', 'g7', 'h8',
                    'e5', 'f6', 'g7', 'h8',
                    'e5', 'f6', 'g7', 'h8',
                    'e5', 'f6', 'g7', 'h8',
                    ]:
            c = Chessercise(piece, node)
            (c.quadrant, c.target_node) = c._get_farthest_node(node)
            self.assertEqual(c.target_node, 'a1',
                             'Got tile %s instead of %s for node %s' % (c.target_node, node, node))
            self.assertEqual(c.quadrant, 4, 'Got quadrant %d instead of 4' % c.quadrant)
    def testGetHorizontalMoves(self):

        piece = 'rook'
        opp1 = piece_factory('pawn', color='black')
        opp2 = piece_factory('pawn', color='black')

        node = 'a1'

        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'd2')
        moves = c.get_horizontal_moves()
        self.assertEqual(moves, ['h1', 'g1', 'f1', 'e1', 'c1', 'b1'])

        node = 'a8'
        c.board.set_piece(c.piece, node)
        c = Chessercise(piece, node)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'd7')
        moves = c.get_horizontal_moves()
        self.assertEqual(moves, ['h8', 'g8', 'f8', 'e8', 'c8', 'b8'])

        node = 'a4'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'd3')
        c.board.set_piece(opp2, 'd5')
        c.path.extend(['f4'])
        c.deadends.extend(['h4'])
        moves = c.get_horizontal_moves()
        self.assertEqual(moves, ['g4', 'e4', 'c4', 'b4'])

    def testGetRandomNode(self):
        board = Board(empty=True)
        node = board.get_random_node()
        row = int(node[1])
        col = ord(node[0]) - 0x60
        self.assertTrue(row in range(1, 9))
        self.assertTrue(col in range(1, 9))

    def testGetVerticalMoves(self):

        piece = 'rook'
        opp1 = piece_factory('pawn', color='black')
        opp2 = piece_factory('pawn', color='black')

        node = 'a1'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'b2')
        moves = c.get_vertical_moves()
        self.assertEqual(moves, ['a8', 'a7', 'a6', 'a5', 'a4', 'a3'])

        node = 'h1'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'g2')
        moves = c.get_vertical_moves()
        self.assertEqual(moves, ['h8', 'h7', 'h6', 'h5', 'h4', 'h3'])

        node = 'd1'
        c = Chessercise(piece, node, num_opponents=0)
        (c.quadrant, c.target_node) = c._get_farthest_node(node)
        c.board.set_piece(opp1, 'c2')
        c.board.set_piece(opp2, 'e2')
        c.path.extend(['d4'])
        c.deadends.extend(['d6'])
        moves = c.get_vertical_moves()
        self.assertEqual(moves, ['d8', 'd7', 'd5', 'd3'])

    def testKnightMoves(self):
        board = Board(empty=True)
        piece = piece_factory('knight')
        piece.set_node('b1')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['a3', 'c3', 'd2'])
        piece.set_node('d5')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['b4', 'b6', 'c3', 'c7', 'e3', 'e7', 'f4', 'f6'])

    def testNodeColor(self):
        board = Board(empty=True)
        for k, v in board.board.iteritems():
            row = int(k[1])
            col = ord(k[0]) - 0x60
            if (is_odd(row) and is_odd(col)) or \
                (not is_odd(row) and not is_odd(col)):
                    self.failUnlessEqual(v['color'], 'black')
            else:
                self.failUnlessEqual(v['color'], 'white')

    def testPiece(self):
        piece = piece_factory('knight')
        self.failUnlessEqual(piece.get_type(), 'knight')
        self.failUnlessEqual(piece.get_color(), 'white')
        piece.set_node('b1')
        self.failUnlessEqual(piece.get_node(), 'b1')

    def testPopulateRandom(self):

        board = Board(empty=True)
        num_pieces = 8

        board.populate_random(num_pieces)
        count = 0
        for _, v in board.board.iteritems():
            if v['piece']:
                count += 1
        self.assertEquals(count, num_pieces, "should have found %d pieces, but found %d instead." % (num_pieces, count))

    def testQueenMoves(self):
        board = Board(empty=True)
        piece = piece_factory('queen')
        piece.set_node('e5')
        self.failUnlessEqual(piece.legal_moves(board)[0],
                             ['a1', 'a5', 'b2', 'b5', 'b8', 'c3', 'c5', 'c7', 'd4', 'd5',
                              'd6', 'e1', 'e2', 'e3', 'e4', 'e6', 'e7', 'e8', 'f4', 'f5',
                              'f6', 'g3', 'g5', 'g7', 'h2', 'h5', 'h8'])

    def testRookMoves(self):
        board = Board(empty=True)
        piece = piece_factory('rook')
        piece.set_node('a1')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                                                           'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8'])
        piece.set_node('d5')
        self.failUnlessEqual(piece.legal_moves(board)[0], ['a5', 'b5', 'c5', 'e5', 'f5', 'g5', 'h5',
                                                           'd1', 'd2', 'd3', 'd4', 'd6', 'd7', 'd8'])

    def testTargetBishopFromA8(self):

        piece = 'bishop'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'a8'

        c = Chessercise(piece, node, num_opponents=0)
        c.board.set_piece(opp1, 'd5')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['a8', 'd5', 'h1']
        self.assertEqual(path_list[0],
                         answer,
                         "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetBishopFromC1(self):

        piece = 'bishop'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'c1'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['c1', 'h6', 'g7', 'h8']
        self.assertEqual(path_list[0],
                         answer,
                         "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetKnightFromA1(self):

        piece = 'knight'
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        node = 'a1'

        c = Chessercise(piece, node, num_opponents=0)
        c.board.set_piece(opp1, 'f6')
        c.board.set_piece(opp2, 'h7')
        c.board.set_piece(opp3, 'd2')
        c.board.set_piece(opp4, 'e7')
        c.board.set_piece(opp5, 'b8')
        c.board.set_piece(opp6, 'd3')
        c.board.set_piece(opp7, 'h3')
        c.board.set_piece(opp8, 'd8')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.save_board = copy.deepcopy(c.board)
        path_list = c.target()
        answer = ['a1', 'c2', 'e3', 'g4', 'h6', 'f7', 'h8']
        self.assertEqual(path_list[0],
                         answer,
                         "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetKnightFromA3(self):

        piece = 'knight'
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        node = 'a3'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'f6')
        c.board.set_piece(opp2, 'h7')
        c.board.set_piece(opp3, 'd2')
        c.board.set_piece(opp4, 'e7')
        c.board.set_piece(opp5, 'b8')
        c.board.set_piece(opp6, 'd3')
        c.board.set_piece(opp7, 'h3')
        c.board.set_piece(opp8, 'd8')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.save_board = copy.deepcopy(c.board)
        path_list = c.target()
        answer = ['a3', 'c4', 'e5', 'g6', 'h8']
        c.board.print_board()
        self.assertEqual(path_list[0],
                         answer,
                         "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromA1NoOpponents(self):

        piece = 'queen'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'a1'

        c = Chessercise(piece, node, num_opponents=0)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f7')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['a1', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromA1OneOpponent(self):

        piece = 'queen'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'a1'

        c = Chessercise(piece, node, num_opponents=0)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['a1', 'f6', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromA1ThreeOpponents(self):

        piece = 'queen'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'a1'

        c = Chessercise(piece, node, num_opponents=0)
        c.board.set_piece(opp1, 'b2')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'd4')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['a1', 'e1', 'e8', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromB8(self):

        piece = 'queen'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'b8'

        c = Chessercise(piece, node, num_opponents=0)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['b8', 'b1', 'h1']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromC1(self):

        piece = 'queen'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'c1'

        c = Chessercise(piece, node, num_opponents=0)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['c1', 'c8', 'h8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromG4(self):

        piece = 'queen'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'g4'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['g4', 'e4', 'a8']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetQueenFromH7(self):

        piece = 'queen'
        opp1 = piece_factory('knight', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('queen', color='black')
        opp4 = piece_factory('bishop', color='black')
        opp5 = piece_factory('king', color='black')
        opp6 = piece_factory('pawn', color='black')
        opp7 = piece_factory('knight', color='black')
        opp8 = piece_factory('pawn', color='black')
        node = 'h7'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'e4')
        c.board.set_piece(opp2, 'a6')
        c.board.set_piece(opp3, 'c8')
        c.board.set_piece(opp4, 'g3')
        c.board.set_piece(opp5, 'h5')
        c.board.set_piece(opp6, 'f5')
        c.board.set_piece(opp7, 'f6')
        c.board.set_piece(opp8, 'h6')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.cur_node = node
        path_list = c.target()
        answer = ['h7', 'a7', 'a6', 'a1']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetRookFromA1(self):
        piece = 'rook'
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        node = 'a1'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'f6')
        c.board.set_piece(opp2, 'h7')
        c.board.set_piece(opp3, 'd2')
        c.board.set_piece(opp4, 'e7')
        c.board.set_piece(opp5, 'b8')
        c.board.set_piece(opp6, 'd3')
        c.board.set_piece(opp7, 'h3')
        c.board.set_piece(opp8, 'd8')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        c.save_board = copy.deepcopy(c.board)
        path_list = c.target()
        self.assertEqual(path_list[0], ['a1', 'g1', 'g8', 'h8'], "Path should be ['a1', 'f1', 'f8', 'h8'], not %s" % path_list[0])

    def testTargetRookFromA8(self):
        piece = 'rook'
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        node = 'a8'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'd4')
        c.board.set_piece(opp2, 'b4')
        c.board.set_piece(opp3, 'b1')
        c.board.set_piece(opp4, 'g7')
        c.board.set_piece(opp5, 'a4')
        c.board.set_piece(opp6, 'e3')
        c.board.set_piece(opp7, 'd6')
        c.board.set_piece(opp8, 'b5')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        path_list = c.target()
        answer = ['a8', 'h8', 'h1']
        self.assertEqual(path_list[0], answer, "Path should be %s, not %s" % (answer, path_list[0]))

    def testTargetRookFromB3(self):
        piece = 'rook'
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        node = 'b3'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'f7')
        c.board.set_piece(opp2, 'g4')
        c.board.set_piece(opp3, 'e8')
        c.board.set_piece(opp4, 'h4')
        c.board.set_piece(opp5, 'd4')
        c.board.set_piece(opp6, 'e7')
        c.board.set_piece(opp7, 'h2')
        c.board.set_piece(opp8, 'd2')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        path_list = c.target()
        answers = [['b3', 'b8', 'e8', 'h8']]
        self.assertIn(path_list[0],
                         answers,
                         "Path %s should be in %s" % (path_list[0], answers))

    def testTargetRookFromH1(self):
        piece = 'rook'
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        node = 'h1'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'd8')
        c.board.set_piece(opp2, 'g1')
        c.board.set_piece(opp3, 'a5')
        c.board.set_piece(opp4, 'd6')
        c.board.set_piece(opp5, 'h4')
        c.board.set_piece(opp6, 'g3')
        c.board.set_piece(opp7, 'c3')
        c.board.set_piece(opp8, 'a1')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        path_list = c.target()
        answers = [['h1', 'h4', 'h8', 'd8', 'a8']]
        self.assertIn(path_list[0],
                         answers,
                         "Path %s should be in %s" % (path_list[0], answers))

    def testTargetRookFromH8(self):
        piece = 'rook'
        opp1 = piece_factory('king', color='black')
        opp2 = piece_factory('pawn', color='black')
        opp3 = piece_factory('knight', color='black')
        opp4 = piece_factory('pawn', color='black')
        opp5 = piece_factory('rook', color='black')
        opp6 = piece_factory('bishop', color='black')
        opp7 = piece_factory('bishop', color='black')
        opp8 = piece_factory('rook', color='black')
        node = 'h8'

        c = Chessercise(piece, node)
        c.board.set_piece(opp1, 'f6')
        c.board.set_piece(opp2, 'g6')
        c.board.set_piece(opp3, 'c4')
        c.board.set_piece(opp4, 'f8')
        c.board.set_piece(opp5, 'g3')
        c.board.set_piece(opp6, 'b3')
        c.board.set_piece(opp7, 'f2')
        c.board.set_piece(opp8, 'e1')
        (c.quadrant, c.far_node) = c._get_farthest_node(node)
        c.verbose = True
        path_list = c.target()
        answers = [['h8', 'h1', 'e1', 'a1']]
        self.assertIn(path_list[0],
                         answers,
                         "Path %s should be in %s" % (path_list[0], answers))


if __name__ == '__main__':
    unittest.main()
