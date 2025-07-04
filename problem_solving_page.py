# problem_solving_page.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import DateEntry
import datetime
import json # Still needed for potential data structure handling
import os # Still needed for path joining
from data_manager import DataManager # Import the centralized DataManager

class ProblemSolvingPage(ttk.Frame):
    def __init__(self, parent, controller, data_manager): # Accept data_manager instance
        super().__init__(parent)
        self.controller = controller
        self.data_manager = data_manager # Store the passed DataManager instance

        # Dictionary to store the data as it's being filled across steps
        self.current_record_data = {}
        self.record_timestamp = None # To store timestamp if editing an existing record

        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=1) # Notebook/content area
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Problem-Solving Process", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        # Create a notebook for steps
        self.steps_notebook = ttk.Notebook(self)
        self.steps_notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Step 1: Define the Problem ---
        self.step1_frame = ttk.Frame(self.steps_notebook, padding="20")
        self.steps_notebook.add(self.step1_frame, text="Step 1: Define Problem")
        self._setup_step1()

        # --- Step 2: Brainstorm & Choose Solution ---
        self.step2_frame = ttk.Frame(self.steps_notebook, padding="20")
        self.steps_notebook.add(self.step2_frame, text="Step 2: Solutions")
        self._setup_step2()

        # --- Step 3: Action Plan & Outcome ---
        self.step3_frame = ttk.Frame(self.steps_notebook, padding="20")
        self.steps_notebook.add(self.step3_frame, text="Step 3: Plan & Review")
        self._setup_step3()

        # Navigation buttons at the bottom, outside the notebook tabs
        navigation_frame = ttk.Frame(self, padding="10")
        navigation_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        navigation_frame.grid_columnconfigure(0, weight=1)
        navigation_frame.grid_columnconfigure(1, weight=1)

        self.prev_button = ttk.Button(navigation_frame, text="< Previous", command=self._go_prev_step, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=0, sticky="w", padx=5)

        self.next_button = ttk.Button(navigation_frame, text="Next >", command=self._go_next_step)
        self.next_button.grid(row=0, column=1, sticky="e", padx=5)
        
        self.save_button = ttk.Button(self.step3_frame, text="Save Problem-Solving Record", command=self._save_problem_solving_record)
        # Position this button within step3_frame, below its content
        self.step3_frame.grid_rowconfigure(9, weight=0) # Ensure button row doesn't expand
        self.save_button.grid(row=9, column=0, columnspan=3, pady=20) # This will be managed by _update_navigation_buttons

        self.steps_notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
        self._update_navigation_buttons() # Initial state of buttons

    def _setup_step1(self):
        # Configure columns for better layout
        self.step1_frame.grid_columnconfigure(0, weight=1)
        self.step1_frame.grid_columnconfigure(1, weight=3) # Make entry wider
        self.step1_frame.grid_columnconfigure(2, weight=1) # For instructions
        
        row_idx = 0

        # Date of Entry
        ttk.Label(self.step1_frame, text="Date:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.entry_date_cal = DateEntry(self.step1_frame, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_date_cal.set_date(datetime.date.today())
        self.entry_date_cal.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        # Problem Description
        ttk.Label(self.step1_frame, text="1. Define the Problem:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        self.problem_description_text = scrolledtext.ScrolledText(self.step1_frame, wrap="word", height=6, width=40, font=("Helvetica", 10))
        self.problem_description_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        ttk.Label(self.step1_frame, text="Be specific and objective about the situation and your reaction.").grid(row=row_idx, column=2, sticky="w", padx=5)
        row_idx += 1

    def _setup_step2(self):
        self.step2_frame.grid_columnconfigure(0, weight=1)
        self.step2_frame.grid_columnconfigure(1, weight=3)
        self.step2_frame.grid_columnconfigure(2, weight=1)

        row_idx = 0

        # Brainstorm Solutions
        ttk.Label(self.step2_frame, text="2. Brainstorm Solutions:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        self.brainstorm_solutions_text = scrolledtext.ScrolledText(self.step2_frame, wrap="word", height=8, width=40, font=("Helvetica", 10))
        self.brainstorm_solutions_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        ttk.Label(self.step2_frame, text="List ALL possible solutions, even impractical ones. Quantity over quality for now!").grid(row=row_idx, column=2, sticky="w", padx=5)
        row_idx += 1

        # Chosen Solution
        ttk.Label(self.step2_frame, text="3. Chosen Solution:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        self.chosen_solution_text = scrolledtext.ScrolledText(self.step2_frame, wrap="word", height=5, width=40, font=("Helvetica", 10))
        self.chosen_solution_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        ttk.Label(self.step2_frame, text="From your brainstorm, choose the best solution to try. Briefly explain why.").grid(row=row_idx, column=2, sticky="w", padx=5)
        row_idx += 1

    def _setup_step3(self):
        self.step3_frame.grid_columnconfigure(0, weight=1)
        self.step3_frame.grid_columnconfigure(1, weight=3)
        self.step3_frame.grid_columnconfigure(2, weight=1)

        row_idx = 0

        # Action Plan
        ttk.Label(self.step3_frame, text="4. Action Plan:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        self.action_plan_text = scrolledtext.ScrolledText(self.step3_frame, wrap="word", height=6, width=40, font=("Helvetica", 10))
        self.action_plan_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        ttk.Label(self.step3_frame, text="Specific steps: who, what, when, where, how. Make it actionable!").grid(row=row_idx, column=2, sticky="w", padx=5)
        row_idx += 1

        # Outcome/Review
        ttk.Label(self.step3_frame, text="5. Outcome / Review:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        self.outcome_text = scrolledtext.ScrolledText(self.step3_frame, wrap="word", height=6, width=40, font=("Helvetica", 10))
        self.outcome_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        ttk.Label(self.step3_frame, text="What happened when you tried the solution? Was it successful? What did you learn?").grid(row=row_idx, column=2, sticky="w", padx=5)
        row_idx += 1

        # Problem Status (NEW FIELD)
        ttk.Label(self.step3_frame, text="6. Problem Status:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.problem_status_var = tk.StringVar(self)
        self.problem_status_combobox = ttk.Combobox(self.step3_frame, textvariable=self.problem_status_var,
                                                    values=["Open", "Partially Solved", "Solved", "Abandoned", "N/A"])
        self.problem_status_combobox.grid(row=row_idx, column=1, sticky="ew", pady=5)
        self.problem_status_combobox.set("Open") # Default value
        ttk.Label(self.step3_frame, text="Current status of the problem.").grid(row=row_idx, column=2, sticky="w", padx=5)
        row_idx += 1

    def _on_tab_change(self, event):
        self._update_navigation_buttons()
        # When changing tabs, we might want to temporarily save data from the current tab
        # or just ensure it's ready for the next step. For simplicity here, we'll
        # rely on _save_problem_solving_record to grab all data at the end.

    def _go_next_step(self):
        current_tab_index = self.steps_notebook.index(self.steps_notebook.select())
        if current_tab_index < len(self.steps_notebook.tabs()) - 1:
            # Optional: Add validation for the current step before moving next
            if current_tab_index == 0: # Validation for Step 1
                if not self.problem_description_text.get("1.0", tk.END).strip():
                    messagebox.showwarning("Input Error", "Please define the problem before proceeding.")
                    return
            elif current_tab_index == 1: # Validation for Step 2
                if not self.brainstorm_solutions_text.get("1.0", tk.END).strip() or \
                   not self.chosen_solution_text.get("1.0", tk.END).strip():
                    messagebox.showwarning("Input Error", "Please brainstorm solutions and choose one before proceeding.")
                    return
            
            self.steps_notebook.select(current_tab_index + 1)
            self._update_navigation_buttons()

    def _go_prev_step(self):
        current_tab_index = self.steps_notebook.index(self.steps_notebook.select())
        if current_tab_index > 0:
            self.steps_notebook.select(current_tab_index - 1)
            self._update_navigation_buttons()

    def _update_navigation_buttons(self):
        current_tab_index = self.steps_notebook.index(self.steps_notebook.select())
        total_tabs = len(self.steps_notebook.tabs())

        self.prev_button.config(state=tk.NORMAL if current_tab_index > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if current_tab_index < total_tabs - 1 else tk.DISABLED)
        
        # The save button is part of step3_frame and its visibility is managed
        # directly in the setup and refresh_page methods.
        if current_tab_index == total_tabs - 1: # On the last tab
             self.save_button.grid() # Show the save button
        else:
             self.save_button.grid_remove() # Hide the save button

    def _save_problem_solving_record(self):
        # Collect data from all steps
        entry_date = self.entry_date_cal.get_date().isoformat()
        problem_description = self.problem_description_text.get("1.0", tk.END).strip()
        brainstorm_solutions = self.brainstorm_solutions_text.get("1.0", tk.END).strip()
        chosen_solution = self.chosen_solution_text.get("1.0", tk.END).strip()
        action_plan = self.action_plan_text.get("1.0", tk.END).strip()
        outcome = self.outcome_text.get("1.0", tk.END).strip()
        problem_status = self.problem_status_var.get() # Get selected status

        # Basic validation for the final step fields
        if not all([action_plan, outcome, problem_status]):
            messagebox.showerror("Input Error", "Please fill in all fields for the Action Plan & Review step.")
            return

        # Prepare data, using existing timestamp if editing, otherwise generate new
        if self.record_timestamp:
            self.current_record_data["creation_timestamp"] = self.record_timestamp
        else:
            self.current_record_data["creation_timestamp"] = datetime.datetime.now().isoformat()

        self.current_record_data.update({
            "Date": entry_date,
            "Problem Description": problem_description,
            "Brainstormed Solutions": brainstorm_solutions,
            "Chosen Solution": chosen_solution,
            "Action Plan": action_plan,
            "Outcome/Review": outcome,
            "Problem Status": problem_status # Add the new field
        })

        if self.record_timestamp:
            success = self.data_manager.update_problem_solving_record(self.record_timestamp, self.current_record_data)
            if success:
                messagebox.showinfo("Success", "Problem-Solving record updated successfully!")
            else:
                messagebox.showerror("Error", "Failed to update problem-solving record.")
        else:
            self.data_manager.add_problem_solving_record(self.current_record_data)
            messagebox.showinfo("Success", "Problem-Solving record saved successfully!")
        
        self._clear_form()
        self.controller.show_frame("ProgressPage") # Go back to progress page after save/update
        # Refresh progress page if it's visible, the refresh_page method will handle which tab
        if "ProgressPage" in self.controller.frames:
            self.controller.frames["ProgressPage"].refresh_page()


    def _clear_form(self):
        # Clear all text fields
        self.problem_description_text.delete("1.0", tk.END)
        self.brainstorm_solutions_text.delete("1.0", tk.END)
        self.chosen_solution_text.delete("1.0", tk.END)
        self.action_plan_text.delete("1.0", tk.END)
        self.outcome_text.delete("1.0", tk.END)
        self.entry_date_cal.set_date(datetime.date.today())
        self.problem_status_combobox.set("Open") # Reset status

        # Reset internal data and timestamp
        self.current_record_data = {}
        self.record_timestamp = None
        
        # Go back to the first step
        self.steps_notebook.select(0)
        self._update_navigation_buttons()

    def refresh_page(self, initial_data=None, record_timestamp=None):
        """
        Method called by app.py when this page is brought to front,
        potentially with data for editing.
        """
        self._clear_form() # Always start with a fresh form
        
        if initial_data:
            self.record_timestamp = record_timestamp
            self.current_record_data = initial_data

            self.entry_date_cal.set_date(initial_data.get("Date", datetime.date.today()))
            self.problem_description_text.insert("1.0", initial_data.get("Problem Description", ""))
            self.brainstorm_solutions_text.insert("1.0", initial_data.get("Brainstormed Solutions", ""))
            self.chosen_solution_text.insert("1.0", initial_data.get("Chosen Solution", ""))
            self.action_plan_text.insert("1.0", initial_data.get("Action Plan", ""))
            self.outcome_text.insert("1.0", initial_data.get("Outcome/Review", ""))
            self.problem_status_combobox.set(initial_data.get("Problem Status", "Open"))

            # Change button text for editing
            self.save_button.config(text="Update Problem-Solving Record")
            # Navigate to the last tab directly if editing so user can review/save
            self.steps_notebook.select(len(self.steps_notebook.tabs()) - 1)
        else:
            self.save_button.config(text="Save Problem-Solving Record")
            self._clear_form() # Ensures it's cleared and reset to first tab
            
        self._update_navigation_buttons() # Ensure navigation buttons are updated after data load