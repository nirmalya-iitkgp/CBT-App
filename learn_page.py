# learn_page.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
from cbt_content import content_data # Import content data for lessons and quizzes

class LearnPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure grid for the LearnPage frame
        self.grid_rowconfigure(0, weight=1) # Row for the notebook to expand and take available space
        self.grid_columnconfigure(0, weight=1)

        # Place the Notebook at the very top, expanding to fill the space
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Placed at row 0, expands

        self.lesson_frames = {}
        for lesson_title, lesson_content in content_data.items():
            lesson_frame = ttk.Frame(self.notebook)
            self.notebook.add(lesson_frame, text=lesson_title)
            self.lesson_frames[lesson_title] = lesson_frame
            self._setup_lesson_content(lesson_frame, lesson_content)

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
        self.current_lesson_quiz_attempts = {}

        # Initial selection (optional, but good for user experience)
        if content_data:
            first_lesson_title = list(content_data.keys())[0]
            self.notebook.select(0) # Select the first tab
            # Call _load_quiz_for_lesson after the frame has been properly gridded
            # Adding a small delay to ensure geometry managers are settled
            # This 'after' call is crucial for geometry managers to initialize
            self.after(100, lambda: self._load_quiz_for_lesson(first_lesson_title))


    def _setup_lesson_content(self, frame, lesson_content):
        # Configure grid for individual lesson frames
        frame.grid_rowconfigure(0, weight=0) # For lesson title within tab
        frame.grid_rowconfigure(1, weight=1) # For scrolled text
        frame.grid_rowconfigure(2, weight=0) # For quiz section
        frame.grid_columnconfigure(0, weight=1)

        # Lesson Title within the tab (optional, as tab text is already title)
        ttk.Label(frame, text=lesson_content.get("title", self.notebook.tab(frame, "text")),
                  font=("Helvetica", 14, "bold")).grid(row=0, column=0, pady=5, sticky="ew")

        # Scrolled Text for lesson content
        lesson_text_area = scrolledtext.ScrolledText(frame, wrap="word", font=("Helvetica", 10), padx=10, pady=10)
        lesson_text_area.insert(tk.END, lesson_content["text"])
        lesson_text_area.config(state="disabled") # Make it read-only
        lesson_text_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # Quiz Section Frame
        quiz_frame = ttk.LabelFrame(frame, text="Quiz Time!", padding="10")
        # DO NOT GRID IT HERE INITIALLY. It will be gridded by _load_quiz_for_lesson
        # to ensure it's shown/hidden properly using grid.
        quiz_frame.grid_columnconfigure(0, weight=1) # This sets up its internal grid config

        # Elements for the quiz - these will still use pack inside quiz_frame
        # It's okay for children of quiz_frame to use pack, as quiz_frame is their parent.
        # The error was about quiz_frame itself being packed/gridded by its parent.
        quiz_question_label = ttk.Label(quiz_frame, text="", wraplength=500, font=("Helvetica", 10, "italic"))
        quiz_question_label.pack(pady=5)

        quiz_options_vars = []
        quiz_option_buttons = []
        for i in range(4): # Assuming max 4 options per question
            var = tk.StringVar()
            rb = ttk.Radiobutton(quiz_frame, text="", variable=var, value="")
            quiz_options_vars.append(var)
            quiz_option_buttons.append(rb)
            rb.pack(anchor="w", padx=10)

        quiz_feedback_label = ttk.Label(quiz_frame, text="", font=("Helvetica", 10))
        quiz_feedback_label.pack(pady=5)

        submit_quiz_button = ttk.Button(quiz_frame, text="Submit Answer", command=self._check_answer)
        submit_quiz_button.pack(pady=10)

        # Store quiz elements with their respective frame
        lesson_content["quiz_widgets"] = {
            "question_label": quiz_question_label,
            "options_vars": quiz_options_vars,
            "option_buttons": quiz_option_buttons,
            "feedback_label": quiz_feedback_label,
            "submit_button": submit_quiz_button,
            "quiz_frame": quiz_frame # Store the frame itself for visibility toggling
        }

    def _on_tab_change(self, event):
        selected_tab_id = self.notebook.select()
        selected_lesson_title = self.notebook.tab(selected_tab_id, "text")
        self._load_quiz_for_lesson(selected_lesson_title)

    def _load_quiz_for_lesson(self, lesson_title):
        lesson_data = content_data.get(lesson_title)
        if not lesson_data:
            return

        quiz_widgets = lesson_data.get("quiz_widgets")
        if not quiz_widgets: # No quiz widgets prepared for this lesson
            return

        quiz_frame = quiz_widgets["quiz_frame"]
        quiz_questions = lesson_data.get("quiz")

        if not quiz_questions: # If no quiz for this lesson
            quiz_frame.grid_forget() # <--- CORRECT: Use grid_forget() for visibility
            return

        # Ensure quiz frame is gridded if it was hidden
        # winfo_manager() returns 'grid', 'pack', 'place', or '' if not managed
        if quiz_frame.winfo_manager() != "grid":
            # Reposition it correctly in its parent 'frame' (the lesson tab frame)
            # <--- CORRECT: Use grid() for visibility. The row/column must match _setup_lesson_content intended layout.
            quiz_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # Track current question for the lesson
        if lesson_title not in self.current_lesson_quiz_attempts:
            self.current_lesson_quiz_attempts[lesson_title] = {
                "question_index": 0,
                "completed": False
            }

        current_attempt = self.current_lesson_quiz_attempts[lesson_title]
        q_idx = current_attempt["question_index"]

        if current_attempt["completed"] or q_idx >= len(quiz_questions):
            quiz_widgets["question_label"].config(text="You've completed the quiz for this lesson!", foreground="green")
            for rb in quiz_widgets["option_buttons"]:
                rb.pack_forget()
            quiz_widgets["submit_button"].pack_forget()
            quiz_widgets["feedback_label"].config(text="")
            return

        question_data = quiz_questions[q_idx]
        quiz_widgets["question_label"].config(text=f"Question {q_idx + 1}: {question_data['question']}", foreground="black")
        quiz_widgets["feedback_label"].config(text="", foreground="black") # Clear previous feedback
        quiz_widgets["submit_button"].pack(pady=10) # Ensure button is visible

        # Shuffle options to prevent memorization by position
        options_with_answer = [{"option": opt, "is_correct": (opt == question_data['answer'])} for opt in question_data['options']]
        random.shuffle(options_with_answer)

        for i, (rb, var) in enumerate(zip(quiz_widgets["option_buttons"], quiz_widgets["options_vars"])):
            if i < len(options_with_answer):
                option_text = options_with_answer[i]["option"]
                var.set("") # Clear previous selection
                rb.config(text=option_text, value=option_text)
                rb.pack(anchor="w", padx=10) # Ensure button is visible
            else:
                rb.pack_forget() # Hide unused radio buttons

        # Store the correct answer for checking
        current_attempt["correct_answer"] = next(opt["option"] for opt in options_with_answer if opt["is_correct"])


    def _check_answer(self):
        selected_tab_id = self.notebook.select()
        selected_lesson_title = self.notebook.tab(selected_tab_id, "text")
        current_attempt = self.current_lesson_quiz_attempts.get(selected_lesson_title)

        if not current_attempt or current_attempt["completed"]:
            return

        quiz_widgets = content_data[selected_lesson_title]["quiz_widgets"]
        selected_option = ""
        for var in quiz_widgets["options_vars"]:
            if var.get(): # Check which radio button is selected
                selected_option = var.get()
                break
        
        if not selected_option:
            quiz_widgets["feedback_label"].config(text="Please select an answer.", foreground="orange")
            return

        correct_answer = current_attempt["correct_answer"]

        if selected_option == correct_answer:
            quiz_widgets["feedback_label"].config(text="Correct! Well done.", foreground="green")
            current_attempt["question_index"] += 1
            if current_attempt["question_index"] >= len(content_data[selected_lesson_title]["quiz"]):
                current_attempt["completed"] = True
                quiz_widgets["submit_button"].pack_forget()
                quiz_widgets["question_label"].config(text="You've completed the quiz for this lesson!", foreground="green")
                for rb in quiz_widgets["option_buttons"]:
                    rb.pack_forget()
            else:
                # Load next question after a short delay
                self.after(1000, lambda: self._load_quiz_for_lesson(selected_lesson_title))
        else:
            quiz_widgets["feedback_label"].config(text=f"Incorrect. The correct answer was: {correct_answer}", foreground="red")