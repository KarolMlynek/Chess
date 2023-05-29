import pygame
from const import *
from board import Board
from dragger import Dragger


class Game:
    def __init__(self):
        self.next_player = "white"
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()

    def show_background(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if (row + column) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                rectangle = (column * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rectangle)

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
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = "#C86464" if (move.final.row + move.final.column) % 2 == 0 else "#C84646"
                rect = (move.final.column * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for position in [initial, final]:
                color = (244, 247, 116) if position.row + position.column %2 == 0 else (172, 195, 51)
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
        #self.hovered_square = self.board.squares[row][column]
        pass