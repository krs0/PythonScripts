import os
import json5  # json5 allows comments in JSON

# json5 may or may not expose a JSON5DecodeError class depending on version.
# Fall back to ValueError so decode errors are caught correctly.
try:
    JSON5DecodeError = json5.JSON5DecodeError
except AttributeError:
    JSON5DecodeError = ValueError
import argparse
import re


def process_json_files(folder_path, output_file):
    # Use os.walk to iterate over all files in the folder and subfolders
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            # Skip files named mod.json
            if filename == "mod.json":
                continue
            
            if filename.endswith(".json"):
                file_path = os.path.join(dirpath, filename)
                # Open the file with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        # Use json5 to load the JSON file with support for comments
                        data = json5.load(json_file)
                        
                        # Check for valid values before writing the source file message
                        found_values = check_for_valid_values(data)

                        # Write the source file comment only if valid values were found
                        if found_values:
                            relative_path = os.path.relpath(file_path, folder_path)
                            with open(output_file, 'a', encoding='utf-8') as out_file:
                                out_file.write(f'// Source file: {relative_path}\n')

                            # Process the JSON data after writing the comment
                            process_json(data, output_file)

                    except JSON5DecodeError:
                        # Print only the simple file name for JSON decode errors (concise output)
                        print(os.path.basename(file_path))
                        continue
                    except UnicodeDecodeError as e:
                        print(f"Unicode decoding error in file {file_path}: {e}")


def check_for_valid_values(data):
    # Function to check if there are valid values in the JSON data
    valid_extensions = {".def", ".png", ".bik", ".smk", ".mp3", ".wav"}
    
    if isinstance(data, dict):
        return any(check_for_valid_values(value) for value in data.values())
    elif isinstance(data, list):
        return any(check_for_valid_values(item) for item in data)
    else:
        # Check if data is a string containing '/' or ends with one of the valid extensions
        return isinstance(data, str) and ('/' in data or any(data.endswith(ext) for ext in valid_extensions))


def process_json(data, output_file, parent_key=""):
    # Recursive function to traverse the JSON structure and write valid values to the output file
    if isinstance(data, dict):
        for key, value in data.items():
            process_json(value, output_file, parent_key + key + ".")
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            process_json(item, output_file, parent_key + str(idx) + ".")
    else:
        # Only process string values that contain '/' and do not contain unwanted patterns
        if isinstance(data, str) and '/' in data and not is_unwanted_line(data):
            node_value = data
            # Check if node_value already has an extension
            base_name, extension = os.path.splitext(node_value)

            # Define a set of valid extensions
            valid_extensions = {".def", ".wav", ".mp3", ".bmp", ".png", ".bik"}

            # Check if the extension is empty or not in the valid extensions
            if not extension or extension.lower() not in valid_extensions:
                node_value += ".def"

            # Replace .bmp with .png
            if '.bmp' in node_value:
                node_value = node_value.split('.bmp')[0] + '.png'

            # If node_value contains ".def:", remove ":" and everything after it
            if '.def:' in node_value:
                node_value = node_value.split('.def:')[0] + '.def'

            # Extract file name from the relative path
            file_name = os.path.basename(node_value)

            # Write to the output file in the format "<node_value>" : "<file_name>",
            with open(output_file, 'a', encoding='utf-8') as out_file:
                out_file.write(f'"{node_value}" : "{file_name}",\n')


def is_unwanted_line(line):
    # Function to determine if a line is unwanted based on specific criteria
    # Exclude lines that contain '//'
    return '//' in line  # Check for unwanted patterns


def main():
    parser = argparse.ArgumentParser(description="Process JSON files to extract specific data.")
    parser.add_argument('--folder', type=str, default=r"c:/Users/Krs/Documents/My Games/vcmi/Mods/succession_wars/Mods",
                        help="Path to the folder containing JSON files.")
    parser.add_argument('--output', type=str, default=r"c:/Users/Krs/Documents/My Games/vcmi/Mods/succession_wars/VCMI_SW_mod_Installer/out/assets_to_paths_mapping_raw_2.txt",
                        help="Path to the output file.")

    args = parser.parse_args()

    folder_path = args.folder
    output_file = args.output

    # Create or clear the output file at the start
    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("")  # Clear the file

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        process_json_files(folder_path, output_file)
    else:
        print(f"The folder path '{folder_path}' is not valid.")


if __name__ == "__main__":
    main()
