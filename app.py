# app.py

# This application now uses the 'ttkthemes' library for modern aesthetics.
# Install it using: pip install ttkthemes

from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import ttk

# Import DataManager
from data_manager import DataManager

# Import all your page classes (ensure these files exist)
from home_page import HomePage
from learn_page import LearnPage
from behavioral_activation_page import BehavioralActivationPage
from thought_record_page import ThoughtRecordPage
from problem_solving_page import ProblemSolvingPage
from progress_page import ProgressPage
from relaxation_page import RelaxationPage

class CBTApp(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.withdraw() # <--- ADDED: Hides the window during setup for a cleaner start

        # --- MODERN AESTHETICS WITH ttkthemes ---
        # <--- ADDED: Set your desired modern theme here.
        # Experiment with themes like: "flatly", "adapta", "arc", "materia", "united", "yaru", "radiance"
        self.set_theme("adapta") # This is a good starting point for a clean, modern look.

        self.title("MindSync: Your CBT Companion") # <--- MODIFIED: Slightly updated title
        self.geometry("1200x800")
        self.minsize(900, 600) # Set a minimum size for the window

        # Initialize the centralized DataManager
        self.data_manager = DataManager()

        # Configure the main window's grid layout
        self.grid_rowconfigure(0, weight=1) # The content area (container) will expand
        self.grid_columnconfigure(0, weight=0) # Sidebar column (fixed width)
        self.grid_columnconfigure(1, weight=1) # Content area (will expand)

        # --- Sidebar for Navigation ---
        # The 'relief="raised"' might sometimes conflict visually with modern themes.
        # Consider changing to "flat" or removing it if it doesn't look right.
        sidebar_frame = ttk.Frame(self, width=200, relief="raised", padding="10")
        sidebar_frame.grid(row=0, column=0, sticky="nswe")
        sidebar_frame.grid_propagate(False) # Prevent sidebar from resizing to content

        # Sidebar Title
        # <--- MODIFIED: Font explicitly set for consistency with modern themes.
        ttk.Label(sidebar_frame, text="CBT Tools", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Navigation Buttons
        # <--- REMOVED: button_font variable is no longer needed as global styles are set.
        # button_font = ("Helvetica", 10, "bold")
        ttk.Button(sidebar_frame, text="Home", command=lambda: self.show_frame("HomePage"), width=20).pack(pady=5)
        ttk.Button(sidebar_frame, text="Learn CBT", command=lambda: self.show_frame("LearnPage"), width=20).pack(pady=5)
        ttk.Button(sidebar_frame, text="Thought Record", command=lambda: self.show_frame("ThoughtRecordPage"), width=20).pack(pady=5)
        ttk.Button(sidebar_frame, text="Behavioral Activation", command=lambda: self.show_frame("BehavioralActivationPage"), width=20).pack(pady=5)
        ttk.Button(sidebar_frame, text="Problem Solving", command=lambda: self.show_frame("ProblemSolvingPage"), width=20).pack(pady=5)
        ttk.Button(sidebar_frame, text="Relaxation", command=lambda: self.show_frame("RelaxationPage"), width=20).pack(pady=5)
        ttk.Button(sidebar_frame, text="Progress", command=lambda: self.show_frame("ProgressPage"), width=20).pack(pady=5)


        # --- Main Content Area (Container for Pages) ---
        # <--- MODIFIED: Changed relief to "flat" for better integration with modern themes.
        container = ttk.Frame(self, relief="flat")
        container.grid(row=0, column=1, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {} # Dictionary to hold all page instances

        # List of page classes to instantiate
        # Pass the DataManager instance to pages that need it
        for Page in (HomePage, LearnPage, BehavioralActivationPage, ThoughtRecordPage, ProblemSolvingPage, ProgressPage, RelaxationPage):
            page_name = Page.__name__
            if page_name in ["BehavioralActivationPage", "ThoughtRecordPage", "ProblemSolvingPage", "ProgressPage"]:
                frame = Page(container, self, self.data_manager) # Pass data_manager
            else:
                frame = Page(container, self) # Pages like HomePage, LearnPage, RelaxationPage don't need data_manager directly
            
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") # Stack all pages in the same grid cell

        self.show_frame("HomePage") # Show the home page initially

        # --- Styling (Optional but Recommended) ---
        # <--- REMOVED: This block is now handled by ttkthemes and the global configure below.
        # self.style = ttk.Style(self)
        # self.style.theme_use("clam") # Or 'default', 'alt', 'vista', 'xpnative'
        # Customize some styles if needed
        # self.style.configure("TLabel", font=("Helvetica", 10))
        # self.style.configure("TButton", font=("Helvetica", 10, "bold"))
        # self.style.configure("TEntry", font=("Helvetica", 10))
        # self.style.configure("TText", font=("Helvetica", 10))

        # <--- ADDED: Global font configuration for all ttk widgets after theme is set.
        # "Segoe UI" is a good modern font for Windows, "Helvetica" for macOS/Linux.
        # Adjust size as needed.
        ttk.Style().configure(".", font=("Segoe UI", 10)) # Sets default font for all ttk widgets
        ttk.Style().configure("TButton", font=("Segoe UI", 10, "bold")) # Explicitly keep buttons bold
        # You might add specific styles for TEntry, TText if they aren't looking right by default:
        # ttk.Style().configure("TEntry", font=("Segoe UI", 10))
        # ttk.Style().configure("TText", font=("Segoe UI", 10)) # Note: tk.Text is not a ttk widget.

        self.deiconify() # <--- ADDED: Shows the main window after setup is complete


    def show_frame(self, page_name, **kwargs):
        """
        Raises the specified page frame to the top, making it visible.
        Accepts kwargs to pass data to the page (e.g., for editing a record).
        """
        frame = self.frames[page_name]

        # If kwargs are provided, it usually means we're loading specific data (e.g., for editing).
        # In this case, we call the page's 'load_data' method if it exists.
        if kwargs and hasattr(frame, 'load_data'):
            frame.load_data(**kwargs)
        # Otherwise, if no specific data is provided, or if 'load_data' isn't implemented,
        # we call a general refresh method to ensure the page's default display is up-to-date.
        # This is useful for pages like ProgressPage when simply navigating to them.
        elif hasattr(frame, 'refresh_page'): # Used in ProgressPage
            frame.refresh_page()
        elif hasattr(frame, 'refresh_data_display'): # Older or other pages might use this name
            frame.refresh_data_display()
            
        frame.tkraise()

        # Handle specific page cleanup/state when navigating away from it
        if page_name != "RelaxationPage" and "RelaxationPage" in self.frames:
            if hasattr(self.frames["RelaxationPage"], 'is_breathing_active') and self.frames["RelaxationPage"].is_breathing_active:
                self.frames["RelaxationPage"]._stop_breathing_exercise()


if __name__ == "__main__":
    app = CBTApp()
    app.mainloop()