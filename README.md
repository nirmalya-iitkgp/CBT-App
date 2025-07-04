# MindSync: Your Self-Guided CBT Companion (Tkinter App)

## Project Overview

MindSync is a desktop application designed to provide tools and exercises based on Cognitive Behavioral Therapy (CBT) principles. It aims to empower users to track their thoughts, engage in behavioral activation, practice relaxation techniques, utilize structured problem-solving, and monitor their personal progress. Built with Python's Tkinter framework, it offers a user-friendly interface enhanced with `ttkthemes` for a modern look.

## Features

* **Learn CBT Principles:** Access structured lessons and quizzes on core CBT concepts.
* **Thought Record:** A dedicated section to log and analyze dysfunctional thought patterns using the CBT thought record model.
* **Behavioral Activation:** Plan, log, and review engaging activities to boost pleasure and mastery.
* **Relaxation Techniques:** A guided breathing exercise with visual cues and a timer to help manage anxiety and stress.
* **Problem Solving:** A structured, multi-step worksheet to break down problems, brainstorm solutions, and develop action plans.
* **Progress Tracking:** Visualize your journey and improvements over time, with logs and charts for behavioral activities, thought records, and problem-solving entries.
* **Local Data Storage:** All user data is securely stored locally in JSON files for privacy and accessibility.
* **Modern UI:** Utilizes `ttkthemes` to provide a clean and modern aesthetic to the Tkinter interface.

## Technologies Used

* **Python:** The core programming language.
* **Tkinter:** Python's standard GUI (Graphical User Interface) library.
* **`ttkthemes`:** For enhancing the visual appearance of Tkinter widgets with modern themes.
* **`tkcalendar`:** For easy date selection in forms.
* **`matplotlib` & `pandas`:** For creating interactive plots and handling data for progress visualization.
* **JSON:** For efficient local storage and retrieval of user data.
* **`datetime` & `uuid`:** Python's built-in modules for timestamping and generating unique identifiers for records.

## Installation & Setup

To run this application locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/MindSyncCBT.git](https://github.com/your-username/MindSyncCBT.git)
    cd MindSyncCBT
    ```
    (Replace `your-username/MindSyncCBT` with your actual GitHub repository path if different)

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

After installing the dependencies, you can launch the app:

```bash
python app.py
