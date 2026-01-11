import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import json
import os
from datetime import datetime
import hashlib
import secrets
import subprocess
import sys

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Secure Password Generator")
        self.root.geometry("800x650")
        self.root.configure(bg='#1e1e2e')
        
        # Variables
        self.password_history = []
        self.saved_passwords = []
        self.history_file = "password_history.json"
        self.saved_file = "saved_passwords.json"
        
        # Load history
        self.load_history()
        self.load_saved_passwords()
        
        # Colors
        self.bg_color = '#1e1e2e'
        self.card_bg = '#2d2d44'
        self.accent_color = '#6c5ce7'
        self.success_color = '#00b894'
        self.warning_color = '#fdcb6e'
        self.danger_color = '#e17055'
        self.text_color = '#dfe6e9'
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_frame = tk.Frame(main_container, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame,
                              text="🔐 SECURE PASSWORD GENERATOR",
                              font=("Arial", 20, "bold"),
                              bg=self.bg_color,
                              fg=self.accent_color)
        title_label.pack()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Generate Password
        tab1 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(tab1, text="Generate Password")
        
        # Tab 2: Password Strength Checker
        tab2 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(tab2, text="Strength Checker")
        
        # Tab 3: Password History
        tab3 = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(tab3, text="History")
        
        # Build each tab
        self.build_generator_tab(tab1)
        self.build_strength_tab(tab2)
        self.build_history_tab(tab3)
        
    def build_generator_tab(self, parent):
        # Settings Frame
        settings_frame = tk.LabelFrame(parent,
                                      text="Password Settings",
                                      font=("Arial", 12, "bold"),
                                      bg=self.card_bg,
                                      fg=self.text_color,
                                      padx=15,
                                      pady=15)
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Password Length
        length_frame = tk.Frame(settings_frame, bg=self.card_bg)
        length_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(length_frame,
                text="Password Length:",
                font=("Arial", 11),
                bg=self.card_bg,
                fg=self.text_color).pack(side=tk.LEFT)
        
        self.length_var = tk.IntVar(value=16)
        self.length_scale = tk.Scale(length_frame,
                                    from_=8,
                                    to=32,
                                    orient=tk.HORIZONTAL,
                                    variable=self.length_var,
                                    bg=self.card_bg,
                                    fg=self.text_color,
                                    highlightbackground=self.card_bg,
                                    length=250)
        self.length_scale.pack(side=tk.LEFT, padx=(20, 0))
        
        self.length_label = tk.Label(length_frame,
                                    textvariable=self.length_var,
                                    font=("Arial", 11, "bold"),
                                    bg=self.accent_color,
                                    fg="white",
                                    width=3,
                                    relief=tk.RAISED)
        self.length_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Character Sets
        charsets_frame = tk.Frame(settings_frame, bg=self.card_bg)
        charsets_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.lower_var = tk.BooleanVar(value=True)
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        tk.Label(charsets_frame,
                text="Include:",
                font=("Arial", 11),
                bg=self.card_bg,
                fg=self.text_color).pack(anchor=tk.W)
        
        check_frame = tk.Frame(charsets_frame, bg=self.card_bg)
        check_frame.pack(fill=tk.X, pady=(5, 0))
        
        charsets = [
            ("Lowercase (a-z)", self.lower_var),
            ("Uppercase (A-Z)", self.upper_var),
            ("Digits (0-9)", self.digits_var),
            ("Symbols (!@#$%)", self.symbols_var)
        ]
        
        for i, (text, var) in enumerate(charsets):
            cb = tk.Checkbutton(check_frame,
                               text=text,
                               variable=var,
                               font=("Arial", 10),
                               bg=self.card_bg,
                               fg=self.text_color,
                               selectcolor=self.accent_color,
                               activebackground=self.card_bg)
            cb.grid(row=0, column=i, sticky=tk.W, padx=(0, 20))
        
        # Generate Button
        button_frame = tk.Frame(settings_frame, bg=self.card_bg)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        generate_btn = tk.Button(button_frame,
                                text="🎲 GENERATE PASSWORD",
                                command=self.generate_password,
                                font=("Arial", 12, "bold"),
                                bg=self.accent_color,
                                fg="white",
                                padx=30,
                                pady=10,
                                cursor="hand2",
                                bd=0)
        generate_btn.pack()
        
        # Generated Password Display
        password_frame = tk.LabelFrame(parent,
                                      text="Generated Password",
                                      font=("Arial", 12, "bold"),
                                      bg=self.card_bg,
                                      fg=self.text_color,
                                      padx=15,
                                      pady=15)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(password_frame,
                                 textvariable=self.password_var,
                                 font=("Courier New", 14, "bold"),
                                 justify=tk.CENTER,
                                 bd=0,
                                 readonlybackground='#3a3a5a',
                                 fg=self.success_color,
                                 state='readonly')
        password_entry.pack(fill=tk.X, ipady=10)
        
        # Action Buttons
        action_frame = tk.Frame(password_frame, bg=self.card_bg)
        action_frame.pack(fill=tk.X, pady=(15, 0))
        
        actions = [
            ("📋 Copy", self.copy_password, self.success_color),
            ("🔄 Regenerate", self.regenerate_password, self.warning_color),
            ("💾 Save", self.save_current_password, self.accent_color)
        ]
        
        for text, command, color in actions:
            btn = tk.Button(action_frame,
                          text=text,
                          command=command,
                          font=("Arial", 10, "bold"),
                          bg=color,
                          fg="white",
                          padx=15,
                          pady=5,
                          cursor="hand2",
                          bd=0)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Password Strength Indicator
        self.strength_frame = tk.Frame(parent, bg=self.bg_color)
        self.strength_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.strength_label = tk.Label(self.strength_frame,
                                      text="Strength: Not Generated",
                                      font=("Arial", 11),
                                      bg=self.bg_color,
                                      fg=self.text_color)
        self.strength_label.pack()
        
        self.strength_bar = tk.Canvas(self.strength_frame,
                                     height=10,
                                     bg=self.bg_color,
                                     highlightthickness=0)
        self.strength_bar.pack(fill=tk.X, pady=(5, 0))
        
    def build_strength_tab(self, parent):
        # Strength Checker Frame
        checker_frame = tk.LabelFrame(parent,
                                     text="Password Strength Analyzer",
                                     font=("Arial", 12, "bold"),
                                     bg=self.card_bg,
                                     fg=self.text_color,
                                     padx=15,
                                     pady=15)
        checker_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Input Password
        input_frame = tk.Frame(checker_frame, bg=self.card_bg)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(input_frame,
                text="Enter Password to Check:",
                font=("Arial", 11),
                bg=self.card_bg,
                fg=self.text_color).pack(anchor=tk.W)
        
        self.check_password_var = tk.StringVar()
        check_entry = tk.Entry(input_frame,
                              textvariable=self.check_password_var,
                              font=("Courier New", 12),
                              show="*",
                              bg='#3a3a5a',
                              fg=self.text_color,
                              insertbackground=self.text_color)
        check_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Check Button
        check_btn = tk.Button(input_frame,
                             text="🔍 CHECK STRENGTH",
                             command=self.analyze_password,
                             font=("Arial", 11, "bold"),
                             bg=self.accent_color,
                             fg="white",
                             padx=20,
                             pady=8,
                             cursor="hand2",
                             bd=0)
        check_btn.pack(pady=(10, 0))
        
        # Results Frame
        results_frame = tk.Frame(checker_frame, bg=self.card_bg)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Strength Score
        score_frame = tk.Frame(results_frame, bg=self.card_bg)
        score_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.score_label = tk.Label(score_frame,
                                   text="Score: 0/100",
                                   font=("Arial", 14, "bold"),
                                   bg=self.card_bg,
                                   fg=self.text_color)
        self.score_label.pack()
        
        self.score_bar = tk.Canvas(score_frame,
                                  height=20,
                                  bg='#3a3a5a',
                                  highlightthickness=0)
        self.score_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Strength Level
        self.level_label = tk.Label(score_frame,
                                   text="",
                                   font=("Arial", 12),
                                   bg=self.card_bg,
                                   fg=self.text_color)
        self.level_label.pack(pady=(5, 0))
        
        # Criteria Checklist
        criteria_frame = tk.LabelFrame(results_frame,
                                      text="Security Criteria",
                                      font=("Arial", 11, "bold"),
                                      bg=self.card_bg,
                                      fg=self.text_color,
                                      padx=10,
                                      pady=10)
        criteria_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.criteria_vars = {}
        criteria = [
            ("Length ≥ 12 characters", False),
            ("Contains lowercase", False),
            ("Contains uppercase", False),
            ("Contains digits", False),
            ("Contains symbols", False)
        ]
        
        for i, (text, _) in enumerate(criteria):
            var = tk.BooleanVar()
            self.criteria_vars[text] = var
            cb = tk.Checkbutton(criteria_frame,
                               text=text,
                               variable=var,
                               state='disabled',
                               font=("Arial", 9),
                               bg=self.card_bg,
                               fg=self.text_color,
                               selectcolor=self.accent_color,
                               disabledforeground=self.text_color)
            cb.grid(row=i, column=0, sticky=tk.W, pady=2)
        
    def build_history_tab(self, parent):
        # History Frame
        history_frame = tk.LabelFrame(parent,
                                     text="Password History",
                                     font=("Arial", 12, "bold"),
                                     bg=self.card_bg,
                                     fg=self.text_color,
                                     padx=15,
                                     pady=15)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text area for history
        self.history_text = scrolledtext.ScrolledText(history_frame,
                                                     height=15,
                                                     font=("Courier New", 10),
                                                     bg='#3a3a5a',
                                                     fg=self.text_color,
                                                     insertbackground=self.text_color)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        self.history_text.config(state=tk.DISABLED)
        
        # Action Buttons for history
        history_btn_frame = tk.Frame(history_frame, bg=self.card_bg)
        history_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        history_buttons = [
            ("🗑️ Clear History", self.clear_history),
            ("📝 Export to File", self.export_history)
        ]
        
        for text, command in history_buttons:
            btn = tk.Button(history_btn_frame,
                          text=text,
                          command=command,
                          font=("Arial", 9),
                          bg=self.accent_color,
                          fg="white",
                          padx=10,
                          pady=5,
                          cursor="hand2",
                          bd=0)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Update history display
        self.update_history_display()
        
    def generate_password(self):
        """Generate a password based on user settings"""
        # Get settings
        length = self.length_var.get()
        
        # Check if at least one character set is selected
        if not any([self.lower_var.get(), self.upper_var.get(), 
                    self.digits_var.get(), self.symbols_var.get()]):
            messagebox.showwarning("Warning", "Please select at least one character set!")
            return
        
        # Build character pool
        char_pool = ""
        if self.lower_var.get():
            char_pool += string.ascii_lowercase
        if self.upper_var.get():
            char_pool += string.ascii_uppercase
        if self.digits_var.get():
            char_pool += string.digits
        if self.symbols_var.get():
            char_pool += "!@#$%^&*"
        
        if not char_pool:
            messagebox.showerror("Error", "No characters available!")
            return
        
        # Generate password using cryptographically secure random
        try:
            password = ''.join(secrets.choice(char_pool) for _ in range(length))
        except:
            # Fallback to random if secrets fails
            password = ''.join(random.choice(char_pool) for _ in range(length))
        
        # Ensure at least one character from each selected set
        if self.lower_var.get() and not any(c.islower() for c in password):
            password = self.force_character(password, string.ascii_lowercase)
        if self.upper_var.get() and not any(c.isupper() for c in password):
            password = self.force_character(password, string.ascii_uppercase)
        if self.digits_var.get() and not any(c.isdigit() for c in password):
            password = self.force_character(password, string.digits)
        if self.symbols_var.get() and not any(c in "!@#$%^&*" for c in password):
            password = self.force_character(password, "!@#$%^&*")
        
        # Set password
        self.password_var.set(password)
        
        # Add to history
        self.add_to_history(password)
        
        # Update strength display
        self.update_strength_display(password)
        
    def force_character(self, password, char_set):
        """Ensure at least one character from char_set is in password"""
        pos = random.randint(0, len(password)-1)
        new_char = random.choice(char_set)
        return password[:pos] + new_char + password[pos+1:]
    
    def update_strength_display(self, password):
        """Update the strength indicator"""
        strength = self.calculate_strength(password)
        
        # Update label
        colors = {
            "Very Weak": self.danger_color,
            "Weak": "#e17055",
            "Moderate": self.warning_color,
            "Strong": "#00cec9",
            "Very Strong": self.success_color
        }
        
        self.strength_label.config(
            text=f"Strength: {strength['level']}",
            fg=colors.get(strength['level'], self.text_color)
        )
        
        # Update progress bar
        self.strength_bar.delete("all")
        width = 300
        fill_width = int(width * (strength['score'] / 100))
        
        self.strength_bar.create_rectangle(0, 0, width, 10, fill='#3a3a5a', outline='')
        self.strength_bar.create_rectangle(0, 0, fill_width, 10, 
                                         fill=colors.get(strength['level'], self.accent_color), 
                                         outline='')
    
    def calculate_strength(self, password):
        """Calculate password strength score"""
        score = 0
        
        # Length score (up to 40 points)
        length = len(password)
        score += min(length * 2, 40)
        
        # Character variety scores
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*" for c in password)
        
        if has_lower:
            score += 10
        if has_upper:
            score += 15
        if has_digit:
            score += 15
        if has_symbol:
            score += 20
        
        # Deduct for common patterns
        common_patterns = ['123', 'abc', 'password', 'qwerty', 'admin']
        for pattern in common_patterns:
            if pattern in password.lower():
                score -= 20
        
        # Ensure score is within bounds
        score = max(0, min(score, 100))
        
        # Determine level
        if score < 30:
            level = "Very Weak"
        elif score < 50:
            level = "Weak"
        elif score < 70:
            level = "Moderate"
        elif score < 85:
            level = "Strong"
        else:
            level = "Very Strong"
        
        return {'score': score, 'level': level}
    
    def add_to_history(self, password):
        """Add password to history"""
        entry = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'password': password,
            'length': len(password),
            'strength': self.calculate_strength(password)['level']
        }
        
        self.password_history.insert(0, entry)
        
        # Keep only last 20 entries
        if len(self.password_history) > 20:
            self.password_history = self.password_history[:20]
        
        # Update history display
        self.update_history_display()
        
        # Save history
        self.save_history()
    
    def update_history_display(self):
        """Update the history text area"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        if not self.password_history:
            self.history_text.insert(tk.END, "No password history yet.")
        else:
            for entry in self.password_history:
                self.history_text.insert(tk.END, 
                    f"Date: {entry['date']}\n"
                    f"Password: {entry['password']}\n"
                    f"Length: {entry['length']} | Strength: {entry['strength']}\n"
                    f"{'-'*40}\n")
        
        self.history_text.config(state=tk.DISABLED)
    
    def copy_password(self):
        """Copy password to clipboard using platform-specific methods"""
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password to copy!")
            return
        
        try:
            # Try different methods to copy to clipboard
            self.copy_to_clipboard(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        except Exception as e:
            # Show password for manual copying
            messagebox.showinfo("Copy Password", 
                              f"Password: {password}\n\n"
                              f"Select and copy the password above.")
    
    def copy_to_clipboard(self, text):
        """Platform-specific clipboard copy"""
        # For Windows
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.user32.OpenClipboard(0)
            ctypes.windll.user32.EmptyClipboard()
            ctypes.windll.user32.SetClipboardData(1, text)
            ctypes.windll.user32.CloseClipboard()
        # For macOS
        elif sys.platform == 'darwin':
            subprocess.run(['pbcopy'], input=text.encode())
        # For Linux
        else:
            subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode())
    
    def regenerate_password(self):
        """Regenerate password with same settings"""
        self.generate_password()
    
    def save_current_password(self):
        """Save current password"""
        password = self.password_var.get()
        if not password:
            messagebox.showwarning("Warning", "No password to save!")
            return
        
        # Simple save dialog
        label = f"Password_{len(self.saved_passwords)+1}"
        
        self.saved_passwords.append({
            'label': label,
            'password': self.simple_encrypt(password),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
        self.save_saved_passwords()
        messagebox.showinfo("Success", f"Password saved as '{label}'")
    
    def simple_encrypt(self, text):
        """Simple encryption for demo purposes"""
        return hashlib.sha256(text.encode()).hexdigest()[:20]
    
    def analyze_password(self):
        """Analyze password strength"""
        password = self.check_password_var.get()
        
        if not password:
            messagebox.showwarning("Warning", "Please enter a password to analyze!")
            return
        
        # Calculate strength
        strength = self.calculate_strength(password)
        
        # Update score display
        self.score_label.config(text=f"Score: {strength['score']}/100")
        
        # Update progress bar
        self.score_bar.delete("all")
        width = 300
        fill_width = int(width * (strength['score'] / 100))
        
        colors = {
            "Very Weak": self.danger_color,
            "Weak": "#e17055",
            "Moderate": self.warning_color,
            "Strong": "#00cec9",
            "Very Strong": self.success_color
        }
        
        self.score_bar.create_rectangle(0, 0, width, 20, fill='#3a3a5a', outline='')
        self.score_bar.create_rectangle(0, 0, fill_width, 20, 
                                       fill=colors.get(strength['level'], self.accent_color), 
                                       outline='')
        
        # Update level
        self.level_label.config(
            text=f"Strength Level: {strength['level']}",
            fg=colors.get(strength['level'], self.text_color)
        )
        
        # Update criteria checklist
        criteria = [
            ("Length ≥ 12 characters", len(password) >= 12),
            ("Contains lowercase", any(c.islower() for c in password)),
            ("Contains uppercase", any(c.isupper() for c in password)),
            ("Contains digits", any(c.isdigit() for c in password)),
            ("Contains symbols", any(c in "!@#$%^&*" for c in password))
        ]
        
        for (text, result), var in zip(criteria, self.criteria_vars.values()):
            var.set(result)
    
    def clear_history(self):
        """Clear password history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            self.password_history = []
            self.update_history_display()
            self.save_history()
    
    def export_history(self):
        """Export history to file"""
        try:
            with open("password_export.txt", "w") as f:
                f.write("Password History Export\n")
                f.write("=" * 50 + "\n\n")
                for entry in self.password_history:
                    f.write(f"Date: {entry['date']}\n")
                    f.write(f"Password: {entry['password']}\n")
                    f.write(f"Length: {entry['length']}\n")
                    f.write(f"Strength: {entry['strength']}\n")
                    f.write("-" * 30 + "\n")
            
            messagebox.showinfo("Success", "History exported to 'password_export.txt'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def save_history(self):
        """Save history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.password_history, f, indent=2)
        except:
            pass
    
    def load_history(self):
        """Load history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.password_history = json.load(f)
            except:
                self.password_history = []
    
    def save_saved_passwords(self):
        """Save passwords to file"""
        try:
            with open(self.saved_file, 'w') as f:
                json.dump(self.saved_passwords, f, indent=2)
        except:
            pass
    
    def load_saved_passwords(self):
        """Load saved passwords from file"""
        if os.path.exists(self.saved_file):
            try:
                with open(self.saved_file, 'r') as f:
                    self.saved_passwords = json.load(f)
            except:
                self.saved_passwords = []

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()