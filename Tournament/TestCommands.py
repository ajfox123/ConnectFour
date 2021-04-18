'''
cd Documents\"Sydney Uni"\2021\S1\COMP3608\Assignments\1\Tournament
Test commands

python ConnectFour.py .......,.......,.......,.......,.......,....... red M 1
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.

python ConnectFour.py ..yyrrr,..ryryr,....y..,.......,.......,....... yellow M 1
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|y|.|.
.|.|r|y|r|y|r
.|.|y|y|r|r|r

python ConnectFour.py .yrryyr,.yyryr.,..r.y..,..r....,.......,....... red M 1
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|r|.|.|.|.
.|.|r|.|y|.|.
.|y|y|r|y|r|.
.|y|r|r|y|y|r

python ConnectFour.py rryyrry,rrryryy,..yyrry,..yry..,..ry...,....... red M 1
.|.|.|.|.|.|.
.|.|r|y|.|.|.
.|.|y|r|y|.|.
.|.|y|y|r|r|y
r|r|r|y|r|y|y
r|r|y|y|r|r|y

python ConnectFour.py yry.yyy,rry.yyr,yyryyrr,rrryrry,yyrrryy,rryyrry red M 1
y|r|y|.|y|y|y
r|r|y|.|y|y|r
y|y|r|y|y|r|r
r|r|r|y|r|r|y
y|y|r|r|r|y|y
r|r|y|y|r|r|y

python ConnectFour.py .yyr.yr,.r.y..r,...y..r,.......,.......,....... yellow M 1
'''
s = '''y|r|y|.|y|y|y
       r|r|y|.|y|r|r
       y|y|r|y|y|y|r
       r|r|r|y|r|r|y
       y|y|r|r|r|y|y
       r|r|y|y|r|r|y'''
s = ','.join(s.replace('|', '').split()[::-1])
col = 'red'
print(f'python ConnectFour.py {s} {col} M 1')


'''

if __name__ == '__main__':
    start = time.time()
    board = Board(sys.argv[1])
    depth = 5
    game = ConnectFour(sys.argv[2], depth)
    print("STARTING BOARD")
    board.display_board()
    print(board.evaluation(game.turn_1, game.turn_2))
    print("\n")
    recommended = game.alpha_beta(0, board, np.NINF, np.inf, True)
    print("\nAI RECOMMENDATION:", recommended[0])
    if recommended[0] == None:
        print("GAME IS TERMINAL")
    else:
        board.drop_piece(game.get_next_open_row(board.board, recommended[0]), recommended[0], game.turn_1)
        print("EVAL:", board.evaluation(game.turn_1, game.turn_2))
        board.display_board()
        s = "python ConnectFour.py " + ",".join(["".join(i) for i in board.board]) + " " + \
            ('yellow' if sys.argv[2] == 'red' else 'red') + " " + sys.argv[3] + " " + sys.argv[4]
        end = time.time()
        print(end - start)
        print(s)
        subprocess.run(s)




if __name__ == '__main__':
    board = Board(sys.argv[1])
    depth = 5
    game = ConnectFour(sys.argv[2], depth)
    recommended = game.alpha_beta(0, board, np.NINF, np.inf, True)
    print(recommended[0])
    
'''
