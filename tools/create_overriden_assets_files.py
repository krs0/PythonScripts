import os

def parse_file(input_file):
    current_mod = None
    mod_added = set()  # Keep track of mods for which comments are already added
    mod_file_list = {}  # Dictionary to store files listed under each mod

    with open(input_file, 'r') as infile:
        for line in infile:
            # Check if the line is a source file comment
            if line.startswith("// Source file:"):
                # Extract the path of the source file
                source_path = line.split(":", 1)[1].strip()

                # Get the last occurrence of the relative mod path up to "\Content\"
                content_marker = r"\Content"
                if content_marker in source_path:
                    # Find the last occurrence of "\Content\" and get the mod path up to there
                    mod_path = source_path[:source_path.rfind(content_marker) + len(content_marker)]

                    # If we're in a new mod group and it's not added yet, insert the mod meta-comment
                    if mod_path != current_mod and mod_path not in mod_added:
                        current_mod = mod_path
                        mod_added.add(mod_path)
                        # Initialize file list for this mod
                        mod_file_list[current_mod] = set()

            # If it's a regular line (not a comment), extract the file name
            elif ":" in line and '"' in line:
                # Extract the part after the last colon and before the comma, then remove quotes and spaces
                right_part = line.split(":")[-1].strip()  # Get the right part after the colon
                if right_part.endswith(','):
                    right_part = right_part[:-1]  # Remove trailing comma if it exists

                # Extract the filename from within quotes
                listed_file = right_part.strip('"').strip()  # Remove quotes and extra spaces

                if current_mod:
                    mod_file_list[current_mod].add(listed_file)

    return mod_file_list


def list_files_on_disk(mod_base_path, mod_path):
    """Walk the mod folder and collect all file names and their relative paths, excluding .json and .txt files."""
    full_mod_path = os.path.join(mod_base_path, mod_path)
    file_list = set()

    # Check if mod path exists on disk
    if not os.path.exists(full_mod_path):
        print(f"Warning: Mod path '{full_mod_path}' does not exist.")
        return file_list

    # Recursively collect files, excluding .json and .txt files
    for root, dirs, files in os.walk(full_mod_path):
        for file in files:
            # Exclude .json and .txt files
            if not file.endswith('.json') and not file.endswith('.txt') and not file.endswith('.bmp') and not file.endswith('.pdn'):
                # Get the relative path to the mod base path
                relative_path = os.path.relpath(os.path.join(root, file), mod_base_path)  # Relative path to the base path
                # Store the tuple (relative path, filename)
                file_list.add((relative_path, file))  # Add a tuple containing relative path and filename
    return file_list


def find_overridden_assets(mod_file_list, mod_base_path):
    for mod_path, listed_files in mod_file_list.items():
        # List actual files on disk in the mod folder
        actual_files = list_files_on_disk(mod_base_path, mod_path)

        # Create a set of filenames from listed_files for comparison
        listed_filenames_set = set(listed_files)  # Use listed_files directly as a set for comparison

        # Find files on disk but not listed in the input file (compare only the second entry, which is the filename)
        overridden_files = {file_tuple for file_tuple in actual_files if file_tuple[1] not in listed_filenames_set}

        # Write the overridden files to a new file in the corresponding mod folder
        if overridden_files:
            # Move one level up from the "Content" subfolder
            # Find the path up to one level before "Content"
            parent_mod_path = mod_path[:mod_path.rfind(r"\Content")]

            # Construct the output path to save one level up from "Content"
            mod_output_path = os.path.join(mod_base_path, parent_mod_path, "overridden_assets.txt")

            # Ensure the mod folder exists, if not create it
            mod_folder = os.path.dirname(mod_output_path)
            os.makedirs(mod_folder, exist_ok=True)

            with open(mod_output_path, 'w') as outfile:
                for relative_path, file_name in overridden_files:
                    # Write the full relative path and the file name
                    outfile.write(f'"{relative_path}" : "{file_name}"\n')


if __name__ == "__main__":
    # Default paths
    mod_base_path = r"d:/git/succession_wars_overridden_assets_tests"  # Default mod base path
    input_file = r"d:/temp/Krs/Python/Extract_WoG_relative_paths/out/assets_to_paths_mapping.txt"  # Default input file

    # Step 1: Parse the input file and collect listed files for each mod
    mod_file_list = parse_file(input_file)

    # Step 2: Find overridden assets and save to individual files in each mod folder
    find_overridden_assets(mod_file_list, mod_base_path)
