"""
Heroes 3 Mod Data Extractor Script

This script is designed to extract specified H3 archive files from a given source directory 
and save the extracted files to a designated output directory. It is using vcmiextract: https://github.com/IvanSavenko/vcmiextract

Key Features:
- Extracts archive files using an external command-line tool (`vcmiextract`).
- Copies extracted files from the temporary extraction directory to the specified output directory.
- Removes unwanted file types (e.g., `.txt`, `.msk`, `.msg`, `.fnt`, `.pal`) from the output directory.
- Optionally, it copies all MP3 files from a designated folder (located one level up) to the output directory.

Usage Instructions:
3. Run the script via the command line with the following syntax:
python mod_data_extractor.py <mod_data_folder> <mod_data_out_folder> <archive_files>

where:
- `<mod_data_folder>`: Directory containing the archive files.
- `<mod_data_out_folder>`: Directory to save extracted files.
- `<archive_files>`: List of archive file names to extract (space-separated).

Example Command: bash
python mod_data_extractor.py /path/to/mod/data /path/to/output_folder archive1.arc archive2.arc
"""

import subprocess
import os
import glob
import shutil
import argparse


def extract_archive(archive_path, output_directory):
    # Ensure the path is absolute
    archive_path = os.path.abspath(archive_path)

    # Command to call the external program
    command = ['./vcmi_extract/vcmiextract', archive_path]

    try:
        # Run the command and wait for it to complete
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        # Print the output from the command
        print("Output:", result.stdout)
        print("Errors:", result.stderr)

        # Get the directory where files are extracted
        extract_dir = os.path.splitext(archive_path)[0]  # Remove the extension to get the folder name

        # Copy extracted files to the output directory
        copy_extracted_files(extract_dir, output_directory)

        # Remove unwanted files from the output directory
        remove_unwanted_files(output_directory)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error output: {e.stderr}")


def copy_mp3_folder(source_folder, output_folder):
    """Copy all files from the mp3 folder (located one level up in Succession Wars mod) to the output directory."""
    # Copy all files from the mp3 folder to the output directory
    if os.path.exists(source_folder):
        for item in os.listdir(source_folder):
            s = os.path.join(source_folder, item)
            d = os.path.join(output_folder, item)
            if os.path.isfile(s):
                shutil.copy(s, d)  # Copy file without preserving metadata
                print(f"Copied: {s} to {d}")
    else:
        print(f"Source MP3 folder not found: {source_folder}")


def copy_extracted_files(source_dir, target_dir):
    """Copy extracted files to the target directory, overwriting if they exist."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            target_file_path = os.path.join(target_dir, filename)
            shutil.copy(file_path, target_file_path)  # Copy file without preserving metadata


def remove_unwanted_files(directory):
    # List of file extensions to remove
    extensions_to_remove = ['*.txt', '*.msk', '*.msg', '*.fnt', '*.pal']

    for ext in extensions_to_remove:
        # Use glob to find files with the given extension
        for file_path in glob.glob(os.path.join(directory, ext)):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


def extract_files(source_folder, archive_names, output_folder):
    """Extracts files from specified archives to output directory."""
    for archive_name in archive_names:
        archive_name = archive_name.strip()  # Remove leading/trailing whitespace
        archive_path = os.path.join(source_folder, archive_name)  # Construct full path
        if os.path.exists(archive_path):
            print(f"Starting extracting: {os.path.basename(archive_path)}")
            extract_archive(archive_path, output_folder)
        else:
            print(f"File not found: {archive_path}")

    mp3_folder_path = os.path.join(os.path.dirname(source_folder), 'mp3') # mp3 folder is one level above data folder
    copy_mp3_folder(mp3_folder_path, output_folder)


# Entry point for standalone execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract archives and clean up unwanted files.")
    parser.add_argument('mod_data_folder', nargs='?', help="Directory containing the archive files.")
    parser.add_argument('mod_data_out_folder', nargs='?', help="Directory to save extracted files.")
    parser.add_argument('archive_files', nargs='*', help="List of archive names to extract.")

    args = parser.parse_args()

    if args.archive_files:
        archive_names = args.archive_files

    extract_files(args.mod_data_folder, archive_names, args.mod_data_out_folder)
