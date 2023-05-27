from const import *
from square import Square
from piece import *
from move import Move


class Board:
    def __init__(self):
        self.squares = []
        self._create()
        self.last_move = None
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        self.squares[initial.row][initial.column].piece = None
        self.squares[final.row][initial.column].piece = piece
        piece.moved = True
        piece.clear_moves()
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calculate_moves(self, piece, row, column):
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
                        final = Square(possible_move_row, possible_move_column)
                        move = Move(initial, final)
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
                        final = Square(possible_move_row, possible_move_column)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straight_line_moves(increments):
            for increment in increments:
                row_increment, column_increment = increment
                possible_move_row = row + row_increment
                possible_move_column = column + column_increment
                while True:
                    if Square.in_range(possible_move_row, possible_move_column):
                        initial = Square(row, column)
                        final = Square(possible_move_row, possible_move_column)
                        move = Move(initial, final)
                        if self.squares[possible_move_row][possible_move_column].is_empty():
                            piece.add_move(move)
                        if self.squares[possible_move_row][possible_move_column].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break
                        if self.squares[possible_move_row][possible_move_column].has_team_piece(piece.color):
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
                        piece.add_move(move)

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
            pass
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