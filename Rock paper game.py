import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os
from datetime import datetime

class RockPaperScissorsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Rock Paper Scissors Game")
        self.root.geometry("800x700")
        self.root.configure(bg='#121212')
        
        # Game variables
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.round = 1
        self.game_history = []
        self.high_score_file = "rps_high_scores.json"
        
        # Load high scores
        self.load_high_scores()
        
        # Colors
        self.bg_color = '#121212'
        self.card_bg = '#1e1e1e'
        self.accent_color = '#6c5ce7'
        self.success_color = '#00b894'
        self.danger_color = '#e17055'
        self.warning_color = '#fdcb6e'
        self.text_color = '#dfe6e9'
        
        # Game choices with emojis
        self.choices = {
            'rock': '🪨 Rock',
            'paper': '📄 Paper', 
            'scissors': '✂️ Scissors'
        }
        
        # Win rules
        self.win_rules = {
            'rock': 'scissors',
            'scissors': 'paper',
            'paper': 'rock'
        }
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_frame = tk.Frame(main_container, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame,
                              text="🎮 ROCK PAPER SCISSORS",
                              font=("Impact", 28),
                              bg=self.bg_color,
                              fg=self.accent_color)
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                 text="Choose your weapon and beat the computer!",
                                 font=("Arial", 12),
                                 bg=self.bg_color,
                                 fg=self.text_color)
        subtitle_label.pack(pady=(5, 0))
        
        # Stats Frame
        stats_frame = tk.Frame(main_container, bg=self.card_bg, relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats = [
            (f"Round: {self.round}", "🔄"),
            (f"Player: {self.user_score}", "👤"),
            (f"Computer: {self.computer_score}", "💻"),
            (f"Ties: {self.ties}", "🤝")
        ]
        
        for i, (text, icon) in enumerate(stats):
            stat_label = tk.Label(stats_frame,
                                 text=f"{icon} {text}",
                                 font=("Arial", 12, "bold"),
                                 bg=self.card_bg,
                                 fg=self.text_color,
                                 padx=20,
                                 pady=10)
            stat_label.grid(row=0, column=i, padx=10, pady=5)
        
        # Instructions
        instructions_frame = tk.LabelFrame(main_container,
                                          text="🎯 How to Play",
                                          font=("Arial", 11, "bold"),
                                          bg=self.card_bg,
                                          fg=self.text_color,
                                          padx=15,
                                          pady=10)
        instructions_frame.pack(fill=tk.X, pady=(0, 20))
        
        rules_text = "🪨 Rock beats ✂️ Scissors | ✂️ Scissors beats 📄 Paper | 📄 Paper beats 🪨 Rock"
        tk.Label(instructions_frame,
                text=rules_text,
                font=("Arial", 10),
                bg=self.card_bg,
                fg=self.text_color).pack()
        
        # Player Choices Frame
        choices_frame = tk.LabelFrame(main_container,
                                     text="⚔️ Choose Your Weapon",
                                     font=("Arial", 14, "bold"),
                                     bg=self.card_bg,
                                     fg=self.text_color,
                                     padx=20,
                                     pady=20)
        choices_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create choice buttons
        self.choice_buttons = {}
        buttons_frame = tk.Frame(choices_frame, bg=self.card_bg)
        buttons_frame.pack()
        
        for i, (choice_key, choice_text) in enumerate(self.choices.items()):
            btn = tk.Button(buttons_frame,
                          text=choice_text,
                          command=lambda c=choice_key: self.play_round(c),
                          font=("Arial", 14, "bold"),
                          bg=self.accent_color,
                          fg="white",
                          padx=30,
                          pady=15,
                          cursor="hand2",
                          bd=0,
                          relief=tk.RAISED)
            btn.grid(row=0, column=i, padx=15)
            self.choice_buttons[choice_key] = btn
        
        # Game Result Display
        result_frame = tk.LabelFrame(main_container,
                                    text="🎮 Game Result",
                                    font=("Arial", 14, "bold"),
                                    bg=self.card_bg,
                                    fg=self.text_color,
                                    padx=20,
                                    pady=20)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Result display area
        self.result_text = tk.StringVar()
        self.result_text.set("Make your choice to start the game!")
        
        result_label = tk.Label(result_frame,
                               textvariable=self.result_text,
                               font=("Arial", 12),
                               bg=self.card_bg,
                               fg=self.text_color,
                               wraplength=500,
                               justify=tk.CENTER)
        result_label.pack(expand=True)
        
        # Choices display
        choices_display_frame = tk.Frame(result_frame, bg=self.card_bg)
        choices_display_frame.pack(pady=(20, 0))
        
        # Player choice display
        self.player_choice_var = tk.StringVar(value="❓")
        player_choice_label = tk.Label(choices_display_frame,
                                      textvariable=self.player_choice_var,
                                      font=("Arial", 40),
                                      bg=self.card_bg,
                                      fg=self.success_color)
        player_choice_label.grid(row=0, column=0, padx=30)
        
        tk.Label(choices_display_frame,
                text="VS",
                font=("Arial", 20, "bold"),
                bg=self.card_bg,
                fg=self.text_color).grid(row=0, column=1, padx=20)
        
        # Computer choice display
        self.computer_choice_var = tk.StringVar(value="❓")
        computer_choice_label = tk.Label(choices_display_frame,
                                        textvariable=self.computer_choice_var,
                                        font=("Arial", 40),
                                        bg=self.card_bg,
                                        fg=self.danger_color)
        computer_choice_label.grid(row=0, column=2, padx=30)
        
        # Labels
        tk.Label(choices_display_frame,
                text="PLAYER",
                font=("Arial", 10, "bold"),
                bg=self.card_bg,
                fg=self.success_color).grid(row=1, column=0)
        
        tk.Label(choices_display_frame,
                text="COMPUTER",
                font=("Arial", 10, "bold"),
                bg=self.card_bg,
                fg=self.danger_color).grid(row=1, column=2)
        
        # Action Buttons Frame
        action_frame = tk.Frame(main_container, bg=self.bg_color)
        action_frame.pack(fill=tk.X)
        
        action_buttons = [
            ("🔄 Play Again", self.reset_round, self.accent_color),
            ("📊 Show History", self.show_history, "#0984e3"),
            ("🏆 High Scores", self.show_high_scores, self.warning_color),
            ("❌ Quit Game", self.quit_game, self.danger_color)
        ]
        
        for i, (text, command, color) in enumerate(action_buttons):
            btn = tk.Button(action_frame,
                          text=text,
                          command=command,
                          font=("Arial", 10, "bold"),
                          bg=color,
                          fg="white",
                          padx=15,
                          pady=8,
                          cursor="hand2",
                          bd=0)
            btn.grid(row=0, column=i, padx=5, pady=5)
    
    def play_round(self, player_choice):
        """Play a round of Rock Paper Scissors"""
        # Get computer choice
        computer_choice = random.choice(list(self.choices.keys()))
        
        # Update displays
        self.player_choice_var.set(self.get_choice_emoji(player_choice))
        self.computer_choice_var.set(self.get_choice_emoji(computer_choice))
        
        # Determine winner
        result = self.determine_winner(player_choice, computer_choice)
        
        # Update scores
        if result == "win":
            self.user_score += 1
            result_text = f"🎉 YOU WIN! {self.choices[player_choice]} beats {self.choices[computer_choice]}"
            color = self.success_color
        elif result == "lose":
            self.computer_score += 1
            result_text = f"😔 YOU LOSE! {self.choices[computer_choice]} beats {self.choices[player_choice]}"
            color = self.danger_color
        else:
            self.ties += 1
            result_text = f"🤝 IT'S A TIE! Both chose {self.choices[player_choice]}"
            color = self.warning_color
        
        # Update result display
        self.result_text.set(f"Round {self.round}\n\n{result_text}")
        
        # Update stats
        self.update_stats_display()
        
        # Add to history
        self.game_history.append({
            'round': self.round,
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'result': result,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        })
        
        # Update round counter
        self.round += 1
        
        # Check for win streak
        if self.user_score >= 5:
            self.check_high_score()
            messagebox.showinfo("🏆 Champion!", "You've reached 5 wins! You're a Rock Paper Scissors Champion!")
    
    def get_choice_emoji(self, choice):
        """Get emoji for choice"""
        emojis = {
            'rock': '🪨',
            'paper': '📄',
            'scissors': '✂️'
        }
        return emojis.get(choice, '❓')
    
    def determine_winner(self, player_choice, computer_choice):
        """Determine the winner of a round"""
        if player_choice == computer_choice:
            return "tie"
        elif self.win_rules[player_choice] == computer_choice:
            return "win"
        else:
            return "lose"
    
    def update_stats_display(self):
        """Update the statistics display"""
        # This method would update the stats frame if we had dynamic updates
        pass
    
    def reset_round(self):
        """Reset the current round display"""
        self.player_choice_var.set("❓")
        self.computer_choice_var.set("❓")
        self.result_text.set("Make your choice to start the game!")
    
    def reset_game(self):
        """Reset the entire game"""
        self.user_score = 0
        self.computer_score = 0
        self.ties = 0
        self.round = 1
        self.game_history = []
        self.reset_round()
        self.update_stats_display()
        messagebox.showinfo("Game Reset", "Game has been reset to start!")
    
    def show_history(self):
        """Show game history"""
        if not self.game_history:
            messagebox.showinfo("Game History", "No games played yet!")
            return
        
        # Create history window
        history_window = tk.Toplevel(self.root)
        history_window.title("📜 Game History")
        history_window.geometry("500x400")
        history_window.configure(bg=self.card_bg)
        
        # Create text widget
        text_widget = tk.Text(history_window, 
                             font=("Courier New", 10),
                             bg='#2d2d2d',
                             fg=self.text_color,
                             padx=10,
                             pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Add history
        text_widget.insert(tk.END, "📜 GAME HISTORY\n")
        text_widget.insert(tk.END, "="*50 + "\n\n")
        
        for game in reversed(self.game_history[-20:]):  # Show last 20 games
            result_emoji = "✅" if game['result'] == 'win' else "❌" if game['result'] == 'lose' else "⚖️"
            text_widget.insert(tk.END, 
                f"Round {game['round']} ({game['timestamp']})\n"
                f"Player: {self.choices[game['player_choice']]} {result_emoji} Computer: {self.choices[game['computer_choice']]}\n"
                f"Result: {game['result'].upper()}\n"
                f"{'-'*40}\n"
            )
        
        text_widget.config(state=tk.DISABLED)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(history_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)
    
    def show_high_scores(self):
        """Show high scores"""
        if not self.high_scores:
            messagebox.showinfo("High Scores", "No high scores yet!")
            return
        
        # Create high scores window
        scores_window = tk.Toplevel(self.root)
        scores_window.title("🏆 High Scores")
        scores_window.geometry("400x300")
        scores_window.configure(bg=self.card_bg)
        
        # Create treeview
        tree = ttk.Treeview(scores_window, columns=("Rank", "Score", "Date"), show="headings")
        
        # Define headings
        tree.heading("Rank", text="Rank")
        tree.heading("Score", text="Score")
        tree.heading("Date", text="Date")
        
        # Define columns
        tree.column("Rank", width=80, anchor=tk.CENTER)
        tree.column("Score", width=100, anchor=tk.CENTER)
        tree.column("Date", width=150, anchor=tk.CENTER)
        
        # Add scores
        for i, score in enumerate(sorted(self.high_scores, key=lambda x: x['score'], reverse=True)[:10], 1):
            tree.insert("", tk.END, values=(i, score['score'], score['date']))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def check_high_score(self):
        """Check if current score is a high score"""
        if self.user_score > 0:
            # Ask if user wants to save high score
            if messagebox.askyesno("🏆 High Score!", 
                                 f"You scored {self.user_score} points!\n"
                                 f"Do you want to save this as a high score?"):
                name = tk.simpledialog.askstring("High Score", "Enter your name:")
                if name:
                    self.high_scores.append({
                        'name': name,
                        'score': self.user_score,
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    self.save_high_scores()
    
    def load_high_scores(self):
        """Load high scores from file"""
        if os.path.exists(self.high_score_file):
            try:
                with open(self.high_score_file, 'r') as f:
                    self.high_scores = json.load(f)
            except:
                self.high_scores = []
        else:
            self.high_scores = []
    
    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open(self.high_score_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except:
            pass
    
    def quit_game(self):
        """Quit the game with confirmation"""
        if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
            self.save_high_scores()
            self.root.destroy()

def main():
    """Main function to run the game"""
    root = tk.Tk()
    game = RockPaperScissorsGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()