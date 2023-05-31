class Square:

    ALPHACOLS = {0: "a", 1: "b", 2: "c", 3: "d",4: "e", 5: "f", 6: "g", 7: "h"}

    def __init__(self, row, column, piece=None):
        self.row = row
        self.column = column
        self.piece = piece
        self.alphacol = self.ALPHACOLS[column]

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

    @staticmethod
    def get_alphacol(column):
        ALPHACOLS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
        return ALPHACOLS[column]