import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import bcrypt
import chessGUI
import chessAnalysisPage

# Function to create a connection to MySQL database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='chess_login',
            user='root',
            password='Jayden00!'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Function to close the connection to MySQL database
def close_connection(connection):
    if connection:
        connection.close()

# Function to register a new user
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, hashed_password))
            connection.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            close_connection(connection)
            root.withdraw()  # Hide the login window
            open_options_window()
    except Error as e:
        messagebox.showerror("Error", f"Error registering user: {e}")
        close_connection(connection)

# Function to authenticate user login
def login_user():
    username = username_entry.get()
    password = password_entry.get()
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT password FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()
            if user_data:
                stored_password = user_data[0].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    messagebox.showinfo("Success", "Login successful!")
                    root.withdraw()  # Hide the login window
                    open_options_window()
                else:
                    messagebox.showerror("Error", "Invalid username or password.")
            else:
                messagebox.showerror("Error", "User not found.")
            close_connection(connection)
    except Error as e:
        messagebox.showerror("Error", f"Error logging in: {e}")
        close_connection(connection)

# Function to open options window after successful login
def open_options_window():
    global options_window
    options_window = tk.Toplevel(root)
    options_window.title("Options")
    options_window.geometry("300x150")  # Set window size

    play_button = tk.Button(options_window, text="Play", command=play, width=20, height=2)
    play_button.pack(pady=10)

    analysis_button = tk.Button(options_window, text="Analysis", command=analysis, width=20, height=2)
    analysis_button.pack(pady=10)

# Function to start playing chess
def play():
    options_window.destroy()  # Close the options window
    chess_game = chessGUI.ChessGame()
    chess_game.run_game()

# Function to start the chess analysis
def analysis():
    options_window.destroy()  # Close the options window
    app = chessAnalysisPage.ChessBoardApp
    app().run()

# Main tkinter window for user authentication
root = tk.Tk()
root.title("User Authentication")

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Password label and entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Register and login buttons
register_button = tk.Button(root, text="Register", command=register_user)
register_button.grid(row=2, column=0, columnspan=2, pady=10)
login_button = tk.Button(root, text="Login", command=login_user)
login_button.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
