from flask import Flask, render_template, request, redirect

app = Flask(__name__)

board = [''] * 9
player = 'X'
game_over = False

def check_winner():
    #Defining winning combinations
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  #Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  #Columns
        (0, 4, 8), (2, 4, 6)              #Diagonals
    ]

    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != '':
            return board[combo[0]]  #Return the winning player here

    return None  #No winner yet

@app.route('/')
def index():
    winner = check_winner()
    draw = all(cell != '' for cell in board) and not winner
    return render_template('index.html', board=board, player=player, game_over=game_over, winner=winner, draw=draw)

@app.route('/play', methods=['POST'])
def play():
    global board, player, game_over

    if request.method == 'POST':
        position = int(request.form['position'])
        if board[position] == '':
            board[position] = player
            winner = check_winner()
            if winner or all(cell != '' for cell in board):
                game_over = True
        player = 'O' if player == 'X' else 'X'
        return redirect('/')
    else:
        return "Method Not Allowed"

@app.route('/reset', methods=['POST'])
def reset():
    global board, player, game_over
    board = [''] * 9
    player = 'X'
    game_over = False
    return redirect('/')

if __name__ == '__main__':
    app.run()
