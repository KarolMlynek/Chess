import pygame
from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square


class Game:
    def __init__(self):
        self.next_player = "white"
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    def show_background(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for column in range(COLUMNS):
                color = theme.background.light if (row + column) %2 == 0 else theme.background.dark
                rectangle = (column * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rectangle)
                if column == 0:
                    color = theme.background.dark if row % 2 == 0 else theme.background.light
                    lbl = self.config.font.render(str(ROWS - row), 1, color)
                    lbl_position = (5, 5 + row * SQSIZE)
                    surface.blit(lbl, lbl_position)
                if row == 7:
                    color = theme.background.dark if (row + column) % 2 == 0 else theme.background.light
                    label = self.config.font.render(Square.get_alphacol(column), 1, color)
                    label_position = (column * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(label, label_position)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if self.board.squares[row][column].has_piece():
                    piece = self.board.squares[row][column].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        image_center = column * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=image_center)
                        surface.blit(img, piece.texture_rect)

    def show_move(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.column) % 2 == 0 else theme.moves.dark
                rect = (move.final.column * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for position in [initial, final]:
                color = theme.trace.light if position.row + position.column %2 == 0 else theme.trace.dark
                rect = (position.column * SQSIZE, position.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_square:
            color = (180, 180, 180)
            rect = (self.hovered_square.column * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    def set_hoover(self, row, column):
        self.hovered_square = self.board.squares[row][column]

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()