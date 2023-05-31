import pygame
import sys
from game import Game
from const import *
from square import Square
from move import Move


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        while True:
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_move(screen)
            game.show_pieces(screen)
            game.show_hover(screen)
            if dragger.dragging:
                dragger.update_blit(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_column = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_column].has_piece():
                        piece = board.squares[clicked_row][clicked_column].piece
                        if piece.color == game.next_player:
                            board.calculate_moves(piece, clicked_row, clicked_column)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_move(screen)
                            game.show_pieces(screen)
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_column = event.pos[0] // SQSIZE
                    game.set_hoover(motion_row, motion_column)
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_move(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_column = dragger.mouseX // SQSIZE
                        initial = Square(dragger.initial_row, dragger.initial_column)
                        final = Square(released_row, released_column)
                        move = Move(initial, final)
                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_column].has_piece()
                            board.move(dragger.piece, move)
                            game.sound_effect(captured)
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()
                    dragger.undrag_piece()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        game.change_theme()
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()




main = Main()
main.mainloop()
