from Plateau import *
from Pieces import *
from IA_alpha_beta import *
from enum import Enum
import pygame
from math import *
import threading


def move_joueur():
    depart = input("Case de départ: ")
    fin = input("Case de fin: ")
    depart = depart.replace(" ","")
    fin = fin.replace(" ","")
    try:
        return Move(int(ord(depart[0]))-65, 8-int(depart[1]), int(ord(fin[0]))-65, 8-int(fin[1]), False)
    except ValueError:
        print("Pas bonne case")
        return move_joueur()


def get_move_joueur(plateau):
    while True:
        move_choisi = move_joueur()
        tabMoves = plateau.get_moves(Piece.BLANC)
        if (not tabMoves):
            return 0

        for move in tabMoves:
            if(move_choisi.egal_a(move)):
                return move
        print("mouvement impossible")

def tour_ia(plateau):
    move_ia =  Algo.choisi_move(plateau)
    if (not move_ia):
        if(plateau.echec(Piece.NOIR)):
            print("Echec et mat, le joueur a gagné")
        else:
            print("Egalité")
    plateau.piece_move(move_ia)
    plateau.fullmove += 1
    check_echec(plateau)
    plateau.draw()
    

def check_echec(plateau):
    tabMoves = checkmat_can_move(plateau.get_moves(Piece.BLANC), plateau)
    if not tabMoves:
        if(plateau.echec(Piece.BLANC)):
            print("Echec et mat, l'IA a gagné")
            return 1
        else:
            print("Egalité")
            return 1
            

def checkmat_can_move(movesPossibles, plateau):
    moves = []
    for move in movesPossibles:
        clone_plateau = Plateau.clone(plateau)
        clone_plateau.piece_move(move)
        if not (clone_plateau.echec(Piece.BLANC)):
            moves.append(move)
    return moves

    

plateau = Plateau.new(True)
print(plateau)
etape = 1
clock = pygame.time.Clock()
pieceSelect = 0
t = threading.Thread(target=tour_ia, args=[plateau])

while True:
    if plateau.gui:
        clock.tick(120)
        x, y = pygame.mouse.get_pos()
        x = ceil(x/Plateau.TAILLE_CASE) - 1
        y = ceil(y/Plateau.TAILLE_CASE) - 1
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                caseSelect = plateau.tabPieces[x][y]
                if caseSelect != 0:
                    if caseSelect.couleur == Piece.BLANC:
                        pieceSelect = caseSelect
                        movesPossibles = checkmat_can_move(pieceSelect.get_moves(plateau), plateau)
                        plateau.draw_possible_moves(movesPossibles)
                    elif caseSelect.couleur == Piece.NOIR and pieceSelect != 0 and not t.is_alive():
                        for move in movesPossibles:
                            if (x, y) == (move.xto, move.yto):
                                plateau.piece_move(move)
                                plateau.draw()
                                t = threading.Thread(target=tour_ia, args=[plateau])
                                t.start()
                    else:
                        pieceSelect = 0
                        plateau.draw()
                    
                elif not t.is_alive():
                    for move in movesPossibles:
                        if (x, y) == (move.xto, move.yto):
                            plateau.piece_move(move)
                            plateau.draw()
                            t = threading.Thread(target=tour_ia, args=[plateau])
                            t.start()
                else:
                    plateau.draw()
                        
                                
            if event.type == pygame.QUIT:
                pygame.quit()


        
        
            

    else:
        move = get_move_joueur(plateau)
        if (move == 0):
            if(plateau.echec(Piece.BLANC)):
                print("Echec et mat, l'IA a gagné")
            else:
                print("Egalité")
            break

        plateau.piece_move(move)

        print("Mouvement: " + move.__str__())
        print(plateau)

        move_ia = Algo.choisi_move(plateau)
        if (not move_ia):
            if(plateau.echec(Piece.NOIR)):
                print("Echec et mat, le joueur a gagné")
            else:
                print("Egalité")
            break

        plateau.piece_move(move_ia)
        print("Mouvement de l'IA: " + move_ia.__str__())
        print(plateau)
    
           





    
