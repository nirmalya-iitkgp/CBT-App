# home_page.py

import tkinter as tk
from tkinter import ttk

class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure grid for the HomePage frame
        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=1) # Content area
        self.grid_columnconfigure(0, weight=1)

        # Welcome Title
        ttk.Label(self, text="Welcome to Your CBT Companion", font=("Helvetica", 18, "bold")).grid(row=0, column=0, pady=20, sticky="ew")

        # Main Content Frame
        content_frame = ttk.Frame(self, padding="30")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=0)
        content_frame.grid_rowconfigure(2, weight=0)

        # Introductory Text
        intro_text = """
        This application is designed to help you practice Cognitive Behavioral Therapy (CBT) techniques.
        CBT is a powerful approach to managing mental health challenges by focusing on the connections
        between your thoughts, emotions, and behaviors.

        Use the navigation on the left (or top, depending on main app layout) to explore different tools:

        •   Learn: Understand core CBT principles and concepts through lessons and quizzes.
        •   Thought Record: Challenge unhelpful thought patterns and reframe them.
        •   Behavioral Activation: Plan and log activities to boost pleasure and mastery.
        •   Problem Solving: Break down problems and develop effective solutions.
        •   Progress: Visualize your journey and see your improvements over time.

        Start by exploring the 'Learn' section or jump straight into a tool!
        """
        ttk.Label(content_frame, text=intro_text, wraplength=700, justify="left", font=("Helvetica", 11)).grid(row=0, column=0, pady=10, sticky="ew")

        # Call to action / Quick start buttons (optional)
        ttk.Label(content_frame, text="Quick Start:", font=("Helvetica", 12, "bold")).grid(row=1, column=0, pady=(20, 10), sticky="w")
        
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=2, column=0, pady=10, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        ttk.Button(button_frame, text="Start Learning", command=lambda: controller.show_frame("LearnPage")).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Log a Thought", command=lambda: controller.show_frame("ThoughtRecordPage")).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ttk.Button(button_frame, text="Plan an Activity", command=lambda: controller.show_frame("BehavioralActivationPage")).grid(row=0, column=2, padx=10, pady=5, sticky="ew")