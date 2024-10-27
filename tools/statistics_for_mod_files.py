import os
import re

def read_input_file(input_file_path):
    """Read the input file and extract the file names and their paths, ignoring comment lines."""
    file_entries = []
    with open(input_file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace
            # Skip lines starting with //
            if line.startswith('//'):
                continue
            
            # Match the pattern and extract the first and second entries
            match = re.match(r'^\s*"([^"]*)"\s*:\s*"([^"]+)"', line)
            if match:
                file_entries.append((match.group(1), match.group(2)))  # (first entry, second entry)
            else:
                print(f"Warning: Line did not match expected format: {line}")
    return file_entries


def check_files_in_directory(file_entries, directory):
    """Check for existence of files in the given directory and return missing files with their paths."""
    missing_files = [(first_entry, second_entry) for first_entry, second_entry in file_entries if not os.path.exists(os.path.join(directory, second_entry))]
    return missing_files


def list_all_files_in_directory(directory):
    """List all files in the given directory."""
    return [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]


def find_files_without_entries(all_files, file_entries):
    """Find files in the directory that do not have entries in the input."""
    second_entries = {second_entry for _, second_entry in file_entries}
    return [file for file in all_files if file not in second_entries]


def normalize_filename(filename):
    """Normalize the filename by removing its extension."""
    return os.path.splitext(filename)[0]


def find_intersection(files1, files2):
    """Find the intersection of two lists disregarding file extensions, excluding .wav files."""
    intersection = set()
    for file1 in files1:
        for file2 in files2:
            # Skip if either file has a .wav extension
            if file1.lower().endswith('.wav') or file2.lower().endswith('.wav'):
                continue
            # Compare normalized filenames
            if normalize_filename(file1) == normalize_filename(file2):
                intersection.add(normalize_filename(file1))  # Add only the name without extension
    return intersection


def main(input_file_path, directory, missing_files_output, files_without_entries_output, intersection_output):
    # Check if the input file exists
    if not os.path.exists(input_file_path):
        print(f"Error: The file '{input_file_path}' does not exist.")
        return
    
    # Read the input file
    file_entries = read_input_file(input_file_path)
    
    # Check for missing files in the directory
    missing_files_in_directory = check_files_in_directory(file_entries, directory)
    
    # List all files in the directory
    all_files_in_directory = list_all_files_in_directory(directory)
    
    # Find files in the directory that do not have entries in the input file
    files_without_entries = find_files_without_entries(all_files_in_directory, file_entries)

    # Write the files without entries to one output file
    with open(files_without_entries_output, 'w') as output_file:
        output_file.write("Files in the Directory that do not exist in the .txt file:\n")
        for file in files_without_entries:
            output_file.write(file + '\n')

    # Write the missing files with their first entries to another output file
    with open(missing_files_output, 'w') as output_file:
        output_file.write("Files in the .txt file that do not exist on disk:\n")
        for first_entry, second_entry in missing_files_in_directory:
            output_file.write(f"{first_entry} : {second_entry}\n")

    # Find intersection of the two lists disregarding extensions and excluding .wav files
    intersection = find_intersection([second_entry for first_entry, second_entry in missing_files_in_directory],
                                     files_without_entries)

    # Write the intersection to a new output file
    with open(intersection_output, 'w') as output_file:
        output_file.write("Intersection of files disregarding extensions (excluding .wav files):\n")
        for file in intersection:
            output_file.write(file + '\n')

    print(f"Results have been written to '{files_without_entries_output}', '{missing_files_output}', and '{intersection_output}'.")


if __name__ == "__main__":
    # Example usage
    input_file_path = r'd:\temp\Krs\Python\Extract_WoG_relative_paths\output_SW.txt'
    directory = r'd:\temp\Krs\Python\Extract_WoG_relative_paths\h3sw'
    files_without_entries_output = r'd:\temp\Krs\Python\Extract_WoG_relative_paths\files_without_entries.txt'
    missing_files_output = r'd:\temp\Krs\Python\Extract_WoG_relative_paths\missing_files.txt'
    intersection_output = r'd:\temp\Krs\Python\Extract_WoG_relative_paths\intersection_files.txt'

    main(input_file_path, directory, missing_files_output, files_without_entries_output, intersection_output)
