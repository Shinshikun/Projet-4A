from Plateau import *
from Pieces import *
import chess.syzygy

class Score:

    #On fabrique les tables dites "pieces-square"
    #Qu'on trouve ici : https://www.chessprogramming.org/Simplified_Evaluation_Function
    


    @staticmethod
    def get_score(plateau):
        listeSquare = {}
        SQUARE_P =[[0,  0,  0,  0,  0,  0,  0,  0],
                       [5, 10, 10,-20,-20, 10, 10,  5],
                       [5, -5,-10,  0,  0,-10, -5,  5],
                       [0,  0,  0, 20, 20,  0,  0,  0],
                       [5,  5, 10, 25, 25, 10,  5,  5],
                       [10, 10, 20, 30, 30, 20, 10, 10],
                       [50, 50, 50, 50, 50, 50, 50, 50],
                       [0,  0,  0,  0,  0,  0,  0,  0]]
        
        SQUARE_C =[[-50,-40,-30,-30,-30,-30,-40,-50],
                           [-40,-20,  0,  5,  5,  0,-20,-40],
                           [-30,  5, 10, 15, 15, 10,  5,-30],
                           [-30,  0, 15, 20, 20, 15,  0,-30],
                           [-30,  5, 15, 20, 20, 15,  5,-30],
                           [-30,  0, 10, 15, 15, 10,  0,-30],
                           [-40,-20,  0,  0,  0,  0,-20,-40],
                           [-50,-40,-30,-30,-30,-30,-40,-50]]

        SQUARE_F =[[-20,-10,-10,-10,-10,-10,-10,-20],
                      [-10,  5,  0,  0,  0,  0,  5,-10],
                      [-10, 10, 10, 10, 10, 10, 10,-10],
                      [-10,  0, 10, 10, 10, 10,  0,-10],
                      [-10,  5,  5, 10, 10,  5,  5,-10],
                      [-10,  0,  5, 10, 10,  5,  0,-10],
                      [-10,  0,  0,  0,  0,  0,  0,-10],
                      [-20,-10,-10,-10,-10,-10,-10,-20]]

        SQUARE_T =[[0,  0,  0,  5,  5,  0,  0,  0],
                       [-5,  0,  0,  0,  0,  0,  0, -5],
                       [-5,  0,  0,  0,  0,  0,  0, -5],
                       [-5,  0,  0,  0,  0,  0,  0, -5],
                       [-5,  0,  0,  0,  0,  0,  0, -5],
                       [-5,  0,  0,  0,  0,  0,  0, -5],
                       [5, 10, 10, 10, 10, 10, 10,  5],
                       [0,  0,  0,  0,  0,  0,  0,  0]]

        SQUARE_K = [[20, 30, 10,  0,  0, 10, 30, 20],
                    [20, 20,  0,  0,  0,  0, 20, 20],
                    [-10,-20,-20,-20,-20,-20,-20,-10],
                    [-20,-30,-30,-40,-40,-30,-30,-20],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30],
                    [-30,-40,-40,-50,-50,-40,-40,-30]]

        SQUARE_Q =[[-20,-10,-10, -5, -5,-10,-10,-20],
                        [-10,  0,  0,  0,  0,  0,  0,-10],
                        [-10,  5,  5,  5,  5,  5,  0,-10],
                        [  0,  0,  5,  5,  5,  5,  0, -5],
                        [ -5,  0,  5,  5,  5,  5,  0, -5],
                        [-10,  0,  5,  5,  5,  5,  0,-10],
                        [-10,  0,  0,  0,  0,  0,  0,-10],
                        [-20,-10,-10, -5, -5,-10,-10,-20]]

        listeSquare["P"] = SQUARE_P
        listeSquare["C"] = SQUARE_C
        listeSquare["F"] = SQUARE_F
        listeSquare["T"] = SQUARE_T
        listeSquare["K"] = SQUARE_K
        listeSquare["Q"] = SQUARE_Q
        score_blanc = 0
        score_noir = 0
        #On regarde déjà le score en fonction des pièces restantes
        for ligne in plateau.tabPieces:
            for piece in ligne:
                if (piece != 0):
                    if (piece.couleur == Piece.BLANC):
                        score_blanc += piece.valeur
                        score_blanc += Score.get_position_score(plateau, piece, listeSquare)
                    else:
                        score_noir += piece.valeur
                        score_noir += Score.get_position_score(plateau, piece, listeSquare)

        return score_blanc - score_noir


    @staticmethod
    def get_position_score(plateau, piece, listeSquare):
    
        #On regarde le score en fonction des positions
        if (piece.couleur == Piece.BLANC):
            return listeSquare[piece.type_piece][piece.x][piece.y]
        else:
            return listeSquare[piece.type_piece][7 - piece.x][piece.y]
   


class Algo:
    @staticmethod
    def alphabeta(plateau, alpha, beta, bool_max, profondeur):
        if (profondeur == 0):
            return Score.get_score(plateau)

        if (bool_max):
            max_score = -10000000
            for move in plateau.get_moves(Piece.BLANC):
                clone_plateau = Plateau.clone(plateau)
                clone_plateau.piece_move(move)
                max_score = max(max_score, Algo.alphabeta(clone_plateau, alpha, beta, False, profondeur-1))
                alpha = max(alpha, max_score)
                if (beta <= alpha):
                    break
            return max_score
        
        else:
            max_score = 10000000
            for move in plateau.get_moves(Piece.NOIR):
                clone_plateau = Plateau.clone(plateau)
                clone_plateau.piece_move(move)

                max_score = min(max_score, Algo.alphabeta(clone_plateau, alpha, beta, True, profondeur-1))
                beta = min(beta, max_score)
                if (beta <= alpha):
                    break
            return max_score

    def choisi_move(plateau, tabMovesInterdits=[]):
        #Essais des tables de finales
        """fen = plateau.fen()
        with chess.syzygy.open_tablebase("D:/Users/thoma/Desktop/syzygy") as tablebase:
            print(tablebase.get_dtz(chess.Board(fen)))"""


        
        meilleur_move = 0
        meilleur_score = 10000000

        for move in plateau.get_moves(Piece.NOIR):
            reset = False
            for move_interdit in tabMovesInterdits:
                if (move_interdit.equals(move)):
                    reset = True
                    break
            if reset:
                continue

            clone_plateau = Plateau.clone(plateau)
            clone_plateau.piece_move(move)

            score = Algo.alphabeta(clone_plateau, -10000000, 10000000, True, 1)
            if score < meilleur_score:
                meilleur_score = score
                meilleur_move = move

        if meilleur_move == 0:
            return 0

        clone_plateau = Plateau.clone(plateau)
        clone_plateau.piece_move(meilleur_move)
        if (clone_plateau.echec(Piece.NOIR)):
            tabMovesInterdits.append(meilleur_move)
            return Algo.choisi_move(plateau, tabMovesInterdits)

        return meilleur_move    
