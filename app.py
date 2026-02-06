# Task 1 - Week 1: Building and Developing AI Models Bootcamp
# Presented by: Amjad Althobaiti
# Description :Tic-Tac-Toe with AI integration, NumPy logic, and Pandas analytics.

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
import os
import openai

app = Flask(__name__)



#Game Board Setup using NumPy
board = np.full((3, 3), "", dtype=object)
players = {}      
current_turn = ""  
winner = None     
game_mode = ""     
results_file = "results.csv"




# Configure OpenAI
client = openai.OpenAI(api_key="sk-proj-...")




# Win/Draw Logic using NumPy 
def check_logic():
    global winner
    for i in range(3):
        if all(board[i, :] == board[i, 0]) and board[i, 0] != "": return True
        if all(board[:, i] == board[0, i]) and board[0, i] != "": return True
    if board[0, 0] == board[1, 1] == board[2, 2] != "": return True
    if board[0, 2] == board[1, 1] == board[2, 0] != "": return True
    return False





def get_ai_move(board_state, ai_symbol):
    system_prompt = (
        "You are a Tic-Tac-Toe Grandmaster. Priority: "
        "1. Win if possible. 2. Block opponent. 3. Take center. "
        f"You play as {ai_symbol}."
    )
    user_prompt = f"Board: {board_state}. Reply ONLY 'row,col'."
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        move = response.choices[0].message.content.strip()
        return map(int, move.split(','))
    except:
        # Fallback to random if API fails
        empty_cells = np.argwhere(board == "")
        return empty_cells[np.random.choice(len(empty_cells))]



def save_analysis(p1, p2, game_result):
    """Extra: Record statistics using Pandas"""
    new_data = pd.DataFrame([
        {"Player": p1, "Result": "Win" if game_result == p1 else ("Draw" if game_result == "Draw" else "Loss")},
        {"Player": p2, "Result": "Win" if game_result == p2 else ("Draw" if game_result == "Draw" else "Loss")}
    ])
    if os.path.exists(results_file):
        df = pd.read_csv(results_file)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(results_file, index=False)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/setup/<mode>", methods=["GET", "POST"])
def setup(mode):
    global board, players, current_turn, winner, game_mode
    game_mode = mode
    if request.method == "POST":
        p1 = request.form.get("player1_name")
        sym = request.form.get("player1_symbol")
        p2 = request.form.get("player2_name") if mode == "pvp" else "OpenAI_Bot"
        
        players = {p1: sym, p2: ("O" if sym == "X" else "X")}
        board = np.full((3, 3), "", dtype=object)
        

        # X starts first
        current_turn = p1 if players[p1] == "X" else p2
        winner = None

        # AI  Logic
        if game_mode == "ai" and current_turn == "OpenAI_Bot":
            ai_row, ai_col = get_ai_move(board.tolist(), players[current_turn])
            board[ai_row, ai_col] = players[current_turn]
            current_turn = p1 
            
        return redirect(url_for("index"))
    return render_template("setup.html", mode=mode)


@app.route("/index", methods=["GET", "POST"])
def index():
    global current_turn, winner
    if request.method == "POST" and not winner:
        row, col = int(request.form["row"]), int(request.form["col"])

        if board[row, col] == "":
            board[row, col] = players[current_turn]
            
            if check_logic():
                winner = current_turn
            elif "" not in board:
                winner = "Draw"
            else:
                #Switch to AI or Player 2
                current_turn = [n for n in players if n != current_turn][0]
                
                #AI Auto-Response
                if game_mode == "ai" and not winner:
                    ai_row, ai_col = get_ai_move(board.tolist(), players[current_turn])
                    if board[ai_row, ai_col] == "":
                        board[ai_row, ai_col] = players[current_turn]
                        if check_logic():
                            winner = current_turn
                        elif "" not in board:
                            winner = "Draw"
                        else:
                            current_turn = [n for n in players if n != current_turn][0]

            if winner:
                save_analysis(list(players.keys())[0], list(players.keys())[1], winner)

    return render_template("index.html", board=board.tolist(), turn=current_turn, winner=winner, players_list=list(players.keys()))

@app.route("/leaderboard")
def leaderboard():
    if os.path.exists(results_file):
        df = pd.read_csv(results_file)
        analysis = df[df["Result"] == "Win"].groupby("Player").size().reset_index(name="Wins")
        table_html = analysis.sort_values(by="Wins", ascending=False).to_html(classes="cyber-table", index=False)
    else:
        table_html = "<p class='no-data'>NO BATTLE DATA FOUND</p>"
    return render_template("leaderboard.html", table=table_html)

if __name__ == "__main__":
    app.run(debug=True)