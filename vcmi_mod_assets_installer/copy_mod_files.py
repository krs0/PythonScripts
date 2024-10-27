import os
import shutil
import argparse


def copy_mod_assets(assets_to_path_mapping_file_path, source_folder, destination_folder):
    # Read the input file and process each line
    with open(assets_to_path_mapping_file_path, 'r') as input_file:
        for line in input_file:
            line = line.strip()
            # Ignore comment lines
            if line.startswith("//") or not line:
                continue
            
            # Split the line into source and destination
            parts = line.split(":")
            if len(parts) != 2:
                print(f"Invalid line format: {line}")
                continue

            # Extract source file and destination path
            source_file = parts[0].strip().strip('"')  # Remove quotes
            dest_file_name = parts[1].strip().strip('",')  # Remove quotes and trailing commas
            
            # Construct the full source file path
            full_source_path = os.path.join(source_folder, dest_file_name)
            # Construct the full destination path
            dest_path = os.path.join(destination_folder, source_file)
            
            # Create the destination directory if it does not exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            # Copy the file if it exists in the source folder
            if os.path.exists(full_source_path):
                shutil.copy(full_source_path, dest_path)  # Copy the file
                print(f"Copied: {full_source_path} -> {dest_path}")
            else:
                print(f"File not found: {full_source_path}")


def copy_overridden_assets(destination_folder, source_folder):
    # Walk through the destination folder recursively
    for root, dirs, files in os.walk(destination_folder):
        for file in files:
            if file == "overridden_assets.txt":
                overridden_assets_path = os.path.join(root, file)
                with open(overridden_assets_path, 'r') as overridden_file:
                    for line in overridden_file:
                        line = line.strip()
                        # Ignore comment lines
                        if line.startswith("//") or not line:
                            continue
                        
                        # Split the line into relative path and file name
                        parts = line.split(":")
                        if len(parts) != 2:
                            print(f"Invalid line format in {overridden_assets_path}: {line}")
                            continue

                        # Extract relative path and file name
                        relative_path = parts[0].strip().strip('"')  # Remove quotes
                        file_name = parts[1].strip().strip('",')  # Remove quotes and trailing commas
                        
                        # Construct the full source file path
                        full_source_path = os.path.join(source_folder, file_name)
                        # Construct the full destination path
                        dest_path = os.path.join(destination_folder, relative_path)

                        # Create the destination directory if it does not exist
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                        # Copy the file if it exists in the source folder
                        if os.path.exists(full_source_path):
                            shutil.copy(full_source_path, dest_path)  # Copy the file
                            print(f"Copied: {full_source_path} -> {dest_path}")
                        else:
                            print(f"File not found: {full_source_path}")


def copy_assets(assets_to_path_mapping_file_path, source_folder, destination_folder):
    # Call the individual copy functions
    copy_mod_assets(assets_to_path_mapping_file_path, source_folder, destination_folder)
    copy_overridden_assets(destination_folder, source_folder)


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy files based on input instructions.')
    
    # Adding arguments with default values
    parser.add_argument('--assets_to_path_mapping_file_path', type=str, 
                        default=r"d:\temp\Krs\Python\Extract_WoG_relative_paths\out\assets_to_paths_mapping.txt",
                        help='Path to your input text file')
    parser.add_argument('--source_folder', type=str, 
                        default=r"d:\temp\Krs\Python\Extract_WoG_relative_paths\out\mod_data",
                        help='Path to your source folder')
    parser.add_argument('--destination_folder', type=str, 
                        default=r"d:\git\succession_wars_overridden_assets_tests",
                        help='Path to your destination folder')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Call the wrapper function to copy assets
    copy_assets(args.assets_to_path_mapping_file_path, args.source_folder, args.destination_folder)
