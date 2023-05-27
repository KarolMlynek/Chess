import pygame
from const import *
from board import Board
from dragger import Dragger


class Game:
    def __init__(self):
        self.next_player = "white"
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

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"
