import copy
import os
from const import *
from square import Square
from piece import *
from move import Move
from sound import Sound


class Board:
    def __init__(self):
        self.squares = []
        self._create()
        self.last_move = None
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final
        en_passant_empty = self.squares[final.row][final.column].is_empty()
        self.squares[initial.row][initial.column].piece = None
        self.squares[final.row][final.column].piece = piece
        if piece.name == "pawn":
            diff = final.column - initial.column
            if diff != 0 and en_passant_empty:
                self.squares[initial.row][initial.column].piece = None
                self.squares[final.row][final.column].piece = piece
                if not testing:
                    sound = Sound(os.path.join("assets/sounds/capture.wav"))
                    sound.play()

            else:
                self.check_promotion(piece, final)

        if piece.name == "king":
            if self.castling(initial, final) and not testing:
                diff = final.column - initial.column
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])
        piece.moved = True
        piece.clear_moves()
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.column].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.column - final.column) == 2

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        for row in range(ROWS):
            for column in range(COLUMNS):
                if isinstance(self.squares[row][column].piece, Pawn):
                    self.squares[row][column].piece.en_passant = False
        piece.en_passant = True

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move, testing=True)
        for row in range(ROWS):
            for column in range(COLUMNS):
                if temp_board.squares[row][column].has_rival_piece(piece.color):
                    p = temp_board.squares[row][column].piece
                    temp_board.calculate_moves(p, row, column, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calculate_moves(self, piece, row, column, bool=True):
        def pawn_moves():
            if piece.moved:
                steps = 1
            else:
                steps = 2
            start = row + piece.direction
            end = row + (piece.direction * (1 + steps))
            for possible_move_row in range(start, end, piece.direction):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][column].is_empty():
                        initial = Square(row, column)
                        final = Square(possible_move_row, column)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else:
                        break
                else:
                    break
            possible_move_row = row + piece.direction
            possible_move_columns = [column-1, column+1]
            for possible_move_column in possible_move_columns:
                if Square.in_range(possible_move_row, possible_move_column):
                    if self.squares[possible_move_row][possible_move_column].has_rival_piece(piece.color):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_move_row][possible_move_column].piece
                        final = Square(possible_move_row, possible_move_column, final_piece)
                        move = Move(initial, final)
                        piece.add_move(move)

            r = 3 if piece.color == "white" else 4
            fr = 2 if piece.color == "white" else 5
            if Square.in_range(column-1) and row == r:
                if self.squares[row][column-1].has_rival_piece(piece.color):
                    p = self.squares[row][column-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, column)
                            final = Square(fr, column-1, p)
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

            if Square.in_range(column+1) and row == r:
                if self.squares[row][column+1].has_rival_piece(piece.color):
                    p = self.squares[row][column+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, column)
                            final = Square(fr, column+1, p)
                            move = Move(initial, final)

                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)


        def knight_moves():
            possible_moves = [
                (row-2, column+1), (row-1, column+2), (row+1, column+2), (row+2, column+1), (row+2, column-1),
                (row+1, column-2), (row-1, column-2), (row-2, column-1)
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_column = possible_move
                if Square.in_range(possible_move_row, possible_move_column):
                    if self.squares[possible_move_row][possible_move_column].empty_or_rival(piece.color):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_move_row][possible_move_column].piece
                        final = Square(possible_move_row, possible_move_column, final_piece)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

        def straight_line_moves(increments):
            for increment in increments:
                row_increment, column_increment = increment
                possible_move_row = row + row_increment
                possible_move_column = column + column_increment
                while True:
                    if Square.in_range(possible_move_row, possible_move_column):
                        initial = Square(row, column)
                        final_piece = self.squares[possible_move_row][possible_move_column].piece
                        final = Square(possible_move_row, possible_move_column, final_piece)
                        move = Move(initial, final)
                        if self.squares[possible_move_row][possible_move_column].is_empty():
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        elif self.squares[possible_move_row][possible_move_column].has_rival_piece(piece.color):
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break
                        elif self.squares[possible_move_row][possible_move_column].has_team_piece(piece.color):
                            break
                    else:
                        break
                    possible_move_row = possible_move_row + row_increment
                    possible_move_column = possible_move_column + column_increment

        def king_moves():
            adjs = [
                (row-1, column+0), (row-1, column+1), (row+0, column+1), (row+1, column+1),
                (row+1, column+0), (row+1, column-1), (row+0, column-1), (row-1, column-1)
            ]
            for possible_move in adjs:
                possible_move_row, possible_move_column = possible_move
                if Square.in_range(possible_move_row, possible_move_column):
                    if self.squares[possible_move_row][possible_move_column].empty_or_rival(piece.color):
                        initial = Square(row, column)
                        final = Square(possible_move_row, possible_move_column)
                        move = Move(initial, final)
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)
            if not piece.moved:
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for col in range(1, 4):
                            if self.squares[row][col].has_piece():
                                break
                            if col == 3:
                                piece.left_rook = left_rook
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)

                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for col in range(5, 7):
                            if self.squares[row][col].has_piece():
                                break
                            if col == 6:
                                piece.right_rook = right_rook
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)

        if piece.name == "pawn":
            pawn_moves()
        elif piece.name == "knight":
            knight_moves()
        elif piece.name == "bishop":
            straight_line_moves([
                (-1, 1), (-1, -1), (1, 1), (1, -1)
            ])
        elif piece.name == "rook":
            straight_line_moves([
                (-1, 0), (0, 1), (1, 0), (0, -1)
            ])
        elif piece.name == "queen":
            straight_line_moves([
                (-1, 1), (-1, -1), (1, 1), (1, -1), (-1, 0), (0, 1), (1, 0), (0, -1)
            ])
        elif piece.name == "king":
            king_moves()

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(COLUMNS)]
        for row in range(ROWS):
            for column in range(COLUMNS):
                self.squares[row][column] = Square(row, column)

    def _add_pieces(self, color):
        if color == "white":
            row_pawn, row_other = (6, 7)
        else:
            row_pawn, row_other = (1, 0)
        for column in range(COLUMNS):
            self.squares[row_pawn][column] = Square(row_pawn, column, Pawn(color))

        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        self.squares[row_other][4] = Square(row_other, 4, King(color))