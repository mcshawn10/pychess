import string
import random
import os
import sys
import time
import math
from turtle import bk
from IPython.display import clear_output
import pygame

pygame.init()
clock = pygame.time.Clock()

Pieces = {}  # global dictionary
all_pieces = ['bR', 'bN', 'bB', 'bQ', 'bK','bp','wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
white = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wp']
black = ['bR', 'bN', 'bB', 'bQ', 'bK','bp']

avail_white = ['wR', 'wN', 'wB', 'wQ', 'wK','wR', 'wN', 'wB','wp','wp','wp','wp','wp','wp','wp','wp']
avail_black = ['bR', 'bN', 'bB', 'bQ', 'bK','bR', 'bN', 'bB','bp','bp','bp','bp','bp','bp','bp','bp']
# needed arrays/tuples
board_arr = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
             ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
             ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

clicks_stored = []
clicks_clicked = ()
move_color = ["-"]

screen = pygame.display.set_mode((512, 512))  # Setting the screen size
screen.fill(pygame.Color((255, 228, 181)))  # intitally fills screen to be all tan color
pygame.display.set_caption("A.I. HW #2")  # title of the pygame window


class Piece:
    def __init__(self, pos, name, color):
        self.pos = pos # should be a tuple
        self.name = name
        self.color = color
        
        

class ChessRules():
    def __init__(self, curr, nxt): # where you pass in two Piece objects
        self.curr = curr
        self.nxt = nxt
        self.all_pieces = ['bR', 'bN', 'bB', 'bQ', 'bK','bp','wR', 'wN', 'wB', 'wQ', 'wK', 'wp'] 
    
    def is_legal(self): #  where n is the next coordinate (row,col)
        global board_arr
        name = self.curr.name

        if self.curr.color == self.nxt.color:
            return False
            
        if name == "pawn": # INCLUDE THE COLOR IF STATEMENT
            if self.curr.color == "white":

                if (self.curr.pos[0] == 6) and (self.nxt.pos[0] == 4) and (self.curr.pos[1]==self.nxt.pos[1]):
                    return True
                elif self.nxt.pos[0] == self.curr.pos[0]-1:
                    return True
                elif (self.nxt.pos[1] == self.curr.pos[1]+1 or self.nxt.pos[1] == self.curr.pos[1]-1) and (self.nxt.pos[0] == self.curr.pos[0]-1):
                    return True
                else: return False
            else:
                if (self.curr.pos[0] == 1) and (self.nxt.pos[0] == 3) and (self.curr.pos[1]==self.nxt.pos[1]):
                    return True
                elif self.nxt.pos[0] == self.curr.pos[0]+1:
                    return True
                elif (self.nxt.pos[1] == self.curr.pos[1]-1 or self.nxt.pos[1] == self.curr.pos[1]+1) and (self.nxt.pos[0] == self.curr.pos[0]+1):
                    return True
                else: return False        

        if name == "king":
            if abs(self.curr.pos[0]-self.nxt.pos[0])==1 or abs(self.curr.pos[1]-self.nxt.pos[1])==1:
                return True
            else: return False

        if name == "queen":
            if abs(self.curr.pos[0]-self.nxt.pos[0])>=1 or abs(self.curr.pos[1]-self.nxt.pos[1])>=1:
                if (self.curr.pos[0] == self.nxt.pos[0]) or (self.curr.pos[1] == self.nxt.pos[1]):
                    if self.is_clear_lin(self.curr.pos, self.nxt.pos):
                        return True

                elif abs(self.curr.pos[0]-self.nxt.pos[0])>=1 and abs(self.curr.pos[1]-self.nxt.pos[1])>=1:        
                    if self.is_clear_diag(self.curr.pos, self.nxt.pos):
                        return True   
            else: return False

        if name == "knight":
            col_diff = abs(self.curr.pos[1]-self.nxt.pos[1])
            row_diff = abs(self.curr.pos[0]-self.nxt.pos[0])
            if col_diff == 1 and row_diff == 2:
                return True
            if col_diff == 2 and row_diff == 1:
                return True
            else: return False

        if name == "bishop":
            
            if abs(self.curr.pos[0]-self.nxt.pos[0])>=1 and abs(self.curr.pos[1]-self.nxt.pos[1])>=1:
                
                if self.is_clear_diag(self.curr.pos, self.nxt.pos):
                    return True
            else: return False   
                    

            

        if name == "rook":
            if (self.curr.pos[0] == self.nxt.pos[0]) or (self.curr.pos[1] == self.nxt.pos[1]):
                if self.is_clear_lin(self.curr.pos, self.nxt.pos):
                    return True
            else: return False
    
    def clear_path(self, p, goal): #goal is a tuple
        if abs(self.curr.pos[0]-goal[0])==1 or abs(self.curr.pos[1]-self.goal[1])==1:
            return True
        else: return False

    def is_clear_diag(self, c, g):  # positions (r,c) of the current and the goal
        global board_arr

        if abs(c[0]-g[0])==1 and abs(c[1]-g[1])==1:
            return True  

        elif c[0]-g[0]>0 and c[1]-g[1]<0: # NE
            
            nr = c[0]-1
            nc = c[1]+1
            if board_arr[nr][nc] != '.':                                 
                return False
            else:           
                return self.is_clear_diag((nr,nc),g)            

        elif c[0]-g[0]<0 and c[1]-g[1]<0: # SE
            
            nr = c[0]+1
            nc = c[1]+1
            if board_arr[nr][nc] != '.':
                return False
            else:
                return self.is_clear_diag((nr,nc),g)

        elif c[0]-g[0]>0 and c[1]-g[1]>0: # NW
            
            nr = c[0]-1
            nc = c[1]-1
            if board_arr[nr][nc] != '.':
                return False
            else:
                return self.is_clear_diag((nr,nc),g)

        elif c[0]-g[0]<0 and c[1]-g[1]>0: # SW
            
            nr = c[0]+1
            nc = c[1]-1
            if board_arr[nr][nc] != '.':
                return False
            else:
                return self.is_clear_diag((nr,nc),g)

    def is_clear_lin(self,c , g):
        global board_arr

        if (abs(c[0]-g[0])==1 or abs(c[1]-g[1])==1):
            return True
        
        elif c[0]-g[0]>0: #  N
            nr = c[0]-1
            if board_arr[nr][c[1]] != '.':
                return False
            else:
                return self.is_clear_lin((nr,c[1]), g)

        elif c[0]-g[0]<0: #  S
            nr = c[0]+1
            if board_arr[nr][c[1]] != '.':
                return False
            else:
                return self.is_clear_lin((nr,c[1]), g)

        elif c[1]-g[1]<0: #  E
            nc = c[1]+1
            if board_arr[c[0]][nc] != '.':
                return False
            else:
                return self.is_clear_lin((c[0],nc), g)
        elif c[1]-g[1]>0: #  W
            nc = c[1]-1
            if board_arr[c[0]][nc] != '.':
                return False
            else:
                return self.is_clear_lin((c[0],nc), g)

    def in_check(self):
        k = self.get_kings()

        if self.curr.name == "rook" or self.curr.name == "queen":
            if k.pos[0] == self.nxt.pos[0] or k.pos[1] == self.nxt.pos[1]:
                print("in check")

        if self.curr.name == "bishop" or self.curr.name == "queen":
            if abs(k.pos[0]-k.pos[1]) == abs(self.nxt.pos[0]-self.nxt.pos[1]) or (k.pos[0]+k.pos[1]) == self.nxt.pos[0]+self.nxt.pos[1]:
                if self.is_clear_diag(self.nxt.pos,k.pos)==True:
                
                    print("in check")

        if self.curr.name == "pawn":
            if abs(k.pos[0]-self.nxt.pos[0])==1 and abs(k.pos[1]-self.nxt.pos[1])==1:
                print("in check") 

    def checkmate(self, c, k):
        pass 
    
        
    def get_kings(self):
        global board_arr
        
        if self.curr.color == "white":

            for i in board_arr:
                for j in i:
                    if j == 'bK':
                        coord = (board_arr.index(i),i.index(j))
                        return Piece(coord, "king","black")
        if self.curr.color == "black":
    
            for i in board_arr:
                for j in i:
                    if j == 'wK':
                        coord = (board_arr.index(i),i.index(j))
                        return Piece(coord, "king", "white")

class Moves:

    def __init__(self):
        pass

    def move_list(self):
        pass




    


class ChessBoard:
    
    def __init__(self, b):
        self.b = b  #  b = board_arr
        self.TAN = (255, 228, 181)  # RGB color combination
        self.BROWN = (139, 101, 8)
        self.rxc = 8  # dimensions of row and columns (9)
        self.height = 512  # dimensions of the board (constants)
        self.width = 512
        self.squares = 512//8  # size of our board squares
        self.colors = [pygame.Color(self.TAN), pygame.Color(self.BROWN)]
        self.PATH = r"C:\\Python\\WORTHY PROJECTS\\AI_hw\\chess_pieces\\"
    
    def board(self):        
        for row in range(self.rxc):
            for col in range(self.rxc):
                color = self.colors[((row+col) % 2)]
                pygame.draw.rect(screen, color, pygame.Rect(
                    col*self.squares, row*self.squares, self.squares, self.squares))

    def import_pieces(self):        
        pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR','wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
        for piece in pieces:
            Pieces[piece] = pygame.transform.scale(pygame.image.load(
                self.PATH + piece + ".png"), (self.squares, self.squares))

    def draw_piece(self):
        for row in range(self.rxc):
            for col in range(self.rxc):
                piece = self.b[row][col]
                if piece != '.':
                    screen.blit(Pieces[piece], pygame.Rect(col*self.squares, row*self.squares,
                                                       self.squares, self.squares))

    def move_piece(self): #ip_pos is a tuple (row, col)
        global clicks_clicked, clicks_stored, avail_black, avail_white              
        row_current, col_current = clicks_stored[0]            
        row_next, col_next = clicks_stored[1]         
        selected_piece = self.b[row_current][col_current]
        if self.b[row_next][col_next] in avail_white:
            avail_white.remove(self.b[row_next][col_next])
        if self.b[row_next][col_next] in avail_black:
            avail_black.remove(self.b[row_next][col_next])
        self.b[row_next][col_next] = '.'
        self.update()
        self.b[row_next][col_next] = selected_piece
        self.b[row_current][col_current] = '.'

        clicks_clicked = ()
        clicks_stored.clear()
            
    def what_color(self,p):
        global white, black
        if p == '.':
            return "blank"
        elif p in white:
            return "white"
        elif p in black:
            return "black"
          
    def get_name(self, p):
        name = "_"
        if p == '.':
            name = "blank"
        if p == 'bp' or p == 'wp':
            name = "pawn"            
        if p == 'wK' or p == 'bK':
            name = "king"            
        if p == 'wQ' or p == 'bQ':
            name = "queen"            
        if p == 'bR' or p == 'wR':
            name = "rook"            
        if p == 'bN' or p == 'wN':
            name = "knight"            
        if p == 'bB' or p == 'wB':
            name = "bishop"
        return name   

    def two_pieces(self, cs, cc): #returns the two pieces that are interacting
                   
        row_c, col_c = cs[0]
        selected_piece = self.b[row_c][col_c]
        name1 = self.get_name(selected_piece)  
        curr_color = self.what_color(selected_piece)
        cp = Piece(cs[0], name1, curr_color)

        row_n, col_n = cs[1] 
        next_piece = self.b[row_n][col_n]
        name2 = self.get_name(next_piece)
        next_color = self.what_color(next_piece)
        np = Piece(cs[1], name2, next_color)
        
        return cp, np

    def get_clicks(self, ip_pos, cs, cc):   
        if cc == ip_pos:
            cc = ()
            cs.clear()
        else:
            cc = ip_pos
            cs.append(cc)
        return cc, cs           
      
    def update(self):
        global screen 
        colors = [pygame.Color(self.TAN), pygame.Color(self.BROWN)]
        for row in range(self.rxc):
            for col in range(self.rxc):
                piece = self.b[row][col]
                if piece != '.':
                    screen.blit(Pieces[piece], pygame.Rect(col*self.squares, row*self.squares,
                                                       self.squares, self.squares))  # draws pieces onto the board
                elif piece == '.':
                        color = colors[((row+col) % 2)]
                        pygame.draw.rect(screen, color, pygame.Rect(
                    col*self.squares, row*self.squares, self.squares, self.squares))

    def get_pos(self,pos):
        x, y = pos
        row = y // self.squares
        col = x // self.squares
        return row, col  # get position of piece

    def inst_piece(self, pos):
        r,c = pos[0],pos[1]
        piece = self.b[r][c]
        name = self.get_name(piece)
        clr = self.what_color(piece)
        return Piece(pos,name,clr)

    
        

    def RUN_ALL(self):
        global clicks_stored, clicks_clicked, move_color
        self.board()
        self.import_pieces()
        self.draw_piece()

        while True:
        # game loop
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # command that makes the game quit
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()                    
                    x, y = self.get_pos(mouse_pos)
                                       
                    clicks_clicked, clicks_stored = self.get_clicks((x,y), clicks_stored, clicks_clicked)
                   
                    if len(clicks_stored) == 2:
                         
                        curr_piece, nxt_piece = self.two_pieces(clicks_stored, clicks_clicked)

                         
                        if move_color[0] == curr_piece.color:
                            clicks_clicked = ()
                            clicks_stored.clear()                            
                            continue

                        elif move_color[0] != curr_piece.color:
                            move_color.clear()
                            move_color.append(curr_piece.color)
                            rlz = ChessRules(curr_piece, nxt_piece)

                            if rlz.is_legal() == True:
                                rlz.in_check()
                                self.move_piece() # may need to modify to just taking in the two points
                                
                            else: 
                                clicks_clicked = ()
                                clicks_stored.clear()
                    
                    self.update()

                
                    

            
            clock.tick(60)  # clock running at 60 FPS
            pygame.display.flip()

class AI:
    def __init__(self):
        pass

    def Adversial_search(self):
        pass

    def Min_Max(self):
        pass



test = ChessBoard(board_arr)
test.RUN_ALL()
print("test")


