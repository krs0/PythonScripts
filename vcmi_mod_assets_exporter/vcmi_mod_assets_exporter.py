"""
VCMI Mod Assets Exporter

This simple GUI extracts only! assets (.def, .png, etc) from a specified VCMI mod folder to a designated destination folder. It maintains the mods folder structure.

Features:
- Loads the source and destination paths from a configuration file (`settings.ini`).
- If destination path is empty, it will extract assets in an `out` folder created in the current folder
- Excludes specific files and folders from being copied, like:
  - Configuration directories (e.g., 'config')
  - JSON files
  - Documentation files (e.g., 'README.md', 'LICENSE')

Output:
The extracted assets will be saved to the specified output folder.
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import configparser

CONFIG_FILE = "settings.ini"

def load_config():
    """Load the source path and output path from the settings.ini file."""
    config = configparser.ConfigParser()
    
    # Set defaults
    source_path = ""
    output_path = os.path.join(os.getcwd(), "out")  # Default output path
    
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        source_path = config.get('Paths', 'vcmi_mod_folder', fallback="")
        # Check if output_folder exists in the config
        if config.has_option('Paths', 'output_folder'):
            output_path = config.get('Paths', 'output_folder')
    
    return source_path, output_path

def save_config(source_path, output_path):
    """Save the source path and output path to the settings.ini file."""
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['Paths'] = {}
    
    # Read existing configuration to update
    config.read(CONFIG_FILE)
    config['Paths']['vcmi_mod_folder'] = source_path
    config['Paths']['output_folder'] = output_path  # Save the output folder path

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def copy_files(src, dest):
    """Copy files from source to destination while excluding certain files and folders."""
    excluded_items = ["config", ".json", ".git", ".gitignore", "README.md", "LICENSE"]
    for root, dirs, files in os.walk(src):
        # Exclude specified items
        files = [f for f in files if not any(f.lower() == item.lower() or f.lower().endswith(".json") for item in excluded_items)]
        # Exclude specified folders
        dirs[:] = [d for d in dirs if d not in excluded_items]

        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(dest, os.path.relpath(src_path, src))

            # Ensure destination folder exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            shutil.copy2(src_path, dest_path)

def browse_source_path():
    """Open a dialog to select the source directory."""
    source_path = filedialog.askdirectory(initialdir=source_path_var.get())
    if source_path:  # Only update if a valid directory is selected
        source_path_var.set(source_path)
        source_path_entry.delete(0, tk.END)
        source_path_entry.insert(0, source_path)

def browse_output_path():
    """Open a dialog to select the output directory."""
    output_path = filedialog.askdirectory(initialdir=output_path_var.get())
    if output_path:  # Only update if a valid directory is selected
        output_path_var.set(output_path)
        output_path_entry.delete(0, tk.END)
        output_path_entry.insert(0, output_path)

def start_asset_extraction():
    """Initiate the file copying process after checking if the destination folder is empty."""
    source_path = source_path_var.get()
    output_path = output_path_var.get()
    
    # Save the selected source path and output path to settings.ini
    save_config(source_path, output_path)
    
    # Check if the output folder is not empty
    if os.path.exists(output_path) and os.listdir(output_path):
        messagebox.showwarning("Warning", f"The destination folder is not empty: {output_path}. No files will be copied.")
        return  # Exit the function if the destination folder is not empty
    
    # Proceed with the file copying if the output folder is empty
    copy_files(source_path, output_path)
    messagebox.showinfo("Extraction Complete", f"Mod assets copied successfully to: {output_path}")

# Create the main window
window = tk.Tk()
window.title("VCMI Mod Assets Extraction")

# StringVars to store last selected paths
source_path_var = tk.StringVar()
output_path_var = tk.StringVar()

# Load last selected paths from the config file
last_source_path, last_output_path = load_config()
source_path_var.set(last_source_path)
output_path_var.set(last_output_path)  # Set output path from config or default

# Create and place widgets
source_path_label = tk.Label(window, text="VCMI mod folder:")
source_path_label.grid(row=0, column=0, padx=5, pady=5)

source_path_entry = tk.Entry(window, width=50, textvariable=source_path_var)
source_path_entry.grid(row=0, column=1, padx=5, pady=5)

browse_source_button = tk.Button(window, text="Browse", command=browse_source_path)
browse_source_button.grid(row=0, column=2, padx=5, pady=5)

output_path_label = tk.Label(window, text="Output Folder:")
output_path_label.grid(row=1, column=0, padx=5, pady=5)

output_path_entry = tk.Entry(window, width=50, textvariable=output_path_var)
output_path_entry.grid(row=1, column=1, padx=5, pady=5)

browse_output_button = tk.Button(window, text="Browse", command=browse_output_path)
browse_output_button.grid(row=1, column=2, padx=5, pady=5)

start_extraction_button = tk.Button(window, text="Start extraction", command=start_asset_extraction)
start_extraction_button.grid(row=2, column=1, pady=10)

# Start the main loop
window.mainloop()
