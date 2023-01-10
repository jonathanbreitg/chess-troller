import chess
import sys
import os

DEPTH = 4
COLOR = chess.BLACK
OPP_COLOR = chess.WHITE
HALF_MOVES = 0

def safe_reverse(arr):
    new_arr = []
    for i in range(0,len(arr)):
     #   print(len(arr)-i-1)
        new_arr.append(arr[len(arr)-i-1])
    return new_arr

def list_game_moves(board):
    moves = []
    print(f"list_game_moves : board is:")
    print(board)
    while True:
        try:
    #        print(moves)
            moves.append(board.pop())
        except Exception as E:
    #        print(f"broke, {moves}")
            break
    #print(moves)
    moves= safe_reverse(moves)
    for move in  moves:
        board.push(move)
    return moves

def eval_board(board1):
    self_val = 0

    self_val += len((board1.pieces(chess.ROOK,COLOR))) * 5
    self_val += len((board1.pieces(chess.PAWN,COLOR))) 
    self_val += len((board1.pieces(chess.BISHOP,COLOR))) * 3
    self_val += len((board1.pieces(chess.KNIGHT,COLOR))) * 3
    self_val += len((board1.pieces(chess.QUEEN,COLOR))) * 9

    enemy_val = 0
    enemy_val += len((board1.pieces(chess.ROOK,OPP_COLOR))) * 5
    enemy_val += len((board1.pieces(chess.PAWN,OPP_COLOR))) 
    enemy_val += len((board1.pieces(chess.BISHOP,OPP_COLOR))) * 3
    enemy_val += len((board1.pieces(chess.KNIGHT,OPP_COLOR))) * 3
    enemy_val += len((board1.pieces(chess.QUEEN,OPP_COLOR))) * 9
    return -1*(self_val - enemy_val)


def chooser(board,moves):
    global COLOR
    worst_move_val = 999999999
    try:

        worst_move = moves[0]
    except Exception as e:
        print("CHECKMATE!!!")
        sys.exit(0)
    for move in moves:
        board.push(move)
        move_val = eval_board(board)
        board.pop()
        if (move_val < worst_move_val):
            worst_move = move
            worst_move_val = move_val
    return worst_move



def good_move_picker(board1,moves,n):
    board = board1
    global HALF_MOVES
    n-=1
    max = 0
    if (len(moves) == 0):
        print(f"mate in {DEPTH-n}")
        print("moves to get to this mate:")
        list_game_moves(board)
        return None, 999
    best_move = moves[0]

    if (n==0):
        for move in moves:
            board.push(move)
            curr_eval = eval_board(board)
            if (curr_eval > max):
                max = curr_eval
                best_move = move
            board.pop()
    else:
        for move in moves:
            board.push(move)
            best_sub_move,val =good_move_picker(board,list(board.legal_moves),n)
            print(f"val is {val}, max is {max}, n is {n}")
            print(f"best move: {best_move}")
            if (val>= max):
                print(f"Half moves: {HALF_MOVES}")
                best_move = list_game_moves(board)[HALF_MOVES]
                max = val
                print(f"current best movelist:,{val} is new val ")

          #  print("line 100 board:")
           # print(board)
            board.pop()
    return best_move, max

board = chess.Board()
print(board)


while True:
    is_checking = False
    
    player_move = chess.Move.from_uci(input("input move for player:"))
    while (not player_move in board.legal_moves):
        print("illegal move! input again")
        player_move = chess.Move.from_uci(input("input move for player:"))
    print(player_move)

    #print(chess.square_name(player_move.to_square)[1])
    if (board.piece_type_at(player_move.from_square) == chess.PAWN and chess.square_name(player_move.to_square)[1] == "8"):
        print("what do you want to promote to?")
        promote_piece = input("piece: (one letter)").upper()
        promote_dict = {"Q":5,"N":2,"B":3,"R":4}
        promote_piece = promote_dict.get(promote_piece)
        player_move.promotion = promote_piece
    if (board.gives_check(player_move) == True):
        is_checking = True
    board.push(player_move)
    HALF_MOVES+= 1

    
    move,val = good_move_picker(board,list(board.legal_moves),DEPTH)
    board.push(move)
    HALF_MOVES+= 1
    print("\n"*8)
    print(board)
    print(f"move valuation is {val}")

    if (is_checking):
        print("check!")

    