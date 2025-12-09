"""
VCMI Mod Assets Installer

This script extracts assets from original H3 mod, and moves them to the right locations in VCMI mod.

Usage:
1. Ensure that the `settings.ini` file is correctly configured with the paths and archive names.
2. Run the script. It will perform the following steps:
   - Read settings from the INI file.
   - Validate and create necessary directories.
   - Extract files from the specified Heroes 3 mod data folder.
   - Process VCMI Mod .json files to determine necessary assets for the VCMI mod.
   - Copy the extracted assets to the VCMI mod folder.

Example settings.ini:
[Paths]
mod_data_folder = /path/to/mod/data
vcmi_mod_folder = /path/to/vcmi/mod

[Archives]
files = archive1.zip, archive2.zip

"""

import configparser
import os
from mod_data_extractor import extract_files
from extract_resources_and_their_relative_paths import process_json_files
from calculate_actual_relative_paths_for_assets import calculate_actual_paths_for_assets
from copy_mod_files import copy_assets


def main():
    # Read settings from the INI file
    config = configparser.ConfigParser()
    config.read('settings.ini')
    
    mod_data_folder = config['Paths']['mod_data_folder']
    vcmi_mod_folder = config['Paths']['vcmi_mod_folder']

    # Ensure the directories exist
    if not os.path.exists(mod_data_folder):
        print(f"Input directory does not exist: {mod_data_folder}")
        return
    
    # Get the current directory and set the temporary output folder
    current_directory = os.getcwd()
    out_folder = os.path.join(current_directory, 'out')  # Create the output path

    if not os.path.exists(out_folder):
        print(f"Temporary output directory does not exist, creating: {out_folder}")
        os.makedirs(out_folder)

    temp_mod_data_folder = os.path.join(out_folder, 'mod_data')

    # Check if mod_data folder already exists and ask user if they want to reuse it
    skip_extraction = False
    if os.path.exists(temp_mod_data_folder) and os.listdir(temp_mod_data_folder):
        print(f"\nFound existing mod_data folder: {temp_mod_data_folder}")
        response = input("Do you want to reuse the existing extracted files? (y/n): ").strip().lower()
        if response == 'y' or response == 'yes':
            print("Reusing existing mod_data folder. Skipping extraction...")
            skip_extraction = True
        else:
            print("Will re-extract files to mod_data folder...")

    if not skip_extraction:
        if not os.path.exists(temp_mod_data_folder):
            print(f"Creating Temporary mod data folder for data extraction: {temp_mod_data_folder}")
            os.makedirs(temp_mod_data_folder)

        # Get the list of archive names from the INI settings or define a default
        archive_names = config.get('Archives', 'files').split(',')

        # Call the function to extract files with the archive names
        print(f"Start extracting original mod assets from: {mod_data_folder}")
        extract_files(mod_data_folder, archive_names, temp_mod_data_folder)

    assets_to_paths_mapping_raw_file_path = os.path.join(out_folder, 'assets_to_paths_mapping_raw.txt') 

    if not os.path.exists(vcmi_mod_folder):
        print(f"Error! VCMI mod folder does not exist: {vcmi_mod_folder}")
        return

    # Clear the output file at the start
    with open(assets_to_paths_mapping_raw_file_path, 'w', encoding='utf-8') as out_file:
        out_file.write("")

    # Read all the needed assets for vcmi_mod
    print(f"Calculate needed assets for VCMI Mod: {vcmi_mod_folder}")
    process_json_files(vcmi_mod_folder, assets_to_paths_mapping_raw_file_path)

    assets_to_paths_mapping_file_path = os.path.join(out_folder, 'assets_to_paths_mapping.txt')

    # Call the parse_file function from the original script directly
    print(f"Calculating actual paths for assets: from {assets_to_paths_mapping_raw_file_path} to {assets_to_paths_mapping_file_path}")
    calculate_actual_paths_for_assets(assets_to_paths_mapping_raw_file_path, assets_to_paths_mapping_file_path)

    copy_assets(assets_to_paths_mapping_file_path, temp_mod_data_folder, vcmi_mod_folder)


if __name__ == "__main__":
    main()
