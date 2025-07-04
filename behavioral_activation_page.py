# behavioral_activation_page.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import DateEntry
import datetime

class BehavioralActivationPage(ttk.Frame):
    def __init__(self, parent, controller, data_manager):
        super().__init__(parent)
        self.controller = controller
        self.data_manager = data_manager

        self.current_step = 0
        self.total_steps = 2 # Two steps for this form

        # Dictionary to store collected data temporarily
        self.activity_data = {}
        self.record_timestamp = None # To store timestamp for update operations

        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=1) # Step frames container
        self.grid_rowconfigure(2, weight=0) # Navigation buttons
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Behavioral Activation", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        # --- Frame to hold all the step-specific content ---
        self.content_frame = ttk.Frame(self, padding="20")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.step_frames = [] # List to hold individual step frames

        self._create_step_1_planning()
        self._create_step_2_review()

        # --- Navigation Buttons ---
        self.nav_button_frame = ttk.Frame(self, padding="10")
        self.nav_button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=5)
        self.nav_button_frame.grid_columnconfigure(0, weight=1)
        self.nav_button_frame.grid_columnconfigure(1, weight=1)
        self.nav_button_frame.grid_columnconfigure(2, weight=1)

        self.prev_button = ttk.Button(self.nav_button_frame, text="Previous", command=self._prev_step)
        self.prev_button.grid(row=0, column=0, padx=5, sticky="e")

        self.next_button = ttk.Button(self.nav_button_frame, text="Next", command=self._next_step)
        self.next_button.grid(row=0, column=2, padx=5, sticky="w")

        self.save_update_button = ttk.Button(self.nav_button_frame, text="Save Activity", command=self._save_or_update_activity)
        # self.save_update_button will be hidden initially and shown on the last step

        self._show_step(self.current_step) # Show the initial step

    def _create_step_1_planning(self):
        frame = ttk.Frame(self.content_frame, padding=10)
        self.step_frames.append(frame)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1) # For slider labels

        ttk.Label(frame, text="Step 1: Plan Your Activity", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        row_idx = 1
        ttk.Label(frame, text="Activity Date:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.activity_date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.activity_date_entry.set_date(datetime.date.today())
        self.activity_date_entry.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Activity Name:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.activity_name_entry = ttk.Entry(frame, width=40)
        self.activity_name_entry.grid(row=row_idx, column=1, columnspan=2, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Predicted Pleasure (0-10):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.pred_pleasure_label = ttk.Label(frame, text="0")
        self.pred_pleasure_label.grid(row=row_idx, column=2, sticky="w", padx=5)
        self.pred_pleasure_var = tk.IntVar(value=0)
        self.pred_pleasure_scale = ttk.Scale(frame, from_=0, to=10, orient="horizontal", variable=self.pred_pleasure_var, command=lambda v: self.pred_pleasure_label.config(text=f"{int(float(v))}"))
        self.pred_pleasure_scale.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Predicted Mastery (0-10):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.pred_mastery_label = ttk.Label(frame, text="0")
        self.pred_mastery_label.grid(row=row_idx, column=2, sticky="w", padx=5)
        self.pred_mastery_var = tk.IntVar(value=0)
        self.pred_mastery_scale = ttk.Scale(frame, from_=0, to=10, orient="horizontal", variable=self.pred_mastery_var, command=lambda v: self.pred_mastery_label.config(text=f"{int(float(v))}"))
        self.pred_mastery_scale.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

    def _create_step_2_review(self):
        frame = ttk.Frame(self.content_frame, padding=10)
        self.step_frames.append(frame)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1) # For slider labels

        ttk.Label(frame, text="Step 2: Review Your Activity", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        row_idx = 1
        ttk.Label(frame, text="Actual Pleasure (0-10):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.actual_pleasure_label = ttk.Label(frame, text="0")
        self.actual_pleasure_label.grid(row=row_idx, column=2, sticky="w", padx=5)
        self.actual_pleasure_var = tk.IntVar(value=0)
        self.actual_pleasure_scale = ttk.Scale(frame, from_=0, to=10, orient="horizontal", variable=self.actual_pleasure_var, command=lambda v: self.actual_pleasure_label.config(text=f"{int(float(v))}"))
        self.actual_pleasure_scale.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Actual Mastery (0-10):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.actual_mastery_label = ttk.Label(frame, text="0")
        self.actual_mastery_label.grid(row=row_idx, column=2, sticky="w", padx=5)
        self.actual_mastery_var = tk.IntVar(value=0)
        self.actual_mastery_scale = ttk.Scale(frame, from_=0, to=10, orient="horizontal", variable=self.actual_mastery_var, command=lambda v: self.actual_mastery_label.config(text=f"{int(float(v))}"))
        self.actual_mastery_scale.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Notes/Observations:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        self.notes_text = scrolledtext.ScrolledText(frame, wrap="word", height=5, width=40, font=("Helvetica", 10))
        self.notes_text.grid(row=row_idx, column=1, columnspan=2, sticky="ew", pady=5)
        row_idx += 1

    def _show_step(self, step_index):
        # Hide all frames first
        for i, frame in enumerate(self.step_frames):
            if i == step_index:
                frame.grid() # Show the current step's frame
            else:
                frame.grid_remove() # Hide others

        # Update navigation buttons
        self.prev_button.config(state="enabled" if step_index > 0 else "disabled")
        self.next_button.config(state="enabled" if step_index < self.total_steps - 1 else "disabled")

        if step_index == self.total_steps - 1: # Last step
            self.save_update_button.grid(row=0, column=1, padx=5) # Place save/update button in nav frame
            self.next_button.grid_remove() # Hide next button on last step
        else:
            self.save_update_button.grid_remove() # Hide save/update button on other steps
            self.next_button.grid(row=0, column=2, padx=5, sticky="w") # Ensure next button is visible

    def _next_step(self):
        if self._validate_step(self.current_step):
            self._collect_data_for_step(self.current_step)
            self.current_step += 1
            self._show_step(self.current_step)

    def _prev_step(self):
        self.current_step -= 1
        self._show_step(self.current_step)

    def _validate_step(self, step_index):
        if step_index == 0: # Step 1: Planning
            if not self.activity_name_entry.get().strip():
                messagebox.showwarning("Input Error", "Please enter an activity name.")
                return False
            if self.pred_pleasure_var.get() == 0 and self.pred_mastery_var.get() == 0:
                # Optionally enforce non-zero prediction, or leave as is if 0 is valid.
                # For now, allow 0 predictions.
                pass 
        elif step_index == 1: # Step 2: Review
            if self.actual_pleasure_var.get() == 0 and self.actual_mastery_var.get() == 0 and not self.notes_text.get("1.0", tk.END).strip():
                messagebox.showwarning("Input Error", "Please rate actual pleasure/mastery or add some notes.")
                return False
        return True

    def _collect_data_for_step(self, step_index):
        if step_index == 0: # Step 1
            self.activity_data["Activity Date"] = self.activity_date_entry.get_date().isoformat()
            self.activity_data["Activity Name"] = self.activity_name_entry.get().strip()
            self.activity_data["Predicted Pleasure"] = self.pred_pleasure_var.get()
            self.activity_data["Predicted Mastery"] = self.pred_mastery_var.get()
        elif step_index == 1: # Step 2
            self.activity_data["Actual Pleasure"] = self.actual_pleasure_var.get()
            self.activity_data["Actual Mastery"] = self.actual_mastery_var.get()
            self.activity_data["Notes"] = self.notes_text.get("1.0", tk.END).strip()

    def _save_or_update_activity(self):
        if self._validate_step(self.total_steps - 1): # Validate the last step before saving
            self._collect_data_for_step(self.total_steps - 1) # Collect data from the last step

            if self.record_timestamp: # If a timestamp exists, it's an update operation
                success = self.data_manager.update_behavioral_activation_activity(self.record_timestamp, self.activity_data)
                action_word = "updated"
            else: # Otherwise, it's a new record
                success = self.data_manager.add_behavioral_activation_activity(self.activity_data)
                action_word = "saved"

            if success:
                messagebox.showinfo("Success", f"Activity {action_word} successfully!")
                self._clear_form() # Reset the form
                self.controller.show_frame("ProgressPage") # Go to progress page to see the changes
            else:
                messagebox.showerror("Error", f"Failed to {action_word} activity. Please try again.")

    def _clear_form(self):
        """Resets all form fields to their default state."""
        self.activity_date_entry.set_date(datetime.date.today())
        self.activity_name_entry.delete(0, tk.END)
        self.pred_pleasure_var.set(0)
        self.pred_pleasure_label.config(text="0")
        self.pred_mastery_var.set(0)
        self.pred_mastery_label.config(text="0")
        self.actual_pleasure_var.set(0)
        self.actual_pleasure_label.config(text="0")
        self.actual_mastery_var.set(0)
        self.actual_mastery_label.config(text="0")
        self.notes_text.delete("1.0", tk.END)
        
        self.activity_data = {} # Clear temporary stored data
        self.record_timestamp = None # Reset timestamp
        self.save_update_button.config(text="Save Activity") # Reset button text
        self.current_step = 0
        self._show_step(self.current_step) # Go back to the first step

    def load_data(self, initial_data=None, record_timestamp=None):
        """
        Loads activity data into the form for editing.
        This method is called by app.py's show_frame when editing is initiated.
        """
        self._clear_form() # Start with a clean slate

        if initial_data:
            self.record_timestamp = record_timestamp
            self.save_update_button.config(text="Update Activity") # Change button text to indicate update mode

            # Populate fields from initial_data
            self.activity_date_entry.set_date(datetime.datetime.fromisoformat(initial_data.get("Activity Date", datetime.date.today().isoformat())).date())
            self.activity_name_entry.insert(0, initial_data.get("Activity Name", ""))
            self.pred_pleasure_var.set(initial_data.get("Predicted Pleasure", 0))
            self.pred_pleasure_label.config(text=str(initial_data.get("Predicted Pleasure", 0)))
            self.pred_mastery_var.set(initial_data.get("Predicted Mastery", 0))
            self.pred_mastery_label.config(text=str(initial_data.get("Predicted Mastery", 0)))
            
            # These are for Step 2, ensure they are also populated
            self.actual_pleasure_var.set(initial_data.get("Actual Pleasure", 0))
            self.actual_pleasure_label.config(text=str(initial_data.get("Actual Pleasure", 0)))
            self.actual_mastery_var.set(initial_data.get("Actual Mastery", 0))
            self.actual_mastery_label.config(text=str(initial_data.get("Actual Mastery", 0)))
            self.notes_text.insert("1.0", initial_data.get("Notes", ""))
            
            self.activity_data = initial_data.copy() # Store the initial data for update operation

        # Always start at the first step when loading data or resetting
        self.current_step = 0
        self._show_step(self.current_step)

    def refresh_page(self):
        """
        Called by app.py when navigating to this page for a new record (not editing).
        Ensures the form is clean when accessed via general navigation.
        """
        self._clear_form()