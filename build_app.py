# build_app.py

import PyInstaller.__main__
import os
import sys
import site

def get_ttkthemes_data_path():
    """
    Dynamically finds the path to the ttkthemes 'themes' directory
    for PyInstaller's --add-data flag.
    """
    try:
        import ttkthemes
        # Get the directory where the ttkthemes package is installed
        ttkthemes_package_path = os.path.dirname(ttkthemes.__file__)
        themes_dir_in_package = os.path.join(ttkthemes_package_path, "themes")

        if os.path.exists(themes_dir_in_package):
            # PyInstaller --add-data format: "SOURCE;DESTINATION" (Windows) or "SOURCE:DESTINATION" (Linux/macOS)
            # DESTINATION should be 'ttkthemes/themes' so the bundled app finds it correctly.
            if sys.platform.startswith('win'):
                return f"{themes_dir_in_package};ttkthemes/themes"
            else: # Linux or macOS
                return f"{themes_dir_in_package}:ttkthemes/themes"
        else:
            print("Warning: 'themes' directory not found inside ttkthemes package. Themed look might fail.")
            return None
    except ImportError:
        print("Error: 'ttkthemes' library not found. Please install it: 'pip install ttkthemes'")
        sys.exit(1) # Exit if ttkthemes is not installed

if __name__ == "__main__":
    # Get the path for ttkthemes data
    ttk_data_path_arg = get_ttkthemes_data_path()
    if not ttk_data_path_arg:
        print("Failed to determine ttkthemes path. Packaging aborted.")
        sys.exit(1)

    # --- PyInstaller Command Configuration ---
    # These are the arguments passed to PyInstaller
    pyinstaller_args = [
        'app.py',             # Your main application file
        '--onefile',          # Create a single executable file
        '--windowed',         # Suppress the console window (for GUI apps)
                              # You can use '--noconsole' as an alternative.
        '--name=MindSyncCBT', # Name of your executable file (e.g., MindSyncCBT.exe)
        '--add-data', ttk_data_path_arg, # Add the ttkthemes data files

        # --- Optional: Add an icon ---
        # If you have an icon file (e.g., 'app_icon.ico' for Windows, 'app_icon.icns' for macOS)
        # Place it in your project's root directory and uncomment the line below:
        # '--icon=app_icon.ico', # Example: For Windows. Use .icns for macOS.

        # --- Optional: Add other data files ---
        # If you have a pre-filled database file (e.g., 'cbt_data.db')
        # that needs to be included in the executable, uncomment and adjust:
        # '--add-data', 'cbt_data.db' + os.pathsep + '.', # Adds cbt_data.db to the root of the bundled app
                                                        # The '.' means "put it in the root of the extracted bundle"
    ]

    print(f"Starting PyInstaller build for MindSyncCBT...")
    print(f"Command: pyinstaller {' '.join(pyinstaller_args)}")

    # Run PyInstaller
    PyInstaller.__main__.run(pyinstaller_args)

    print("\n--- Packaging Complete! ---")
    print("Your executable can be found in the 'dist' folder.")
    print("The 'build' folder contains temporary files and can be deleted.")