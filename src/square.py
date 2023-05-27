class Square:
    def __init__(self, row, column, piece=None):
        self.row = row
        self.column = column
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def has_piece(self):
        return self.piece is not None

    def is_empty(self):
        return self.piece is None

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def empty_or_rival(self, color):
        return self.is_empty() or self.has_rival_piece(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

