# progress_page.py

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime

class ProgressPage(ttk.Frame):
    def __init__(self, parent, controller, data_manager):
        super().__init__(parent)
        self.controller = controller
        self.data_manager = data_manager

        # Dictionaries to map Treeview item IDs to full record data for each type
        self.ba_activity_data_map = {}
        self.thought_record_data_map = {}
        self.problem_solving_data_map = {}

        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=1) # Notebook/content area
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Your Progress & Logs", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Behavioral Activation Log Tab ---
        self.ba_log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ba_log_frame, text="Activity Log")
        self._setup_ba_log_tab()

        # --- Behavioral Activation Trends Tab (for plotting) ---
        self.ba_trends_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ba_trends_frame, text="Activity Trends")
        self._setup_ba_trends_tab() # Initial setup, will be updated on refresh

        # --- NEW: Thought Records Log Tab ---
        self.thought_records_log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.thought_records_log_frame, text="Thought Records Log")
        self._setup_thought_records_tab()

        # --- NEW: Problem Solving Log Tab ---
        self.problem_solving_log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.problem_solving_log_frame, text="Problem Solving Log")
        self._setup_problem_solving_tab()

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    # --- Behavioral Activation Log Tab Setup (Existing) ---
    def _setup_ba_log_tab(self):
        self.ba_log_frame.grid_rowconfigure(0, weight=1) # Treeview
        self.ba_log_frame.grid_rowconfigure(1, weight=0) # Buttons
        self.ba_log_frame.grid_columnconfigure(0, weight=1)

        # Treeview for displaying BA activities
        columns = ("Date", "Activity", "Pred. Pleasure", "Act. Pleasure", "Pred. Mastery", "Act. Mastery", "Notes")
        self.ba_tree = ttk.Treeview(self.ba_log_frame, columns=columns, show="headings")

        # Define headings
        self.ba_tree.heading("Date", text="Date")
        self.ba_tree.heading("Activity", text="Activity")
        self.ba_tree.heading("Pred. Pleasure", text="P-P")
        self.ba_tree.heading("Act. Pleasure", text="A-P")
        self.ba_tree.heading("Pred. Mastery", text="P-M")
        self.ba_tree.heading("Act. Mastery", text="A-M")
        self.ba_tree.heading("Notes", text="Notes")

        # Set column widths
        self.ba_tree.column("Date", width=100, anchor="center")
        self.ba_tree.column("Activity", width=150)
        self.ba_tree.column("Pred. Pleasure", width=60, anchor="center")
        self.ba_tree.column("Act. Pleasure", width=60, anchor="center")
        self.ba_tree.column("Pred. Mastery", width=60, anchor="center")
        self.ba_tree.column("Act. Mastery", width=60, anchor="center")
        self.ba_tree.column("Notes", width=250)

        self.ba_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.ba_log_frame, orient="vertical", command=self.ba_tree.yview)
        self.ba_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Buttons for actions
        button_frame = ttk.Frame(self.ba_log_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        ttk.Button(button_frame, text="Edit Selected", command=self._edit_selected_activity).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Delete Selected", command=self._delete_selected_activity).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Refresh List", command=self.populate_ba_treeview).grid(row=0, column=2, padx=10)

        # Double-click to edit
        self.ba_tree.bind("<Double-1>", lambda event: self._edit_selected_activity())


    def populate_ba_treeview(self):
        # Clear existing items
        for item in self.ba_tree.get_children():
            self.ba_tree.delete(item)

        # Clear the data map before repopulating
        self.ba_activity_data_map.clear()

        # Get all activities
        activities = self.data_manager.get_all_behavioral_activation_activities()
        
        # Sort activities by date, then by creation_timestamp for consistent ordering
        activities.sort(key=lambda x: (x.get("Activity Date", ""), x.get("creation_timestamp", "")))

        # Insert new data
        for activity in activities:
            item_id = activity.get("creation_timestamp") # Use creation_timestamp as unique item ID
            
            # If for some reason a record doesn't have a timestamp (older data), create a unique one
            if item_id is None:
                item_id = f"no_timestamp_{id(activity)}_{datetime.now().microsecond}"
                activity["creation_timestamp"] = item_id # Add it to the activity for consistent lookup

            self.ba_tree.insert("", "end", iid=item_id, values=(
                activity.get("Activity Date", "N/A"),
                activity.get("Activity Name", "N/A"),
                activity.get("Predicted Pleasure", "N/A"),
                activity.get("Actual Pleasure", "N/A"),
                activity.get("Predicted Mastery", "N/A"),
                activity.get("Actual Mastery", "N/A"),
                activity.get("Notes", "")
            ))
            # Store the full activity data in our map
            self.ba_activity_data_map[item_id] = activity


    def _edit_selected_activity(self):
        selected_items = self.ba_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an activity to edit.")
            return

        item_id = selected_items[0] # Get the iid of the first selected item
        
        # Retrieve the full activity data from our map
        activity_data = self.ba_activity_data_map.get(item_id)
        
        if activity_data is None:
            messagebox.showerror("Error", "Could not retrieve activity data for editing.")
            return
        
        # Pass the data to the BehavioralActivationPage for loading
        self.controller.show_frame("BehavioralActivationPage", initial_data=activity_data, record_timestamp=activity_data.get("creation_timestamp"))


    def _delete_selected_activity(self):
        selected_items = self.ba_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select an activity to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected activity?")
        if confirm:
            item_id = selected_items[0] # Get the iid of the selected item
            
            # Retrieve the full activity data from our map
            activity_data = self.ba_activity_data_map.get(item_id)

            if activity_data is None:
                messagebox.showerror("Error", "Could not retrieve activity data for deletion.")
                return

            record_timestamp = activity_data.get("creation_timestamp")

            if record_timestamp:
                success = self.data_manager.delete_behavioral_activation_activity(record_timestamp)
                if success:
                    messagebox.showinfo("Deleted", "Activity deleted successfully.")
                    # Remove from our map as well
                    self.ba_activity_data_map.pop(item_id, None)
                    self.populate_ba_treeview() # Refresh list
                    self.plot_ba_trends() # Refresh plot
                else:
                    messagebox.showerror("Error", "Failed to delete activity. Record not found in data manager.")
            else:
                messagebox.showerror("Error", "Cannot delete activity: No unique timestamp found for this record.")


    # --- Behavioral Activation Trends Tab Setup (Existing) ---
    def _setup_ba_trends_tab(self):
        self.ba_trends_frame.grid_rowconfigure(0, weight=1)
        self.ba_trends_frame.grid_columnconfigure(0, weight=1)
        
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.ba_trends_frame)
        self.canvas_widget = self.canvas_plot.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.plot_ba_trends() # Initial plot

    def plot_ba_trends(self):
        """Plots the trends for Behavioral Activation activities."""
        self.ax.clear() # Clear previous plot

        activities = self.data_manager.get_all_behavioral_activation_activities()
        if not activities:
            self.ax.text(0.5, 0.5, "No Behavioral Activation data to plot.",
                          horizontalalignment='center', verticalalignment='center',
                          transform=self.ax.transAxes, fontsize=12)
            self.canvas_plot.draw()
            return

        df = pd.DataFrame(activities)
        df["Activity Date"] = pd.to_datetime(df["Activity Date"])
        df = df.sort_values(by="Activity Date")

        # Plotting Predicted vs Actual Pleasure
        self.ax.plot(df["Activity Date"], df["Predicted Pleasure"], marker='o', linestyle='-', label="Predicted Pleasure")
        self.ax.plot(df["Activity Date"], df["Actual Pleasure"], marker='o', linestyle='--', label="Actual Pleasure")

        # Plotting Predicted vs Actual Mastery
        self.ax.plot(df["Activity Date"], df["Predicted Mastery"], marker='x', linestyle='-', label="Predicted Mastery")
        self.ax.plot(df["Activity Date"], df["Actual Mastery"], marker='x', linestyle='--', label="Actual Mastery")

        self.ax.set_title("Behavioral Activation: Pleasure & Mastery Trends")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Rating (0-10)")
        self.ax.legend()
        self.ax.grid(True)
        self.fig.autofmt_xdate() # Rotate dates for better readability

        self.canvas_plot.draw()

    # --- NEW: Thought Records Tab Setup ---
    def _setup_thought_records_tab(self):
        self.thought_records_log_frame.grid_rowconfigure(0, weight=1) # Treeview
        self.thought_records_log_frame.grid_rowconfigure(1, weight=0) # Buttons
        self.thought_records_log_frame.grid_columnconfigure(0, weight=1)

        columns = ("Date", "Situation", "Emotion", "Automatic Thought", "Alternative Thought")
        self.thought_records_tree = ttk.Treeview(self.thought_records_log_frame, columns=columns, show="headings")
        
        self.thought_records_tree.heading("Date", text="Date")
        self.thought_records_tree.heading("Situation", text="Situation")
        self.thought_records_tree.heading("Emotion", text="Main Emotion")
        self.thought_records_tree.heading("Automatic Thought", text="Automatic Thought")
        self.thought_records_tree.heading("Alternative Thought", text="Alternative Thought")

        self.thought_records_tree.column("Date", width=100, anchor="center")
        self.thought_records_tree.column("Situation", width=200, anchor="w")
        self.thought_records_tree.column("Emotion", width=120, anchor="center")
        self.thought_records_tree.column("Automatic Thought", width=250, anchor="w")
        self.thought_records_tree.column("Alternative Thought", width=250, anchor="w")

        self.thought_records_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(self.thought_records_log_frame, orient="vertical", command=self.thought_records_tree.yview)
        self.thought_records_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        button_frame = ttk.Frame(self.thought_records_log_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        ttk.Button(button_frame, text="Edit Selected", command=self._edit_selected_thought_record).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Delete Selected", command=self._delete_selected_thought_record).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Refresh List", command=self._populate_thought_records_treeview).grid(row=0, column=2, padx=10)

        self.thought_records_tree.bind("<Double-1>", lambda event: self._edit_selected_thought_record())


    def _populate_thought_records_treeview(self):
        for item in self.thought_records_tree.get_children():
            self.thought_records_tree.delete(item)
        self.thought_record_data_map.clear()

        # This line correctly calls the updated DataManager method
        records = self.data_manager.get_all_thought_records() 
        records.sort(key=lambda x: (x.get("Date", ""), x.get("creation_timestamp", "")))

        for record in records:
            item_id = record.get("creation_timestamp")
            if item_id is None:
                item_id = f"no_timestamp_tr_{id(record)}_{datetime.now().microsecond}"
                record["creation_timestamp"] = item_id

            display_date = record.get("Date", "N/A")
            try:
                display_date = datetime.fromisoformat(display_date).strftime("%Y-%m-%d")
            except ValueError:
                pass

            self.thought_records_tree.insert("", "end", iid=item_id, values=(
                display_date,
                record.get("Situation", "N/A"),
                record.get("Main Emotion", "N/A"),
                record.get("Automatic Thought", "N/A"),
                record.get("Alternative Thought", "N/A")
            ))
            self.thought_record_data_map[item_id] = record

    def _edit_selected_thought_record(self):
        selected_items = self.thought_records_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a Thought Record to edit.")
            return

        item_id = selected_items[0]
        record_data = self.thought_record_data_map.get(item_id)
        
        if record_data is None:
            messagebox.showerror("Error", "Could not retrieve Thought Record data for editing.")
            return
        
        self.controller.show_frame("ThoughtRecordPage", initial_data=record_data, record_timestamp=record_data.get("creation_timestamp"))

    def _delete_selected_thought_record(self):
        selected_items = self.thought_records_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a Thought Record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected Thought Record?")
        if confirm:
            item_id = selected_items[0]
            record_data = self.thought_record_data_map.get(item_id)

            if record_data is None:
                messagebox.showerror("Error", "Could not retrieve Thought Record data for deletion.")
                return

            record_timestamp = record_data.get("creation_timestamp")

            if record_timestamp:
                success = self.data_manager.delete_thought_record(record_timestamp)
                if success:
                    messagebox.showinfo("Deleted", "Thought Record deleted successfully.")
                    self.thought_record_data_map.pop(item_id, None)
                    self._populate_thought_records_treeview()
                else:
                    messagebox.showerror("Error", "Failed to delete Thought Record. Record not found in data manager.")
            else:
                messagebox.showerror("Error", "Cannot delete Thought Record: No unique timestamp found for this record.")


    # --- NEW: Problem Solving Tab Setup ---
    def _setup_problem_solving_tab(self):
        self.problem_solving_log_frame.grid_rowconfigure(0, weight=1) # Treeview
        self.problem_solving_log_frame.grid_rowconfigure(1, weight=0) # Buttons
        self.problem_solving_log_frame.grid_columnconfigure(0, weight=1)

        columns = ("Date", "Problem Description", "Chosen Solution", "Problem Status")
        self.problem_solving_tree = ttk.Treeview(self.problem_solving_log_frame, columns=columns, show="headings")
        
        self.problem_solving_tree.heading("Date", text="Date")
        self.problem_solving_tree.heading("Problem Description", text="Problem")
        self.problem_solving_tree.heading("Chosen Solution", text="Solution")
        self.problem_solving_tree.heading("Problem Status", text="Status")

        self.problem_solving_tree.column("Date", width=100, anchor="center")
        self.problem_solving_tree.column("Problem Description", width=300, anchor="w")
        self.problem_solving_tree.column("Chosen Solution", width=250, anchor="w")
        self.problem_solving_tree.column("Problem Status", width=120, anchor="center")

        self.problem_solving_tree.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(self.problem_solving_log_frame, orient="vertical", command=self.problem_solving_tree.yview)
        self.problem_solving_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        button_frame = ttk.Frame(self.problem_solving_log_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        ttk.Button(button_frame, text="Edit Selected", command=self._edit_selected_problem_solving_record).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Delete Selected", command=self._delete_selected_problem_solving_record).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Refresh List", command=self._populate_problem_solving_treeview).grid(row=0, column=2, padx=10)

        self.problem_solving_tree.bind("<Double-1>", lambda event: self._edit_selected_problem_solving_record())


    def _populate_problem_solving_treeview(self):
        for item in self.problem_solving_tree.get_children():
            self.problem_solving_tree.delete(item)
        self.problem_solving_data_map.clear()

        # This line correctly calls the updated DataManager method
        records = self.data_manager.get_all_problem_solving_records() 
        records.sort(key=lambda x: (x.get("Date", ""), x.get("creation_timestamp", "")))

        for record in records:
            item_id = record.get("creation_timestamp")
            if item_id is None:
                item_id = f"no_timestamp_ps_{id(record)}_{datetime.now().microsecond}"
                record["creation_timestamp"] = item_id

            display_date = record.get("Date", "N/A")
            try:
                display_date = datetime.fromisoformat(display_date).strftime("%Y-%m-%d")
            except ValueError:
                pass

            self.problem_solving_tree.insert("", "end", iid=item_id, values=(
                display_date,
                record.get("Problem Description", "N/A"),
                record.get("Chosen Solution", "N/A"),
                record.get("Problem Status", "N/A")
            ))
            self.problem_solving_data_map[item_id] = record

    def _edit_selected_problem_solving_record(self):
        selected_items = self.problem_solving_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a Problem Solving Record to edit.")
            return

        item_id = selected_items[0]
        record_data = self.problem_solving_data_map.get(item_id)
        
        if record_data is None:
            messagebox.showerror("Error", "Could not retrieve Problem Solving Record data for editing.")
            return
        
        self.controller.show_frame("ProblemSolvingPage", initial_data=record_data, record_timestamp=record_data.get("creation_timestamp"))

    def _delete_selected_problem_solving_record(self):
        selected_items = self.problem_solving_tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a Problem Solving Record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected Problem Solving Record?")
        if confirm:
            item_id = selected_items[0]
            record_data = self.problem_solving_data_map.get(item_id)

            if record_data is None:
                messagebox.showerror("Error", "Could not retrieve Problem Solving Record data for deletion.")
                return

            record_timestamp = record_data.get("creation_timestamp")

            if record_timestamp:
                success = self.data_manager.delete_problem_solving_record(record_timestamp)
                if success:
                    messagebox.showinfo("Deleted", "Problem Solving Record deleted successfully.")
                    self.problem_solving_data_map.pop(item_id, None)
                    self._populate_problem_solving_treeview()
                else:
                    messagebox.showerror("Error", "Failed to delete Problem Solving Record. Record not found in data manager.")
            else:
                messagebox.showerror("Error", "Cannot delete Problem Solving Record: No unique timestamp found for this record.")


    def refresh_page(self):
        """Method called by app.py when this page is brought to front."""
        # This will ensure the correct tab is refreshed
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if selected_tab == "Activity Log":
            self.populate_ba_treeview()
        elif selected_tab == "Activity Trends":
            self.plot_ba_trends()
        elif selected_tab == "Thought Records Log":
            self._populate_thought_records_treeview()
        elif selected_tab == "Problem Solving Log":
            self._populate_problem_solving_treeview()

    def _on_tab_change(self, event):
        # Refresh content based on selected tab
        self.refresh_page() # Call the main refresh method which checks the active tab