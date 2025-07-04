# data_manager.py

import json
import os
import datetime

class DataManager:
    """
    Manages loading, saving, updating, and deleting of all application data
    (thought records, behavioral activation, problem solving).
    Ensures data consistency and handles file operations.
    Each record will have a 'creation_timestamp' for unique identification, especially for editing/deleting.
    """
    def __init__(self, base_dir="data"): # Use base_dir argument for flexibility
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

        # Define the file paths for each type of record as instance variables
        self.thought_records_file = os.path.join(self.base_dir, "thought_records.json")
        self.behavioral_activation_file = os.path.join(self.base_dir, "behavioral_activation_activities.json")
        self.problem_solving_records_file = os.path.join(self.base_dir, "problem_solving_records.json")

        # Initialize empty JSON files if they don't exist or are empty
        self._initialize_file(self.thought_records_file)
        self._initialize_file(self.behavioral_activation_file)
        self._initialize_file(self.problem_solving_records_file)

    def _initialize_file(self, file_path):
        """Ensures a JSON file exists and is initialized as an empty list if not."""
        if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
            with open(file_path, 'w') as f:
                json.dump([], f) # Initialize as an empty list for records

    def _load_data(self, filepath):
        """
        Internal helper method to load data from a given JSON file.
        Returns an empty list if the file does not exist or is empty/corrupt.
        """
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r') as f:
            try:
                # Attempt to load JSON data
                data = json.load(f)
                # If file is empty, json.load() might return None, ensure it's a list
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                # If JSON is malformed, return an empty list and print a warning
                print(f"Warning: {filepath} is empty or contains malformed JSON. Returning empty list and re-initializing.")
                self._save_data(filepath, []) # Attempt to fix by writing an empty list back
                return []
            except Exception as e:
                # Catch any other potential errors during file reading
                print(f"Error loading {filepath}: {e}. Returning empty list.")
                return []

    def _save_data(self, filepath, data):
        """
        Internal helper method to save data to a given JSON file.
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data to {filepath}: {e}")

    def _add_creation_timestamp(self, record_data):
        """Helper to add 'creation_timestamp' to a record if it's not already present."""
        if "creation_timestamp" not in record_data:
            record_data["creation_timestamp"] = datetime.datetime.now().isoformat()
        return record_data

    def _update_record_by_timestamp(self, filepath, record_timestamp, updated_data):
        """
        Generic method to update a record in a JSON file by its 'creation_timestamp'.
        Returns True if successful, False otherwise.
        """
        records = self._load_data(filepath)
        found = False
        for i, record in enumerate(records):
            if record.get("creation_timestamp") == record_timestamp:
                # Ensure the updated_data retains the original creation_timestamp
                # as it's the key identifier for the record.
                updated_data["creation_timestamp"] = record_timestamp
                records[i] = updated_data
                found = True
                break
        if found:
            self._save_data(filepath, records)
            return True
        return False

    def _delete_record_by_timestamp(self, filepath, record_timestamp):
        """
        Generic method to delete a record from a JSON file by its 'creation_timestamp'.
        Returns True if successful, False otherwise.
        """
        records = self._load_data(filepath)
        initial_len = len(records)
        records = [record for record in records if record.get("creation_timestamp") != record_timestamp]
        if len(records) < initial_len:
            self._save_data(filepath, records)
            return True
        return False


    # --- Behavioral Activation Management ---
    def add_behavioral_activation_activity(self, activity_data):
        """Adds a new behavioral activation activity to the collection."""
        activity_data = self._add_creation_timestamp(activity_data) # Add timestamp
        activities = self.get_all_behavioral_activation_activities()
        activities.append(activity_data)
        self._save_data(self.behavioral_activation_file, activities)

    def get_all_behavioral_activation_activities(self):
        """Retrieves all stored behavioral activation activities."""
        return self._load_data(self.behavioral_activation_file)

    def get_behavioral_activation_activity(self, timestamp):
        """Retrieves a single behavioral activation activity by its creation_timestamp."""
        activities = self.get_all_behavioral_activation_activities()
        for activity in activities:
            if activity.get("creation_timestamp") == timestamp:
                return activity
        return None

    def update_behavioral_activation_activity(self, record_timestamp, updated_data):
        """Updates an existing behavioral activation activity."""
        return self._update_record_by_timestamp(self.behavioral_activation_file, record_timestamp, updated_data)

    def delete_behavioral_activation_activity(self, record_timestamp):
        """Deletes a behavioral activation activity."""
        return self._delete_record_by_timestamp(self.behavioral_activation_file, record_timestamp)


    # --- Thought Record Management ---
    def add_thought_record(self, record_data):
        """Adds a new thought record to the collection."""
        record_data = self._add_creation_timestamp(record_data) # Add timestamp
        records = self.get_all_thought_records() # Renamed method call
        records.append(record_data)
        self._save_data(self.thought_records_file, records)

    def get_all_thought_records(self): # Renamed this method
        """Retrieves all stored thought records."""
        return self._load_data(self.thought_records_file)

    def get_thought_record(self, timestamp): # NEW method for fetching single record
        """Retrieves a single thought record by its creation_timestamp."""
        records = self.get_all_thought_records()
        for record in records:
            if record.get("creation_timestamp") == timestamp:
                return record
        return None

    def update_thought_record(self, record_timestamp, updated_data):
        """Updates an existing thought record."""
        return self._update_record_by_timestamp(self.thought_records_file, record_timestamp, updated_data)

    def delete_thought_record(self, record_timestamp):
        """Deletes a thought record."""
        return self._delete_record_by_timestamp(self.thought_records_file, record_timestamp)


    # --- Problem Solving Management ---
    def add_problem_solving_record(self, record_data):
        """Adds a new problem solving record to the collection."""
        record_data = self._add_creation_timestamp(record_data) # Add timestamp
        records = self.get_all_problem_solving_records() # Renamed method call
        records.append(record_data)
        self._save_data(self.problem_solving_records_file, records)

    def get_all_problem_solving_records(self): # Renamed this method
        """Retrieves all stored problem solving records."""
        return self._load_data(self.problem_solving_records_file)

    def get_problem_solving_record(self, timestamp): # NEW method for fetching single record
        """Retrieves a single problem solving record by its creation_timestamp."""
        records = self.get_all_problem_solving_records()
        for record in records:
            if record.get("creation_timestamp") == timestamp:
                return record
        return None

    def update_problem_solving_record(self, record_timestamp, updated_data):
        """Updates an existing problem solving record."""
        return self._update_record_by_timestamp(self.problem_solving_records_file, record_timestamp, updated_data)

    def delete_problem_solving_record(self, record_timestamp):
        """Deletes a problem solving record."""
        return self._delete_record_by_timestamp(self.problem_solving_records_file, record_timestamp)