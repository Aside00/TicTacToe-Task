## TicTacToe-Task
# Task 1 - Week 1: Building and Developing AI Models Bootcamp
# Developed by: Amjad Althobaiti

This project is a modern, web-based Tic-Tac-Toe game that integrates Generative AI for a challenging gameplay experience. It demonstrates the use of NumPy for game logic, Pandas for data analytics, and OpenAI's GPT-3.5 as a strategic opponent.

# 🛠️ Tech Stack
Backend: Python (Flask)

AI Engine: OpenAI API (GPT-3.5 Turbo)

Data Science: NumPy (Matrix logic) & Pandas (Leaderboard analysis)

Frontend: HTML5, CSS3 (Cyberpunk/Neon Theme), JavaScript

# ✨ Key Features
AI Opponent: A strategic AI that uses prompt engineering to analyze the board and make optimal moves.

Real-time Analytics: Uses Pandas to track wins/losses and generate a live leaderboard from a CSV database.

High Performance: Powered by NumPy for lightning-fast win/draw detection via matrix slicing.

Responsive UI: A futuristic "Cyberpunk" interface with glassmorphism effects.

# 🎮 How to Run
Clone the Repo:

# Install Dependencies:
pip install flask numpy pandas openai

# Set Up OpenAI API Key: Replace the key in app.py or set it as an environment variable.

# Launch the Game:
python app.py
Access: Open http://127.0.0.1:5000 in your browser.

## 📊 Logic Implementation
# Game State: 
Managed using a 3x3 NumPy array for efficient row/column checking.

# Leaderboard:
Automatically saves results to results.csv and processes them using Pandas DataFrames.

# AI Prompting: 
Optimized using temperature=0 and explicit "Available Moves" filtering to ensure valid and smart gameplay.

