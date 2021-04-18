'''
cd Documents\"Sydney Uni"\2021\S1\COMP3608\Assignments\1\Tournament
Test commands

python ConnectFour.py .......,.......,.......,.......,.......,....... red M 5
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.

python ConnectFour.py ..yyrrr,..ryryr,....y..,.......,.......,....... yellow A 5
python ConnectFour.py ..yyrrr,..ryryr,....y..,.......,.......,....... yellow M 5
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|.|.|y|.|.
.|.|r|y|r|y|r
.|.|y|y|r|r|r

python ConnectFour.py .ryyrry,.rryry.,..y.r..,..y....,.......,....... yellow A 4
.|.|.|.|.|.|.
.|.|.|.|.|.|.
.|.|y|.|.|.|.
.|.|y|.|r|.|.
.|r|r|y|r|y|.
.|r|y|y|r|r|y

python ConnectFour.py rryyrry,rrryry.,..y.r..,..y....,.......,....... red A 4
.|.|y|.|.|.|.
.|.|r|y|.|.|.
.|.|y|r|y|.|.
.|.|y|y|r|r|y
r|r|r|y|r|y|y
r|r|y|y|r|r|y
'''

if __name__ == '__main__':
    start = time.time()
    board = Board(sys.argv[1])
    game = ConnectFour(sys.argv[2], sys.argv[4])
    print("STARTING BOARD")
    board.display_board()
    print(board.evaluation(game.turn_1, game.turn_2))
    print("\n")
    if sys.argv[3] == 'A':
        recommended = game.alpha_beta(0, board, np.NINF, np.inf, True)
    else:
        recommended = game.min_max(0, board, True)
    print("\nAI RECOMMENDATION:", recommended[0])
    print("NODES EXPLORED:", game.c)
    if recommended[0] == None:
        print("GAME IS TERMINAL")
    else:
        board.drop_piece(game.get_next_open_row(board.board, recommended[0]), recommended[0], game.turn_1)
        print("EVAL:", board.evaluation(game.turn_1, game.turn_2))
        print("BEST MOVE FOUND")
        board.display_board()
        s = "python ConnectFour.py " + ",".join(["".join(i) for i in board.board]) + " " + \
            ('yellow' if sys.argv[2] == 'red' else 'red') + " " + sys.argv[3] + " " + sys.argv[4]
        end = time.time()
        print(end - start)
        print(s)
        # subprocess.run(s)


if __name__ == '__main__':
    board = Board(sys.argv[1])
    game = ConnectFour(sys.argv[2], sys.argv[4])
    if sys.argv[3] == 'A':
        recommended = game.alpha_beta(0, board, np.NINF, np.inf, True)
    else:
        recommended = game.min_max(0, board, True)
    print(recommended[0])
    print(game.c)