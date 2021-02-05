import pygame
from pygame.locals import *
from Pieces import *

class Plateau:

    #Constante pour la taille du plateau
    L = 8
    H = 8
    TAILLE_CASE = 40

    def __init__(self, tabPieces, roi_blanc_bouge, roi_noir_bouge, gui):
        self.tabPieces = tabPieces
        self.previous_tabPieces = []
        self.roi_blanc_bouge = roi_blanc_bouge
        self.roi_noir_bouge = roi_noir_bouge
        self.gui = gui
        self.fullmove = 1
        if gui:
            self.fenetre = pygame.display.set_mode((Plateau.L*Plateau.TAILLE_CASE, Plateau.H*Plateau.TAILLE_CASE), RESIZABLE)
            pygame.init()
            self.draw()
        
            

    def __str__(self):
        string =  "\n    A  B  C  D  E  F  G  H"
        string += "                           \n"
        for y in range(Plateau.H):
            string += str(Plateau.H - y) + " | "
            for x in range(Plateau.L):
                piece = self.tabPieces[x][y]
                if (piece != 0):
                    string += piece.__str__()
                else:
                    string += ".. "
            string += "\n"
        string += "    A  B  C  D  E  F  G  H\n"
        return string

    def fen(self):
        string = ""
        for y in range(Plateau.H):
            string2 = ""
            empty = 0
            for x in range(Plateau.L):
                piece = self.tabPieces[x][y]
                if piece == 0:
                    empty +=1
                else:
                    string2 += str(empty) if empty > 0 else ""
                    empty = 0
                    if piece.couleur == Piece.BLANC:
                        string2 += piece.type_piece.upper()
                    else:
                        string2 += piece.type_piece.lower()
            string2 += str(empty) if empty > 0 else ""
            string += string2 + "/"

        string = string[:-1]
        string = string.replace("f","b")
        string = string.replace("F","B")
        string = string.replace("t","r")
        string = string.replace("T","R")
        string = string.replace("c","n")
        string = string.replace("C","N")
        string += " b"
        string3 = ""
        if not self.roi_blanc_bouge:
            string3 += "KQ"
        if not self.roi_noir_bouge:
            string3 += "kq"
        if string3 == "":
            string += " -"
        else:
            string += " "+string3

        string += " -"
        string += " 0"
        string += " "+str(self.fullmove)
        return string
        

    def draw(self):
        self.fenetre.fill((255,255,255))
        for y in range(Plateau.H):
            for x in range(Plateau.L):
                piece = self.tabPieces[x][y]
                img = pygame.image.load("sprite/case"+str((y+x)%2)+".png")
                self.fenetre.blit(img,(x*Plateau.TAILLE_CASE,y*Plateau.TAILLE_CASE))
                if (piece != 0):
                    img = pygame.image.load("sprite/"+str(piece.couleur)+str(piece.type_piece)+".png")
                    self.fenetre.blit(img,(x*Plateau.TAILLE_CASE,y*Plateau.TAILLE_CASE))
        pygame.display.flip()

    def draw_possible_moves(self, moves):
        img = pygame.image.load("sprite/caseV.png").convert_alpha()
        img.set_alpha(127)
        self.draw()
        for move in moves:
            x = move.xto
            y = move.yto
            piece = self.tabPieces[x][y]
            self.fenetre.blit(img,(x*Plateau.TAILLE_CASE,y*Plateau.TAILLE_CASE))
            pygame.display.update(pygame.Rect(x*Plateau.TAILLE_CASE, y*Plateau.TAILLE_CASE, Plateau.TAILLE_CASE, Plateau.TAILLE_CASE))


    #Fonction pour cloner le plateau actuel
    @classmethod
    def clone(cls, plateau):
        tabPieces = [[0 for x in range(Plateau.L)] for y in range(Plateau.H)]
        for x in range(Plateau.L):
            for y in range(Plateau.H):
                if (plateau.tabPieces[x][y] != 0):
                    tabPieces[x][y] = plateau.tabPieces[x][y].clone()
                else:
                    tabPieces[x][y] = 0
        return cls(tabPieces, plateau.roi_blanc_bouge, plateau.roi_noir_bouge, False)


    #Fonction pour créer un nouveau plateau
    @classmethod
    def new(cls, gui):
        tabPieces = [[0 for x in range(Plateau.L)] for y in range(Plateau.H)]
        # On créer les pions
        for x in range(Plateau.L):
            tabPieces[x][Plateau.H-2] = Pion(x, Plateau.H-2, Piece.BLANC)
            tabPieces[x][1] = Pion(x, 1, Piece.NOIR)

        # On créer les tours
        tabPieces[0][Plateau.H-1] = Tour(0, Plateau.H-1, Piece.BLANC)
        tabPieces[Plateau.L-1][Plateau.H-1] = Tour(Plateau.L-1, Plateau.H-1, Piece.BLANC)
        tabPieces[0][0] = Tour(0, 0, Piece.NOIR)
        tabPieces[Plateau.L-1][0] = Tour(Plateau.L-1, 0, Piece.NOIR)

        # On créer les cavaliers
        tabPieces[1][Plateau.H-1] = Cavalier(1, Plateau.H-1, Piece.BLANC)
        tabPieces[Plateau.L-2][Plateau.H-1] = Cavalier(Plateau.L-2, Plateau.H-1, Piece.BLANC)
        tabPieces[1][0] = Cavalier(1, 0, Piece.NOIR)
        tabPieces[Plateau.L-2][0] = Cavalier(Plateau.L-2, 0, Piece.NOIR)

        # On créer les fous
        tabPieces[2][Plateau.H-1] = Fou(2, Plateau.H-1, Piece.BLANC)
        tabPieces[Plateau.L-3][Plateau.H-1] = Fou(Plateau.L-3, Plateau.H-1, Piece.BLANC)
        tabPieces[2][0] = Fou(2, 0, Piece.NOIR)
        tabPieces[Plateau.L-3][0] = Fou(Plateau.L-3, 0, Piece.NOIR)

        # On place le roi
        tabPieces[4][Plateau.H-1] = Roi(4, Plateau.H-1, Piece.BLANC)
        tabPieces[4][0] = Roi(4, 0, Piece.NOIR)

        # On place la reine
        tabPieces[3][Plateau.H-1] = Reine(3, Plateau.H-1, Piece.BLANC)
        tabPieces[3][0] = Reine(3, 0, Piece.NOIR)

        return cls(tabPieces, False, False, gui)


    def get_moves(self, couleur):
        moves = []
        for ligne in self.tabPieces:
            for piece in ligne:
                if (piece != 0 and piece.couleur == couleur):
                    moves += piece.get_moves(self)
        return moves



    def piece_move(self, move):
        piece = self.tabPieces[move.xfrom][move.yfrom]
        piece.x = move.xto
        piece.y = move.yto
        self.tabPieces[move.xto][move.yto] = piece
        self.tabPieces[move.xfrom][move.yfrom] = 0


        #Transformation pion en reine
        if (piece.type_piece == Pion.TYPE_PIECE):
            if (piece.y == 0 or piece.y == Plateau.H-1):
                self.tabPieces[piece.x][piece.y] = Reine(piece.x, piece.y, piece.couleur)

        #S'il y a un roque
        if (move.roque):
            if(move.xto > move.xfrom):
                tour = self.tabPieces[Plateau.L-1][move.yfrom]
                tour.x = Plateau.L - 3
                self.tabPieces[tour.x][move.yfrom] = tour
                self.tabPieces[Plateau.L-1][move.yfrom] = 0
            if(move.xto < move.xfrom):
                tour = self.tabPieces[0][move.yfrom]
                tour.x = 3
                self.tabPieces[tour.x][move.yfrom] = tour
                self.tabPieces[0][move.yfrom] = 0


        #Si le roi bouge, on ne peut plus roque
        if (piece.type_piece == Roi.TYPE_PIECE):
            if (piece.couleur == Piece.BLANC):
                self.roi_blanc_bouge = True
            else:
                self.roi_noir_bouge = True

    # On regarde si l'un des joueurs est en échec
    def echec(self, couleur):
        if (couleur == Piece.BLANC):
            adversaire = Piece.NOIR
        else:
            adversaire = Piece.BLANC


        for move in self.get_moves(adversaire):
            clone_plateau = Plateau.clone(self)
            clone_plateau.piece_move(move)
            roi_trouve = False
            for ligne in clone_plateau.tabPieces:
                for piece in ligne:
                    if piece != 0:
                        if (piece.couleur == couleur and piece.type_piece == Roi.TYPE_PIECE):
                            roi_trouve = True
            if(not roi_trouve):
                return True
                
        return False

    # Vérifie qu'on cherche bien dans le plateau
    def inside(self, x, y):
        return (x >= 0 and y >= 0 and x < Plateau.L and y < Plateau.H)
    
    # Retourne la case (x,y)
    def get_piece(self, x, y):
        if (not self.inside(x, y)):
            return 0
        return self.tabPieces[x][y]

    

    
