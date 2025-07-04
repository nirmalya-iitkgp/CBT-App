# relaxation_page.py

import tkinter as tk
from tkinter import ttk, messagebox
import time

class RelaxationPage(ttk.Frame):
    def __init__(self, parent, controller): # No DataManager needed directly for this page
        super().__init__(parent)
        self.controller = controller

        self.is_breathing_active = False
        self.breathe_animation_id = None
        self.countdown_id = None
        self.current_countdown_time = 0
        self.total_breathing_duration = 120 # Default to 2 minutes (120 seconds)

        self.grid_rowconfigure(0, weight=0) # Title
        self.grid_rowconfigure(1, weight=1) # Main content area for breathing exercise
        self.grid_columnconfigure(0, weight=1)

        ttk.Label(self, text="Relaxation Exercises", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        # Main content frame for the exercise
        exercise_frame = ttk.Frame(self, padding="20")
        exercise_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        exercise_frame.grid_rowconfigure(0, weight=1) # Canvas
        exercise_frame.grid_rowconfigure(1, weight=0) # Instructions
        exercise_frame.grid_rowconfigure(2, weight=0) # Controls
        exercise_frame.grid_columnconfigure(0, weight=1)

        # --- Breathing Visual (Canvas) ---
        self.canvas = tk.Canvas(exercise_frame, bg="#E0F2F7", highlightbackground="#B2EBF2", highlightthickness=2)
        self.canvas.grid(row=0, column=0, sticky="nsew", pady=10)

        # Breathing circle (initial size, will be animated)
        self.circle_radius = 50
        self.center_x = 0
        self.center_y = 0
        self.breathing_circle = None
        self.canvas.bind("<Configure>", self._recenter_circle) # Recenter on resize

        # Text on canvas
        self.breathe_text = self.canvas.create_text(0, 0, text="Press Start", font=("Helvetica", 24, "bold"), fill="darkblue")
        self.canvas.tag_raise(self.breathe_text) # Ensure text is above circle

        # --- Instructions ---
        instructions_text = """
        **Deep Breathing Exercise**

        1.  **Inhale:** Slowly breathe in through your nose for 4 counts, allowing your belly to rise.
        2.  **Hold:** Hold your breath for 7 counts.
        3.  **Exhale:** Slowly exhale through your mouth for 8 counts, emptying your lungs completely.

        Follow the expanding and contracting circle.
        """
        ttk.Label(exercise_frame, text=instructions_text, wraplength=600, justify="left",
                  font=("Helvetica", 10), anchor="w").grid(row=1, column=0, pady=10, sticky="ew")

        # --- Controls Frame ---
        controls_frame = ttk.Frame(exercise_frame)
        controls_frame.grid(row=2, column=0, pady=10)
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        controls_frame.grid_columnconfigure(2, weight=1)
        controls_frame.grid_columnconfigure(3, weight=1)

        self.start_button = ttk.Button(controls_frame, text="Start Breathing", command=self._start_breathing_exercise)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(controls_frame, text="Stop Breathing", command=self._stop_breathing_exercise, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)

        ttk.Label(controls_frame, text="Duration (min):").grid(row=0, column=2, padx=(20, 5), sticky="e")
        self.duration_spinbox = ttk.Spinbox(controls_frame, from_=1, to=10, width=5, justify="center",
                                            command=self._update_duration)
        self.duration_spinbox.set(str(self.total_breathing_duration // 60)) # Set default to 2 minutes
        self.duration_spinbox.grid(row=0, column=3, padx=5, sticky="w")
        
        self.countdown_label = ttk.Label(controls_frame, text=f"Time Left: {self.total_breathing_duration // 60:02d}:00", font=("Helvetica", 12, "bold"))
        self.countdown_label.grid(row=1, column=0, columnspan=4, pady=10)


    def _recenter_circle(self, event=None):
        """Recalculate circle position and draw/reposition it."""
        self.center_x = self.canvas.winfo_width() / 2
        self.center_y = self.canvas.winfo_height() / 2
        
        if self.breathing_circle:
            self.canvas.coords(self.breathing_circle,
                               self.center_x - self.circle_radius, self.center_y - self.circle_radius,
                               self.center_x + self.circle_radius, self.center_y + self.circle_radius)
        else:
            self.breathing_circle = self.canvas.create_oval(
                self.center_x - self.circle_radius, self.center_y - self.circle_radius,
                self.center_x + self.circle_radius, self.center_y + self.circle_radius,
                fill="#ADD8E6", outline="#6495ED", width=2
            )
        self.canvas.coords(self.breathe_text, self.center_x, self.center_y)
        self.canvas.tag_raise(self.breathe_text) # Ensure text is always on top

    def _update_duration(self):
        try:
            minutes = int(self.duration_spinbox.get())
            if 1 <= minutes <= 10:
                self.total_breathing_duration = minutes * 60
                self.countdown_label.config(text=f"Time Left: {minutes:02d}:00")
            else:
                self.duration_spinbox.set("2") # Reset if invalid input
                messagebox.showerror("Invalid Input", "Duration must be between 1 and 10 minutes.")
        except ValueError:
            self.duration_spinbox.set("2") # Reset if non-numeric
            messagebox.showerror("Invalid Input", "Please enter a valid number for duration.")

    def _start_breathing_exercise(self):
        if self.is_breathing_active:
            return

        self.is_breathing_active = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.duration_spinbox.config(state="disabled")

        self.current_countdown_time = self.total_breathing_duration
        self._run_countdown()
        self._animate_breathing_cycle("inhale", 0)

    def _stop_breathing_exercise(self):
        self.is_breathing_active = False
        if self.breathe_animation_id:
            self.after_cancel(self.breathe_animation_id)
            self.breathe_animation_id = None
        if self.countdown_id:
            self.after_cancel(self.countdown_id)
            self.countdown_id = None
        
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.duration_spinbox.config(state="normal")
        # --- FIX: Use itemconfig for canvas items ---
        self.canvas.itemconfig(self.breathe_text, text="Press Start", fill="darkblue")
        # --- END FIX ---
        self._reset_circle_size()
        self.countdown_label.config(text=f"Time Left: {self.total_breathing_duration // 60:02d}:00")
        messagebox.showinfo("Exercise Stopped", "Breathing exercise stopped.")

    def _reset_circle_size(self):
        self.canvas.delete(self.breathing_circle) # Delete and recreate to ensure size reset
        self.breathing_circle = self.canvas.create_oval(
            self.center_x - 50, self.center_y - 50,
            self.center_x + 50, self.center_y + 50,
            fill="#ADD8E6", outline="#6495ED", width=2
        )
        self.canvas.tag_raise(self.breathe_text) # Ensure text is always on top

    def _run_countdown(self):
        if not self.is_breathing_active or self.current_countdown_time <= 0:
            self._stop_breathing_exercise()
            self.countdown_label.config(text="Time's Up!")
            messagebox.showinfo("Exercise Complete", "The breathing exercise has concluded. Well done!")
            return

        minutes = self.current_countdown_time // 60
        seconds = self.current_countdown_time % 60
        self.countdown_label.config(text=f"Time Left: {minutes:02d}:{seconds:02d}")
        self.current_countdown_time -= 1
        self.countdown_id = self.after(1000, self._run_countdown)

    def _animate_breathing_cycle(self, phase, step):
        if not self.is_breathing_active:
            return

        min_radius = 50
        max_radius = 150 # Max size for the circle
        animation_steps = {
            "inhale": 4 * 20, # 4 seconds, 20 steps per second (50ms delay)
            "hold_in": 7 * 20, # 7 seconds
            "exhale": 8 * 20, # 8 seconds
            "hold_out": 1 * 20 # 1 second pause between cycles
        }
        
        if phase == "inhale":
            # --- FIX: Use itemconfig for canvas items ---
            self.canvas.itemconfig(self.breathe_text, text="Breathe In...", fill="green")
            # --- END FIX ---
            radius = min_radius + (max_radius - min_radius) * (step / animation_steps["inhale"])
            if step < animation_steps["inhale"]:
                next_phase = "inhale"
                next_step = step + 1
            else:
                next_phase = "hold_in"
                next_step = 0
        elif phase == "hold_in":
            # --- FIX: Use itemconfig for canvas items ---
            self.canvas.itemconfig(self.breathe_text, text="Hold", fill="blue")
            # --- END FIX ---
            radius = max_radius # Stay at max size
            if step < animation_steps["hold_in"]:
                next_phase = "hold_in"
                next_step = step + 1
            else:
                next_phase = "exhale"
                next_step = 0
        elif phase == "exhale":
            # --- FIX: Use itemconfig for canvas items ---
            self.canvas.itemconfig(self.breathe_text, text="Breathe Out...", fill="red")
            # --- END FIX ---
            radius = max_radius - (max_radius - min_radius) * (step / animation_steps["exhale"])
            if step < animation_steps["exhale"]:
                next_phase = "exhale"
                next_step = step + 1
            else:
                next_phase = "hold_out"
                next_step = 0
        elif phase == "hold_out":
            # --- FIX: Use itemconfig for canvas items ---
            self.canvas.itemconfig(self.breathe_text, text="Pause", fill="darkgray")
            # --- END FIX ---
            radius = min_radius # Stay at min size
            if step < animation_steps["hold_out"]:
                next_phase = "hold_out"
                next_step = step + 1
            else:
                next_phase = "inhale" # Cycle back
                next_step = 0
        
        self.canvas.coords(self.breathing_circle,
                           self.center_x - radius, self.center_y - radius,
                           self.center_x + radius, self.center_y + radius)
        
        self.breathe_animation_id = self.after(50, self._animate_breathing_cycle, next_phase, next_step) # 50ms = 20 frames/sec