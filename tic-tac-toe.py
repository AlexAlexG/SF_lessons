# Игра «Крестики-нолики».
# Размер поля 3x3.

import random

# print tic-tac-toe
def print_tic():
    for i in tic:
        print(i)

#input step of player
def input_player(s):
    i = input(f"Enter {s} 0/1/2 ")
    if i == '0' or i == '1' or i == '2':
        return int(i)
    else:
        print(f"Error! You input {s} = {i}. Enter please 0, 1 or 2")
        return input_player(s)

#check that cell is free
def free_cell(r,c,check):
    t =tic[r+1]
    if t[c*2+2] == '-':
        tt = t[:c*2+2]+check+t[c*2+3:]
        tic[r + 1] = tt
        return 1
    else:
        return 0

#step by player
def step_pl(check):
    global step_game
    row = input_player('row')
    column = input_player('column')
    free_c = free_cell(row, column, check)
    if free_c == 0:
        print('This cell not free. Try again')
        return step_pl(check)
    else:
        step_game+= 1

#check how many steps. Must be <9
def game_over():
    if step_game == 9:
        print("Game over! Draw!")
        return 0
    else:
        return 1

#check for win
def win(check):
    j =0
    d1 = d2 = r1 =r2 =r3 =''
    for i in tic[1:]:
        j+= 2
        if i[1:]== (' '+check)*3:
            print(f'Congratulations! Win {check}')
            return 0
        d1+=i[j]
        d2+=i[8-j]
        r1+=i[2]
        r2+=i[4]
        r3+=i[6]
    ch=check*3
    if d1 == ch or d2 == ch or r1 ==ch or r2 ==ch or r3 ==ch:
        print(f'Congratulations! Win {check}!')
        return 0
    return 1


# tic-tac-toe programm
print("New Game of tic-tac-toe!")
tic = ["  0 1 2", "0 - - - ", "1 - - -", "2 - - -"]
step_game = 0

print_tic() #print plant
while 1:
    print("Step by player 1:")
    step_pl('x') #step by player 1
    print_tic() #print plant
    win_pl = win('x') #check the win
    if win_pl == 0 or game_over() == 0: #escape if X win or ouer
        break

    print("Step by player 2:")
    #step_comp() # ход компьютера
    step_pl('O')  # step by player
    print_tic()
    win_pl = win('O')
    if win_pl == 0 or game_over() == 0:
        break
