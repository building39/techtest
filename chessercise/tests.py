import unittest

from board import Board
from piece import piece_factory
class TestChessercise(unittest.TestCase):

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
        piece = piece_factory('bishop')
        piece.set_position('c1')
        self.failUnlessEqual(piece.legal_moves(), ['a3', 'b2', 'd2', 'e3', 'f4', 'g5', 'h6'])
        piece.set_position('d5')
        self.failUnlessEqual(piece.legal_moves(), ['a2', 'a8', 'b3', 'b7', 'c4', 'c6', 'e4', 'e6', 'f3', 'f7', 'g2', 'g8', 'h1'])

    def testKnightMoves(self):
        piece = piece_factory('knight')
        piece.set_position('b1')
        self.failUnlessEqual(piece.legal_moves(), ['a3', 'c3', 'd2'])
        piece.set_position('d5')
        self.failUnlessEqual(piece.legal_moves(), ['b4', 'b6', 'c3', 'c7', 'e3', 'e7', 'f4', 'f6'])

    def testQueenMoves(self):
        piece = piece_factory('queen')
        piece.set_position('d1')
        self.failUnlessEqual(piece.legal_moves(), ['a1', 'a4', 'b1', 'b3', 'c1', 'c2', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'e1', 'e2', 'f1', 'f3', 'g1', 'g4', 'h1', 'h5'])
        piece.set_position('e5')
        self.failUnlessEqual(piece.legal_moves(), ['a1', 'a5', 'b2', 'b5', 'b8', 'c3', 'c5', 'c7', 'd4', 'd5', 'd6', 'e1', 'e2', 'e3', 'e4', 'e6', 'e7', 'e8', 'f4', 'f5', 'f6', 'g3', 'g5', 'g7', 'h2', 'h5', 'h8'])

    def testRookMoves(self):
        piece = piece_factory('rook')
        piece.set_position('a1')
        self.failUnlessEqual(piece.legal_moves(), ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'])
        piece.set_position('d5')
        self.failUnlessEqual(piece.legal_moves(), ['d1', 'd2', 'd3', 'd4', 'd6', 'd7', 'd8', 'a5', 'b5', 'c5', 'e5', 'f5', 'g5', 'h5'])

if __name__ == '__main__':
    unittest.main()
