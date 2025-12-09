import re
import os
import argparse

def calculate_actual_paths_for_assets(input_file_path, output_file_path):
    # Initialize the relative root and a list to hold all lines
    relative_root = ""
    output_lines = []

    with open(input_file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Check for source file comment
            if line.startswith("// Source file:"):
                # Extract the relative root before 'Content'
                match = re.search(r'^(.*?Content)', line)  # Changed 'config' to 'Content'
                if match:
                    # Remove the prefix '// Source file: ' and construct relative_root
                    relative_root = match.group(0).replace("// Source file: ", "").replace("Content", "").lower() + "content\\"
                # Add the comment line to output (but do not process it)
                output_lines.append(line)  # Retain the comment line in the output
                continue
            
            # Skip comments that start with // and empty lines
            if line.startswith("//") or not line:
                output_lines.append(line)  # Keep comments in the output
                continue
            
            # Use regex to find the path and definition
            match = re.match(r'"([^"]+)"\s*:\s*"([^"]+)"', line)
            if match:
                path, definition = match.groups()
                # Determine the extension type
                ext = os.path.splitext(definition)[1].lower()
                # Create the output directory based on the extension
                if ext == '.def':
                    output_directory = "Sprites"
                elif ext == '.wav':
                    output_directory = "Sounds"
                elif ext == '.mp3':
                    output_directory = "Music"
                elif ext == '.bik':
                    output_directory = "Video"
                elif ext == '.png':
                    output_directory = "Data"
                else:
                    output_directory = ""  # Handle unknown extensions

                # Create the new relative path using backslashes
                new_path = relative_root + output_directory + "\\" + path.replace('/', '\\')
                # Replace the path in the output line
                new_line = f'"{new_path}" : "{definition}",'
                output_lines.append(new_line)  # Add the valid entry to the output
            else:
                # If the line doesn't match, keep it unchanged
                output_lines.append(line)

    # Write the modified lines to the output file
    with open(output_file_path, 'w') as output_file:
        for output_line in output_lines:
            output_file.write(output_line + '\n')


if __name__ == "__main__":
    # Default file paths
    default_input_file_path = 'd:\\temp\\Krs\\Python\\Extract_WoG_relative_paths\\out\\output_SW.txt'
    default_output_file_path = 'd:\\temp\\Krs\\Python\\Extract_WoG_relative_paths\\out\\output_SW_prepared_for_copy.txt'

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Process input and output file paths.")
    parser.add_argument('input_file', type=str, nargs='?', default=default_input_file_path, help='The path to the input file (default: %(default)s)')
    parser.add_argument('output_file', type=str, nargs='?', default=default_output_file_path, help='The path to the output file (default: %(default)s)')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the parse_file function with the provided or default file paths
    calculate_actual_paths_for_assets(args.input_file, args.output_file)
