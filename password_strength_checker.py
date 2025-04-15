import tkinter as tk
from tkinter import ttk
import re

class PasswordStrengthChecker:
    def __init__(self, root):
        """Initialize the Password Strength Checker application"""
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(padx=20, pady=20)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Title
        title_label = ttk.Label(
            self.root, 
            text="Password Strength Checker", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Password entry frame
        input_frame = ttk.LabelFrame(self.root, text="Enter Password")
        input_frame.pack(fill="x", padx=5, pady=5)
        
        # Password entry
        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self.check_password_strength)
        
        self.password_entry = ttk.Entry(
            input_frame, 
            textvariable=self.password_var,
            show="•", 
            width=30, 
            font=("Arial", 12)
        )
        self.password_entry.pack(padx=10, pady=10, fill="x")
        
        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        self.show_password_var.trace_add("write", self.toggle_password_visibility)
        
        show_password_check = ttk.Checkbutton(
            input_frame,
            text="Show Password",
            variable=self.show_password_var
        )
        show_password_check.pack(padx=10, pady=(0, 10), anchor="w")
        
        # Strength meter frame
        meter_frame = ttk.LabelFrame(self.root, text="Password Strength")
        meter_frame.pack(fill="x", padx=5, pady=10)
        
        # Strength progress bar
        self.strength_var = tk.DoubleVar()
        self.strength_bar = ttk.Progressbar(
            meter_frame,
            orient="horizontal",
            length=400,
            mode="determinate",
            variable=self.strength_var
        )
        self.strength_bar.pack(padx=10, pady=10, fill="x")
        
        # Strength label
        self.strength_label = ttk.Label(
            meter_frame,
            text="Password Strength: None",
            font=("Arial", 10, "bold")
        )
        self.strength_label.pack(padx=10, pady=(0, 10), anchor="w")
        
        # Criteria frame
        criteria_frame = ttk.LabelFrame(self.root, text="Password Criteria")
        criteria_frame.pack(fill="x", padx=5, pady=5)
        
        # Create criteria labels with checkmarks
        self.criteria_labels = {}
        criteria = [
            "length", "lowercase", "uppercase", "numbers", "special"
        ]
        
        for criterion in criteria:
            var = tk.StringVar(value="✕")
            label = ttk.Label(
                criteria_frame,
                text=f"{criterion.capitalize()}: ",
                font=("Arial", 10)
            )
            label.grid(row=criteria.index(criterion), column=0, sticky="w", padx=5, pady=2)
            
            check_label = ttk.Label(
                criteria_frame,
                textvariable=var,
                font=("Arial", 10, "bold")
            )
            check_label.grid(row=criteria.index(criterion), column=1, sticky="w", padx=5, pady=2)
            
            # Add description
            desc_text = self.get_criterion_description(criterion)
            desc_label = ttk.Label(
                criteria_frame,
                text=desc_text,
                font=("Arial", 9)
            )
            desc_label.grid(row=criteria.index(criterion), column=2, sticky="w", padx=5, pady=2)
            
            self.criteria_labels[criterion] = var
        
        # Set equal width for all columns
        for i in range(3):
            criteria_frame.columnconfigure(i, weight=1)
        
    def get_criterion_description(self, criterion):
        """Return the description for each criterion"""
        descriptions = {
            "length": "At least 12 characters (14+ recommended)",
            "lowercase": "At least one lowercase letter (a-z)",
            "uppercase": "At least one uppercase letter (A-Z)",
            "numbers": "At least one number (0-9)",
            "special": "At least one special character (!@#$%^&*)"
        }
        return descriptions.get(criterion, "")
        
    def toggle_password_visibility(self, *args):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def check_password_strength(self, *args):
        """Assess password strength based on multiple criteria"""
        password = self.password_var.get()
        
        # Reset criteria
        for key in self.criteria_labels:
            self.criteria_labels[key].set("✕")
        
        # If password is empty, reset everything
        if not password:
            self.strength_var.set(0)
            self.strength_label.config(text="Password Strength: None")
            self.update_strength_color(0)
            return
        
        # Check criteria
        score = 0
        max_score = 5
        criteria_met = 0
        
        # Check length (minimum 12 characters)
        if len(password) >= 12:
            score += 1
            criteria_met += 1
            self.criteria_labels["length"].set("✓")
            
            # Bonus for extra length (14+ characters recommended)
            if len(password) >= 14:
                score += 0.5  # Bonus points for longer passwords
                max_score += 0.5
        
        # Check for lowercase letters
        if re.search(r"[a-z]", password):
            score += 1
            criteria_met += 1
            self.criteria_labels["lowercase"].set("✓")
        
        # Check for uppercase letters
        if re.search(r"[A-Z]", password):
            score += 1
            criteria_met += 1
            self.criteria_labels["uppercase"].set("✓")
        
        # Check for numbers
        if re.search(r"\d", password):
            score += 1
            criteria_met += 1
            self.criteria_labels["numbers"].set("✓")
        
        # Check for special characters
        if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
            score += 1
            criteria_met += 1
            self.criteria_labels["special"].set("✓")
        
        # Calculate percentage
        percentage = (score / max_score) * 100
        # Cap at 100% for UI consistency
        if percentage > 100:
            percentage = 100
            
        self.strength_var.set(percentage)
        
        # Update strength label
        strength_text = self.get_strength_text(percentage, criteria_met)
        self.strength_label.config(text=f"Password Strength: {strength_text}")
        
        # Update progress bar color
        self.update_strength_color(percentage, criteria_met)
    
    def get_strength_text(self, percentage, criteria_met=0):
        """Return text based on password strength percentage and criteria met"""
        if percentage == 0:
            return "None"
        
        # For a password to be "Very Strong", it must meet all criteria
        if criteria_met == 5 and percentage >= 80:
            return "Very Strong"
        
        # If missing any criteria, cap at appropriate level
        if criteria_met < 5 and percentage > 80:
            return "Strong"  # Cap at Strong if missing criteria
            
        # Regular strength categories
        if percentage <= 20:
            return "Very Weak"
        elif percentage <= 40:
            return "Weak"
        elif percentage <= 60:
            return "Moderate"
        elif percentage <= 80:
            return "Strong"
        else:
            return "Very Strong"
    
    def update_strength_color(self, percentage, criteria_met=0):
        """Update the progress bar color based on strength and criteria met"""
        # Special color for 100% criteria met with high score
        if criteria_met == 5 and percentage >= 90:
            color = "#00cc00"  # Bright green
        # Standard color scheme based on percentage
        elif percentage == 0:
            color = "grey"
        elif percentage <= 20:
            color = "#ff0000"  # Red
        elif percentage <= 40:
            color = "#ff7700"  # Orange
        elif percentage <= 60:
            color = "#ffff00"  # Yellow
        elif percentage <= 80:
            color = "#aaff00"  # Light green
        else:
            color = "#00ff00"  # Green
            
        # Apply the style
        style = ttk.Style()
        style.configure("TProgressbar", background=color)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()

if __name__ == "__main__":
    main()