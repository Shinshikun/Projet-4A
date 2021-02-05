from Plateau import *
import pygame

class Piece():

    BLANC = "B"
    NOIR = "N"

    def __init__(self, x, y, couleur, type_piece, valeur):
        self.x = x
        self.y = y
        self.couleur = couleur
        self.type_piece = type_piece
        self.valeur = valeur
        self.image = pygame.image.load("sprite/"+str(self.couleur)+str(self.type_piece)+".png")

    def __str__(self):
        return self.couleur + self.type_piece + " "

    # Retourne les mouvements possibles en diagonal
    def get_diagonal_moves(self, plateau):
        moves = []

        for i in range(1, 8):
            if (not plateau.inside(self.x+i, self.y+i)):
                break
            
            moves.append(self.get_move(plateau, self.x+i, self.y+i))
            if (plateau.get_piece(self.x+i, self.y+i) != 0):
                break

        for i in range(1, 8):
            if (not plateau.inside(self.x+i, self.y-i)):
                break

            moves.append(self.get_move(plateau, self.x+i, self.y-i))
            if (plateau.get_piece(self.x+i, self.y-i) != 0):
                break

        for i in range(1, 8):
            if (not plateau.inside(self.x-i, self.y-i)):
                break
            
            moves.append(self.get_move(plateau, self.x-i, self.y-i))
            if (plateau.get_piece(self.x-i, self.y-i) != 0):
                break

        for i in range(1, 8):
            if (not plateau.inside(self.x-i, self.y+i)):
                break

            moves.append(self.get_move(plateau, self.x-i, self.y+i))
            if (plateau.get_piece(self.x-i, self.y+i) != 0):
                break

        return [move for move in moves if move != 0]

    # Retourne les mouvements possibles en horizontal / vertical
    def get_horizontal_moves(self, plateau):
        moves = []

        # Droite de la pièce
        for i in range(1, 8 - self.x):
            moves.append(self.get_move(plateau, self.x+i, self.y))
            if (plateau.get_piece(self.x+i, self.y) != 0):
                break

        # Gauche de la pièce
        for i in range(1, self.x + 1):
            moves.append(self.get_move(plateau, self.x-i, self.y))
            if (plateau.get_piece(self.x-i, self.y) != 0):
                break

        # Bas de la pièce
        for i in range(1, 8 - self.y):
            moves.append(self.get_move(plateau, self.x, self.y+i))
            if (plateau.get_piece(self.x, self.y+i) != 0):
                break

        # haut de la pièce
        for i in range(1, self.y + 1):
            moves.append(self.get_move(plateau, self.x, self.y-i))
            if (plateau.get_piece(self.x, self.y - i) != 0):
                break


        return [move for move in moves if move != 0]


    
    # Retourne le mouvement d'une piece aux coordonnées xto, yto
    def get_move(self, plateau, xto, yto):
        move = 0
        if (plateau.inside(xto, yto)):
            if (plateau.get_piece(xto, yto) != 0):
                if (plateau.get_piece(xto, yto).couleur != self.couleur):
                    move = Move(self.x, self.y, xto, yto, False)
            else:
                move = Move(self.x, self.y, xto, yto, False)

        return move
        


    
class Pion(Piece):

    TYPE_PIECE = "P"
    VALEUR = 100

    def __init__(self, x, y, couleur):
        super(Pion, self).__init__(x, y, couleur, Pion.TYPE_PIECE, Pion.VALEUR)

    def commence(self, plateau):
        if (self.couleur == Piece.NOIR):
            return self.y == 1
        else:
            return self.y == plateau.H - 2

    def get_moves(self, plateau):
        moves = []

        # Direction en fonction de la couleur
        if (self.couleur == Piece.NOIR):
            direction = 1
        else:
            direction = -1

        # Mouvement de base
        if (plateau.get_piece(self.x, self.y+direction) == 0):
            moves.append(self.get_move(plateau, self.x, self.y + direction))

        # Si le pion a pas encore bougé, il peut avancer de 2 cases
        if (self.commence(plateau) and plateau.get_piece(self.x, self.y+ direction) == 0 and plateau.get_piece(self.x, self.y + direction*2) == 0):
            moves.append(self.get_move(plateau, self.x, self.y + direction * 2))

        # Mouvement pour manger les pieces
        if (plateau.get_piece(self.x + 1, self.y + direction) != 0):
            moves.append(self.get_move(plateau, self.x + 1, self.y + direction))

        if (plateau.get_piece(self.x - 1, self.y + direction) != 0):
            moves.append(self.get_move(plateau, self.x - 1, self.y + direction))

        return [move for move in moves if move != 0]

    def clone(self):
        return Pion(self.x, self.y, self.couleur)


class Tour(Piece):

    TYPE_PIECE = "T"
    VALEUR = 563

    def __init__(self, x, y, couleur):
        super(Tour, self).__init__(x, y, couleur, Tour.TYPE_PIECE, Tour.VALEUR)

    def get_moves(self, plateau):
        return self.get_horizontal_moves(plateau)

    def clone(self):
        return Tour(self.x, self.y, self.couleur)


class Cavalier(Piece):

    TYPE_PIECE = "C"
    VALEUR = 305

    def __init__(self, x, y, couleur):
        super(Cavalier, self).__init__(x, y, couleur, Cavalier.TYPE_PIECE, Cavalier.VALEUR)

    def get_moves(self, plateau):
        moves = []

        moves.append(self.get_move(plateau, self.x-2, self.y-1))
        moves.append(self.get_move(plateau, self.x+2, self.y+1))
        moves.append(self.get_move(plateau, self.x-2, self.y+1))
        moves.append(self.get_move(plateau, self.x+2, self.y-1))
        moves.append(self.get_move(plateau, self.x-1, self.y+2))
        moves.append(self.get_move(plateau, self.x+1, self.y-2))
        moves.append(self.get_move(plateau, self.x-1, self.y-2))
        moves.append(self.get_move(plateau, self.x+1, self.y+2))

        return [move for move in moves if move != 0]

    def clone(self):
        return Cavalier(self.x, self.y, self.couleur)


class Fou(Piece):

    TYPE_PIECE = "F"
    VALEUR = 333

    def __init__(self, x, y, couleur):
        super(Fou, self).__init__(x, y, couleur, Fou.TYPE_PIECE, Fou.VALEUR)

    def get_moves(self, plateau):
        return self.get_diagonal_moves(plateau)

    def clone(self):
        return Fou(self.x, self.y, self.couleur)


class Reine(Piece):

    TYPE_PIECE = "Q"
    VALEUR = 950

    def __init__(self, x, y, couleur):
        super(Reine, self).__init__(x, y, couleur, Reine.TYPE_PIECE, Reine.VALEUR)

    def get_moves(self, plateau):
        return self.get_diagonal_moves(plateau) + self.get_horizontal_moves(plateau)

    def clone(self):
        return Reine(self.x, self.y, self.couleur)


class Roi(Piece):

    TYPE_PIECE = "K"
    VALEUR = 20000

    def __init__(self, x, y, couleur):
        super(Roi, self).__init__(x, y, couleur, Roi.TYPE_PIECE, Roi.VALEUR)

    def get_moves(self, plateau):
        moves = []

        moves.append(self.get_move(plateau, self.x+1, self.y))
        moves.append(self.get_move(plateau, self.x+1, self.y+1))
        moves.append(self.get_move(plateau, self.x, self.y+1))
        moves.append(self.get_move(plateau, self.x-1, self.y+1))
        moves.append(self.get_move(plateau, self.x-1, self.y))
        moves.append(self.get_move(plateau, self.x-1, self.y-1))
        moves.append(self.get_move(plateau, self.x, self.y-1))
        moves.append(self.get_move(plateau, self.x+1, self.y-1))

        moves.append(self.get_fort_roque(plateau))
        moves.append(self.get_faible_roque(plateau))

        return [move for move in moves if move != 0]

    def get_faible_roque(self, plateau):
        if ((self.couleur == Piece.BLANC and plateau.roi_blanc_bouge) or (self.couleur == Piece.NOIR and plateau.roi_noir_bouge)):
            return 0

        piece = plateau.get_piece(self.x+3, self.y)
        if (piece != 0):
            if (piece.couleur == self.couleur and piece.type_piece == Tour.TYPE_PIECE):
                if (plateau.get_piece(self.x+1, self.y) == 0 and plateau.get_piece(self.x+2, self.y) == 0):
                    return Move(self.x, self.y, self.x+2, self.y, True)

        return 0

    def get_fort_roque(self, plateau):
        if ((self.couleur == Piece.BLANC and plateau.roi_blanc_bouge) or (self.couleur == Piece.NOIR and plateau.roi_noir_bouge)):
            return 0

        piece = plateau.get_piece(self.x-4, self.y)
        if (piece != 0):
            if (piece.couleur == self.couleur and piece.type_piece == Tour.TYPE_PIECE):
                if (plateau.get_piece(self.x-1, self.y) == 0 and plateau.get_piece(self.x-2, self.y) == 0 and plateau.get_piece(self.x-3, self.y) == 0):
                    return Move(self.x, self.y, self.x-2, self.y, True)

        return 0


    def clone(self):
        return Roi(self.x, self.y, self.couleur)



class Move:

    def __init__(self, xfrom, yfrom, xto, yto, roque):
        self.xfrom = xfrom
        self.yfrom = yfrom
        self.xto = xto
        self.yto = yto
        self.roque = roque

    def __str__(self):
        return "(" + chr(self.xfrom+65) + "," + str(self.yfrom) + ") va en (" + chr(self.xto+65) + "," + str(self.yto) + ")"

    def egal_a(self, move2):
        return self.xfrom == move2.xfrom and self.yfrom == move2.yfrom and self.xto == move2.xto and self.yto == move2.yto


    
