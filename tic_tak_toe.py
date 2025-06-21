import tkinter as tk
from tkinter import messagebox

# --- CONFIGURABLE COLORS ---
X_COLOR = "#ff4b5c"   # Neon Red
O_COLOR = "#56cfe1"   # Soft Blue
WIN_HIGHLIGHT = "#80ed99"
BTN_COLOR = "#ffffff"
HOVER_COLOR = "#cdeffd"
GRADIENT_START = "#f8cdda"
GRADIENT_END = "#1d2b64"

# --- GAME STATE ---
board = [""] * 9
current_player = "X"
buttons = []

# --- ROOT SETUP ---
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("400x500")
root.resizable(False, False)

# --- STATUS TEXT ---
status_text = tk.StringVar()
status_text.set("Your turn (X)")

# --- CREATE GRADIENT BACKGROUND ---
gradient_canvas = tk.Canvas(root, width=400, height=500)
gradient_canvas.pack(fill="both", expand=True)

def draw_gradient(canvas, start, end):
    r1, g1, b1 = root.winfo_rgb(start)
    r2, g2, b2 = root.winfo_rgb(end)
    r_ratio = (r2 - r1) / 400
    g_ratio = (g2 - g1) / 400
    b_ratio = (b2 - b1) / 400

    for i in range(400):
        nr = int(r1 + (r_ratio * i)) >> 8
        ng = int(g1 + (g_ratio * i)) >> 8
        nb = int(b1 + (b_ratio * i)) >> 8
        color = f"#{nr:02x}{ng:02x}{nb:02x}"
        canvas.create_line(0, i, 400, i, fill=color)

draw_gradient(gradient_canvas, GRADIENT_START, GRADIENT_END)

# --- BUTTON LAYER ---
btn_frame = tk.Frame(gradient_canvas, bg="", padx=20, pady=20)
btn_frame.place(relx=0.5, rely=0.4, anchor="center")

# --- WINNING COMBOS ---
WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

# --- CHECK WINNER ---
def check_winner(b):
    for a, b_, c in WIN_COMBOS:
        if b[a] == b[b_] == b[c] != "":
            return b[a]
    if all(cell != "" for cell in b):
        return "Draw"
    return None

# --- HANDLE PLAYER CLICK ---
def on_click(index):
    global current_player
    if board[index] == "" and current_player == "X":
        board[index] = "X"
        buttons[index].config(text="X", fg=X_COLOR, state="disabled")
        result = check_winner(board)
        if result:
            handle_result(result)
        else:
            current_player = "O"
            status_text.set("AI is thinking...")
            root.after(600, ai_move)

# --- AI MOVE (Minimax) ---
def ai_move():
    global current_player
    move = best_move()
    if move is not None:
        board[move] = "O"
        buttons[move].config(text="O", fg=O_COLOR, state="disabled")
    result = check_winner(board)
    if result:
        handle_result(result)
    else:
        current_player = "X"
        status_text.set("Your turn (X)")

def best_move():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

def minimax(b, is_max):
    result = check_winner(b)
    if result == "X": return -1
    if result == "O": return 1
    if result == "Draw": return 0

    if is_max:
        best = -float("inf")
        for i in range(9):
            if b[i] == "":
                b[i] = "O"
                best = max(best, minimax(b, False))
                b[i] = ""
        return best
    else:
        best = float("inf")
        for i in range(9):
            if b[i] == "":
                b[i] = "X"
                best = min(best, minimax(b, True))
                b[i] = ""
        return best

# --- HANDLE WIN/DRAW ---
def handle_result(winner):
    if winner == "Draw":
        status_text.set("It's a draw!")
    else:
        status_text.set(f"🎉 {winner} wins!")
    highlight_buttons(winner)
    root.after(2000, reset_game)

def highlight_buttons(winner):
    for i, btn in enumerate(buttons):
        if winner == "Draw" or board[i] == winner:
            btn.config(bg=WIN_HIGHLIGHT)

def reset_game():
    global board, current_player
    board = [""] * 9
    current_player = "X"
    status_text.set("Your turn (X)")
    for btn in buttons:
        btn.config(text="", state="normal", bg=BTN_COLOR)

# --- HOVER EFFECTS ---
def on_enter(e, btn):
    index = buttons.index(btn)
    if board[index] == "" and current_player == "X":
        btn.config(bg=HOVER_COLOR)

def on_leave(e, btn):
    index = buttons.index(btn)
    if board[index] == "":
        btn.config(bg=BTN_COLOR)

# --- CREATE BUTTON GRID ---
for i in range(9):
    btn = tk.Button(btn_frame, text="", font=("Arial", 30, "bold"), width=4, height=2,
                    bg=BTN_COLOR, relief="flat", command=lambda i=i: on_click(i))
    btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))
    btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))
    buttons.append(btn)

# --- STATUS BAR ---
status_label = tk.Label(root, textvariable=status_text,
                        font=("Arial", 16, "bold"),
                        bg="#000000", fg="#ffffff", pady=10)
status_label.place(relx=0.5, rely=0.9, anchor="center")

# --- RUN ---
root.mainloop()
