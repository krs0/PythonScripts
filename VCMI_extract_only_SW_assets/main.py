import os
import shutil
import tkinter as tk
from tkinter import filedialog

CONFIG_FILE = "config.txt"


def save_config(source_path, destination_path):
    with open(CONFIG_FILE, "w") as config_file:
        config_file.write(f"SourcePath={source_path}\n")
        config_file.write(f"DestinationPath={destination_path}\n")


def load_config():
    source_path = ""
    destination_path = ""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as config_file:
            for line in config_file:
                key, value = line.strip().split("=")
                if key == "SourcePath":
                    source_path = value
                elif key == "DestinationPath":
                    destination_path = value
    return source_path, destination_path


def copy_files(src, dest):
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
    source_path_entry.delete(0, tk.END)
    source_path = filedialog.askdirectory(initialdir=source_path_var.get())
    source_path_var.set(source_path)
    source_path_entry.insert(0, source_path)


def browse_destination_path():
    destination_path_entry.delete(0, tk.END)
    destination_path = filedialog.askdirectory(initialdir=destination_path_var.get())
    destination_path_var.set(destination_path)
    destination_path_entry.insert(0, destination_path)


def start_copy():
    source_path = source_path_var.get()
    destination_path = destination_path_var.get()
    copy_files(source_path, destination_path)
    tk.messagebox.showinfo("Copy Complete", "Files copied successfully!")
    save_config(source_path, destination_path)


# Create the main window
window = tk.Tk()
window.title("File Copy GUI")

# StringVars to store last selected paths
source_path_var = tk.StringVar()
destination_path_var = tk.StringVar()

# Load last selected paths from the config file
last_source_path, last_destination_path = load_config()
source_path_var.set(last_source_path)
destination_path_var.set(last_destination_path)

# Create and place widgets
source_path_label = tk.Label(window, text="Source Path:")
source_path_label.grid(row=0, column=0, padx=5, pady=5)

source_path_entry = tk.Entry(window, width=50, textvariable=source_path_var)
source_path_entry.grid(row=0, column=1, padx=5, pady=5)

browse_source_button = tk.Button(window, text="Browse", command=browse_source_path)
browse_source_button.grid(row=0, column=2, padx=5, pady=5)

destination_path_label = tk.Label(window, text="Destination Path:")
destination_path_label.grid(row=1, column=0, padx=5, pady=5)

destination_path_entry = tk.Entry(window, width=50, textvariable=destination_path_var)
destination_path_entry.grid(row=1, column=1, padx=5, pady=5)

browse_destination_button = tk.Button(window, text="Browse", command=browse_destination_path)
browse_destination_button.grid(row=1, column=2, padx=5, pady=5)

copy_button = tk.Button(window, text="Start Copy", command=start_copy)
copy_button.grid(row=2, column=1, pady=10)

# Start the main loop
window.mainloop()
