# thought_record_page.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkcalendar import DateEntry
import datetime

class ThoughtRecordPage(ttk.Frame):
    def __init__(self, parent, controller, data_manager):
        super().__init__(parent)
        self.controller = controller
        self.data_manager = data_manager

        self.current_step = 0
        self.total_steps = 4 # Number of distinct steps in the thought record

        # Dictionary to store collected data temporarily
        self.record_data = {}
        # List to store selected emotions and their initial/final labels
        self.selected_emotions = {} # {emotion_name: {'initial_var': IntVar, 'final_var': IntVar}}

        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=1) # Step frames
        self.grid_rowconfigure(2, weight=0) # Navigation buttons
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Thought Record", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        # --- Frame to hold all the step-specific content ---
        self.content_frame = ttk.Frame(self, padding="20")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.step_frames = [] # List to hold individual step frames

        self._create_step_1_situation_emotions()
        self._create_step_2_automatic_thoughts()
        self._create_step_3_evidence()
        self._create_step_4_alternative_outcome()

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

        self.submit_button = ttk.Button(self.nav_button_frame, text="Save Record", command=self._save_record)
        # self.submit_button will be hidden initially and shown on the last step

        self._show_step(self.current_step) # Show the initial step

    def _create_step_1_situation_emotions(self):
        frame = ttk.Frame(self.content_frame, padding=10)
        self.step_frames.append(frame)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1) # For intensity labels

        ttk.Label(frame, text="Step 1: Situation & Initial Emotions", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        row_idx = 1
        ttk.Label(frame, text="Date:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.set_date(datetime.date.today())
        self.date_entry.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Situation:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        ttk.Label(frame, text="(Who, what, when, where? What led to the unpleasant feeling?)", wraplength=300, font=("Helvetica", 8, "italic")).grid(row=row_idx, column=2, sticky="nw", padx=5)
        self.situation_text = scrolledtext.ScrolledText(frame, wrap="word", height=5, width=40, font=("Helvetica", 10))
        self.situation_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Initial Emotions & Intensity (0-100%):", font=("Helvetica", 10, "bold")).grid(row=row_idx, column=0, columnspan=3, sticky="w", pady=(15, 5))
        row_idx += 1

        # Common emotions checklist with intensity sliders
        emotion_options = ["Sad", "Anxious", "Angry", "Frustrated", "Guilty", "Ashamed", "Hopeless", "Scared", "Embarrassed", "Discouraged"]
        self.emotion_checkbox_vars = {} # {emotion_name: BooleanVar}
        self.emotion_intensity_labels = {} # {emotion_name: Label}

        col_count = 3
        for i, emotion in enumerate(emotion_options):
            self.emotion_checkbox_vars[emotion] = tk.BooleanVar(value=False)
            initial_intensity_var = tk.IntVar(value=0) # For initial rating
            self.selected_emotions[emotion] = {'initial_var': initial_intensity_var, 'final_var': tk.IntVar(value=0)} # Store both for re-rating

            chk = ttk.Checkbutton(frame, text=emotion, variable=self.emotion_checkbox_vars[emotion],
                                  command=lambda e=emotion: self._toggle_emotion_intensity(e))
            chk.grid(row=row_idx + i // col_count, column=(i % col_count) * 2, sticky="w", pady=2)

            slider_label = ttk.Label(frame, text="0%")
            slider = ttk.Scale(frame, from_=0, to=100, orient="horizontal",
                               variable=initial_intensity_var,
                               command=lambda v, l=slider_label: l.config(text=f"{int(float(v))}%"))
            slider.grid(row=row_idx + i // col_count, column=(i % col_count) * 2 + 1, sticky="ew", padx=5)
            self.emotion_intensity_labels[emotion] = slider_label # Store reference to the label
            slider_label.grid(row=row_idx + i // col_count, column=(i % col_count) * 2 + 2, sticky="w") # Place label next to slider

            # Disable sliders initially
            slider.config(state='disabled')
            initial_intensity_var.set(0) # Reset to 0 when disabled

        row_idx += (len(emotion_options) + col_count - 1) // col_count # Adjust row_idx for next section

    def _toggle_emotion_intensity(self, emotion_name):
        # Enable/disable the slider based on checkbox state
        is_checked = self.emotion_checkbox_vars[emotion_name].get()
        # Find the slider widget associated with this emotion
        # This is a bit tricky with the dynamic grid layout, so we'll re-create logic
        # A more robust way might be to store direct widget references for scales.
        # For simplicity, we assume scales are always next to their checkboxes.
        
        # Find the slider by iterating through the widgets or by storing references when creating them
        # Let's adjust _create_step_1 to store scale references as well for easier access
        
        # Simpler approach for now: we only care about the *value* of the intensity,
        # which is stored in self.selected_emotions[emotion]['initial_var']
        # The UI part (enabling/disabling the actual ttk.Scale widget) is a bit harder
        # without directly storing widget references in a way that maps emotion to scale widget.
        # For a basic functional demo, we'll let the user manually set to 0 if unchecked,
        # or disable the scale visually if we stored the scale widget references.

        # To properly disable/enable scales, we need to store them.
        # Let's refactor _create_step_1_situation_emotions to store references to scales.
        pass # This function will need to be properly implemented once scale references are stored.
             # For now, the user can just set intensity to 0 manually if not selected.
             # Or, the validation on _next_step will ignore unchecked emotions.

    # Refactored _create_step_1 to store scale widgets
    def _create_step_1_situation_emotions(self):
        frame = ttk.Frame(self.content_frame, padding=10)
        self.step_frames.append(frame)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text="Step 1: Situation & Initial Emotions", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        row_idx = 1
        ttk.Label(frame, text="Date:").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.set_date(datetime.date.today())
        self.date_entry.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Situation:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        ttk.Label(frame, text="(Who, what, when, where? What led to the unpleasant feeling?)", wraplength=300, font=("Helvetica", 8, "italic")).grid(row=row_idx, column=2, sticky="nw", padx=5)
        self.situation_text = scrolledtext.ScrolledText(frame, wrap="word", height=5, width=40, font=("Helvetica", 10))
        self.situation_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Initial Emotions & Intensity (0-100%):", font=("Helvetica", 10, "bold")).grid(row=row_idx, column=0, columnspan=3, sticky="w", pady=(15, 5))
        row_idx += 1

        # Common emotions checklist with intensity sliders
        emotion_options = ["Sad", "Anxious", "Angry", "Frustrated", "Guilty", "Ashamed", "Hopeless", "Scared", "Embarrassed", "Discouraged"]
        self.emotion_checkbox_vars = {} # {emotion_name: BooleanVar}
        self.emotion_intensity_labels = {} # {emotion_name: Label}
        self.emotion_intensity_scales = {} # --- NEW: Store scale widgets ---

        col_count = 3
        for i, emotion in enumerate(emotion_options):
            self.emotion_checkbox_vars[emotion] = tk.BooleanVar(value=False)
            initial_intensity_var = tk.IntVar(value=0) # For initial rating
            final_intensity_var = tk.IntVar(value=0) # For final rating, used in step 4
            self.selected_emotions[emotion] = {'initial_var': initial_intensity_var, 'final_var': final_intensity_var}

            chk = ttk.Checkbutton(frame, text=emotion, variable=self.emotion_checkbox_vars[emotion],
                                  command=lambda e=emotion: self._toggle_emotion_intensity_scale(e))
            chk.grid(row=row_idx + i // col_count, column=(i % col_count) * 2, sticky="w", pady=2)

            slider_label = ttk.Label(frame, text="0%")
            slider = ttk.Scale(frame, from_=0, to=100, orient="horizontal",
                               variable=initial_intensity_var,
                               command=lambda v, l=slider_label: l.config(text=f"{int(float(v))}%"))
            slider.grid(row=row_idx + i // col_count, column=(i % col_count) * 2 + 1, sticky="ew", padx=5)
            self.emotion_intensity_labels[emotion] = slider_label
            self.emotion_intensity_scales[emotion] = slider # --- NEW: Store scale reference ---
            slider_label.grid(row=row_idx + i // col_count, column=(i % col_count) * 2 + 2, sticky="w")

            slider.config(state='disabled')
            initial_intensity_var.set(0) # Ensure it starts at 0

        row_idx += (len(emotion_options) + col_count - 1) // col_count # Adjust row_idx for next section

    def _toggle_emotion_intensity_scale(self, emotion_name):
        # Enable/disable the slider and reset its value when checkbox is toggled
        is_checked = self.emotion_checkbox_vars[emotion_name].get()
        scale_widget = self.emotion_intensity_scales[emotion_name]
        intensity_var = self.selected_emotions[emotion_name]['initial_var']
        label_widget = self.emotion_intensity_labels[emotion_name]

        if is_checked:
            scale_widget.config(state='enabled')
            # Retain last set value or set to a default if you prefer
            if intensity_var.get() == 0: # Only set to 50 if it was 0 (disabled state)
                intensity_var.set(50) # Set a default intensity when enabled
                label_widget.config(text="50%")
        else:
            scale_widget.config(state='disabled')
            intensity_var.set(0) # Reset to 0 when disabled
            label_widget.config(text="0%")


    def _create_step_2_automatic_thoughts(self):
        frame = ttk.Frame(self.content_frame, padding=10)
        self.step_frames.append(frame)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text="Step 2: Automatic Thoughts", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        row_idx = 1
        ttk.Label(frame, text="Automatic Thoughts:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        ttk.Label(frame, text="(What thoughts or images went through your mind? What were you thinking/believing?)", wraplength=300, font=("Helvetica", 8, "italic")).grid(row=row_idx, column=2, sticky="nw", padx=5)
        self.automatic_thoughts_text = scrolledtext.ScrolledText(frame, wrap="word", height=5, width=40, font=("Helvetica", 10))
        self.automatic_thoughts_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Belief in Automatic Thoughts (0-100%):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.belief_auto_label = ttk.Label(frame, text="0%")
        self.belief_auto_label.grid(row=row_idx, column=2, sticky="w", padx=5)
        self.belief_auto_scale_var = tk.IntVar(value=0)
        self.belief_auto_scale = ttk.Scale(frame, from_=0, to=100, orient="horizontal", variable=self.belief_auto_scale_var, command=lambda v: self.belief_auto_label.config(text=f"{int(float(v))}%"))
        self.belief_auto_scale.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

    def _create_step_3_evidence(self):
        frame = ttk.Frame(self.content_frame, padding=10)
        self.step_frames.append(frame)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text="Step 3: Evidence For/Against", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        row_idx = 1
        ttk.Label(frame, text="Evidence FOR the automatic thought:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        ttk.Label(frame, text="(Facts, experiences, memories that support your automatic thought)", wraplength=300, font=("Helvetica", 8, "italic")).grid(row=row_idx, column=2, sticky="nw", padx=5)
        self.evidence_for_text = scrolledtext.ScrolledText(frame, wrap="word", height=5, width=40, font=("Helvetica", 10))
        self.evidence_for_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Evidence AGAINST the automatic thought:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        ttk.Label(frame, text="(Facts, experiences, memories that contradict your automatic thought)", wraplength=300, font=("Helvetica", 8, "italic")).grid(row=row_idx, column=2, sticky="nw", padx=5)
        self.evidence_against_text = scrolledtext.ScrolledText(frame, wrap="word", height=5, width=40, font=("Helvetica", 10))
        self.evidence_against_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

    def _create_step_4_alternative_outcome(self):
        frame = ttk.Frame(self.content_frame, padding=10)
        self.step_frames.append(frame)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)
        frame.grid_columnconfigure(2, weight=1)

        ttk.Label(frame, text="Step 4: Alternative Thought & Re-evaluation", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        row_idx = 1
        ttk.Label(frame, text="Alternative/Balanced Thought:").grid(row=row_idx, column=0, sticky="nw", pady=5)
        ttk.Label(frame, text="(A more realistic, helpful, or balanced thought)", wraplength=300, font=("Helvetica", 8, "italic")).grid(row=row_idx, column=2, sticky="nw", padx=5)
        self.alternative_thought_text = scrolledtext.ScrolledText(frame, wrap="word", height=5, width=40, font=("Helvetica", 10))
        self.alternative_thought_text.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Belief in Alternative Thought (0-100%):").grid(row=row_idx, column=0, sticky="w", pady=5)
        self.belief_alt_label = ttk.Label(frame, text="0%")
        self.belief_alt_label.grid(row=row_idx, column=2, sticky="w", padx=5)
        self.belief_alt_scale_var = tk.IntVar(value=0)
        self.belief_alt_scale = ttk.Scale(frame, from_=0, to=100, orient="horizontal", variable=self.belief_alt_scale_var, command=lambda v: self.belief_alt_label.config(text=f"{int(float(v))}%"))
        self.belief_alt_scale.grid(row=row_idx, column=1, sticky="ew", pady=5)
        row_idx += 1

        ttk.Label(frame, text="Re-rate Initial Emotions (0-100%):", font=("Helvetica", 10, "bold")).grid(row=row_idx, column=0, columnspan=3, sticky="w", pady=(15, 5))
        row_idx += 1

        # Re-rating sliders for selected emotions from Step 1
        self.final_emotion_scales = {} # {emotion_name: ttk.Scale}
        self.final_emotion_labels = {} # {emotion_name: ttk.Label}
        
        # We need a dynamic way to show only the selected emotions from Step 1.
        # This will be handled in _show_step or _next_step when moving to step 4.
        # For now, create placeholders for all emotions, but they will be dynamically added/removed
        # or their visibility controlled.
        
        # A simpler initial approach is to dynamically create/place these widgets on the fly
        # when step 4 is shown, based on the selected emotions.
        self.final_emotion_container = ttk.Frame(frame)
        self.final_emotion_container.grid(row=row_idx, column=0, columnspan=3, sticky="ew", pady=5)
        # We will populate this container when _show_step moves to step 4.


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
            self.submit_button.grid(row=0, column=1, padx=5) # Place submit button in nav frame
            self.next_button.grid_remove() # Hide next button on last step
            self._update_final_emotions_section() # Populate final emotions for step 4
        else:
            self.submit_button.grid_remove() # Hide submit button on other steps
            self.next_button.grid(row=0, column=2, padx=5, sticky="w") # Ensure next button is visible

        # Update step title if needed (already part of frame itself)
        # self.nav_button_frame.winfo_parent().winfo_children()[0].config(text=f"Step {step_index + 1}/{self.total_steps}") # Example: update overall title


    def _update_final_emotions_section(self):
        # Clear previous final emotion widgets
        for widget in self.final_emotion_container.winfo_children():
            widget.destroy()
        
        self.final_emotion_scales.clear()
        self.final_emotion_labels.clear()

        # Only create sliders for emotions that were checked in Step 1
        final_emotions_row_idx = 0
        col_count = 3 # Same as initial emotions layout

        for i, emotion in enumerate(self.emotion_checkbox_vars):
            if self.emotion_checkbox_vars[emotion].get(): # If emotion was selected in step 1
                # Retrieve the final_var associated with this emotion
                final_intensity_var = self.selected_emotions[emotion]['final_var']

                ttk.Label(self.final_emotion_container, text=f"Re-rate {emotion}:").grid(row=final_emotions_row_idx, column=(i % col_count) * 2, sticky="w", pady=2)
                
                final_slider_label = ttk.Label(self.final_emotion_container, text=f"{final_intensity_var.get()}%")
                final_slider = ttk.Scale(self.final_emotion_container, from_=0, to=100, orient="horizontal",
                                         variable=final_intensity_var,
                                         command=lambda v, l=final_slider_label: l.config(text=f"{int(float(v))}%"))
                
                final_slider.grid(row=final_emotions_row_idx, column=(i % col_count) * 2 + 1, sticky="ew", padx=5)
                final_slider_label.grid(row=final_emotions_row_idx, column=(i % col_count) * 2 + 2, sticky="w")

                self.final_emotion_scales[emotion] = final_slider
                self.final_emotion_labels[emotion] = final_slider_label

                if (i + 1) % col_count == 0: # Move to next row if current row is full
                    final_emotions_row_idx += 1
        
        if not self.final_emotion_scales: # If no emotions were selected in step 1
            ttk.Label(self.final_emotion_container, text="No emotions selected in Step 1 to re-rate.", font=("Helvetica", 9, "italic")).grid(row=0, column=0, columnspan=3, sticky="w")

    def _next_step(self):
        if self._validate_step(self.current_step):
            self._collect_data_for_step(self.current_step)
            self.current_step += 1
            self._show_step(self.current_step)

    def _prev_step(self):
        self.current_step -= 1
        self._show_step(self.current_step)

    def _validate_step(self, step_index):
        if step_index == 0: # Step 1: Situation & Emotions
            if not self.situation_text.get("1.0", tk.END).strip():
                messagebox.showwarning("Input Error", "Please describe the situation.")
                return False
            # Check if at least one emotion is selected
            selected_any_emotion = any(var.get() for var in self.emotion_checkbox_vars.values())
            if not selected_any_emotion:
                messagebox.showwarning("Input Error", "Please select at least one emotion and its intensity.")
                return False
            for emotion, vars_dict in self.selected_emotions.items():
                if self.emotion_checkbox_vars[emotion].get() and vars_dict['initial_var'].get() == 0:
                    messagebox.showwarning("Input Error", f"Please rate the initial intensity for '{emotion}'.")
                    return False

        elif step_index == 1: # Step 2: Automatic Thoughts
            if not self.automatic_thoughts_text.get("1.0", tk.END).strip():
                messagebox.showwarning("Input Error", "Please describe your automatic thoughts.")
                return False
            if self.belief_auto_scale_var.get() == 0:
                 messagebox.showwarning("Input Error", "Please rate your belief in automatic thoughts.")
                 return False

        elif step_index == 2: # Step 3: Evidence
            # Evidence fields are optional, so no mandatory validation
            pass

        elif step_index == 3: # Step 4: Alternative Thought & Outcome
            if not self.alternative_thought_text.get("1.0", tk.END).strip():
                messagebox.showwarning("Input Error", "Please provide an alternative/balanced thought.")
                return False
            if self.belief_alt_scale_var.get() == 0:
                 messagebox.showwarning("Input Error", "Please rate your belief in the alternative thought.")
                 return False
            # Check if re-rated emotions were set to 0 if they were selected in step 1
            for emotion, vars_dict in self.selected_emotions.items():
                if self.emotion_checkbox_vars[emotion].get() and vars_dict['final_var'].get() == 0:
                    messagebox.showwarning("Input Error", f"Please re-rate the intensity for '{emotion}' in the final emotions section.")
                    return False

        return True

    def _collect_data_for_step(self, step_index):
        if step_index == 0: # Step 1
            self.record_data["Date"] = self.date_entry.get_date().isoformat()
            self.record_data["Situation"] = self.situation_text.get("1.0", tk.END).strip()
            
            initial_emotions = {}
            for emotion, vars_dict in self.selected_emotions.items():
                if self.emotion_checkbox_vars[emotion].get():
                    initial_emotions[emotion] = vars_dict['initial_var'].get()
            self.record_data["Initial Emotions"] = initial_emotions

        elif step_index == 1: # Step 2
            self.record_data["Automatic Thoughts"] = self.automatic_thoughts_text.get("1.0", tk.END).strip()
            self.record_data["Belief in Automatic Thoughts"] = self.belief_auto_scale_var.get()

        elif step_index == 2: # Step 3
            self.record_data["Evidence For"] = self.evidence_for_text.get("1.0", tk.END).strip()
            self.record_data["Evidence Against"] = self.evidence_against_text.get("1.0", tk.END).strip()

        elif step_index == 3: # Step 4
            self.record_data["Alternative Thought"] = self.alternative_thought_text.get("1.0", tk.END).strip()
            self.record_data["Belief in Alternative Thought"] = self.belief_alt_scale_var.get()
            
            final_emotions = {}
            for emotion, vars_dict in self.selected_emotions.items():
                if self.emotion_checkbox_vars[emotion].get():
                    final_emotions[emotion] = vars_dict['final_var'].get()
            self.record_data["Final Emotions"] = final_emotions


    def _save_record(self):
        if self._validate_step(self.total_steps - 1): # Validate the last step before saving
            self._collect_data_for_step(self.total_steps - 1) # Collect data from the last step

            self.data_manager.add_thought_record(self.record_data)
            messagebox.showinfo("Success", "Thought Record saved successfully!")
            self._clear_form() # Reset the form
            self.controller.show_frame("ProgressPage") # Go to progress page to see the new record

    def _clear_form(self):
        self.date_entry.set_date(datetime.date.today())
        self.situation_text.delete("1.0", tk.END)
        self.automatic_thoughts_text.delete("1.0", tk.END)
        self.evidence_for_text.delete("1.0", tk.END)
        self.evidence_against_text.delete("1.0", tk.END)
        self.alternative_thought_text.delete("1.0", tk.END)

        self.belief_auto_scale_var.set(0)
        self.belief_auto_label.config(text="0%")
        self.belief_alt_scale_var.set(0)
        self.belief_alt_label.config(text="0%")

        # Clear emotion selections and reset sliders
        for emotion in self.emotion_checkbox_vars:
            self.emotion_checkbox_vars[emotion].set(False)
            self.selected_emotions[emotion]['initial_var'].set(0)
            self.selected_emotions[emotion]['final_var'].set(0)
            self.emotion_intensity_scales[emotion].config(state='disabled')
            self.emotion_intensity_labels[emotion].config(text="0%")
        
        # Clear the final emotion container
        for widget in self.final_emotion_container.winfo_children():
            widget.destroy()

        self.record_data = {} # Clear stored data
        self.current_step = 0
        self._show_step(self.current_step) # Go back to the first step

    def load_data(self, initial_data=None, record_timestamp=None):
        """
        Loads activity data into the form for editing.
        Note: Implementing edit mode for a multi-step form is more complex
        as you'd need to populate all steps. For now, this just clears the form
        if called without data, or can be extended for edit mode later.
        """
        if initial_data:
            messagebox.showinfo("Feature Not Implemented", "Editing multi-step Thought Records is not yet fully supported.")
            # For a full implementation, you would populate all fields from initial_data
            # and potentially navigate to the step where editing makes most sense,
            # or allow going through steps to review/modify.
            # For now, just load the basic fields and keep the sequential flow.
            
            # Example (simplified):
            self.record_data = initial_data
            self.date_entry.set_date(datetime.datetime.fromisoformat(initial_data.get("Date", datetime.date.today().isoformat())).date())
            self.situation_text.delete("1.0", tk.END)
            self.situation_text.insert("1.0", initial_data.get("Situation", ""))
            
            # Populate other fields as well
            self.automatic_thoughts_text.delete("1.0", tk.END)
            self.automatic_thoughts_text.insert("1.0", initial_data.get("Automatic Thoughts", ""))
            self.belief_auto_scale_var.set(initial_data.get("Belief in Automatic Thoughts", 0))
            self.belief_auto_label.config(text=f"{initial_data.get('Belief in Automatic Thoughts', 0)}%")
            
            self.evidence_for_text.delete("1.0", tk.END)
            self.evidence_for_text.insert("1.0", initial_data.get("Evidence For", ""))
            self.evidence_against_text.delete("1.0", tk.END)
            self.evidence_against_text.insert("1.0", initial_data.get("Evidence Against", ""))

            self.alternative_thought_text.delete("1.0", tk.END)
            self.alternative_thought_text.insert("1.0", initial_data.get("Alternative Thought", ""))
            self.belief_alt_scale_var.set(initial_data.get("Belief in Alternative Thought", 0))
            self.belief_alt_label.config(text=f"{initial_data.get('Belief in Alternative Thought', 0)}%")
            
            # For emotions, this is more complex as you need to set checkboxes and scale values
            initial_emotions_data = initial_data.get("Initial Emotions", {})
            final_emotions_data = initial_data.get("Final Emotions", {})
            for emotion, initial_var_dict in self.selected_emotions.items():
                if emotion in initial_emotions_data:
                    self.emotion_checkbox_vars[emotion].set(True)
                    initial_var_dict['initial_var'].set(initial_emotions_data[emotion])
                    self._toggle_emotion_intensity_scale(emotion) # Enable and set label
                if emotion in final_emotions_data:
                    initial_var_dict['final_var'].set(final_emotions_data[emotion])

            self.record_timestamp = record_timestamp # Store for update operation
            # You would need to change the submit button to "Update" and modify _save_record logic
            # to call update_thought_record instead of add_thought_record.
            # For a multi-step edit, you might want to show the first step and let the user navigate.
            self.current_step = 0
            self._show_step(self.current_step)
            # End of simplified example
            
        else:
            self.record_timestamp = None
            self._clear_form() # Reset to new record mode

    def refresh_page(self):
        """Called by app.py when navigating to this page (for new record)."""
        self._clear_form() # Ensure form is clean for a new entry