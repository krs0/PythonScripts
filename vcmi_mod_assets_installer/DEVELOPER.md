# VCMI Mod Assets Installer - Developer Documentation

## Overview
This tool extracts assets from original Heroes 3 mods and moves them to the correct locations in VCMI mods. It automates the process of asset extraction, path calculation, and file organization.

## Main Execution Flow

When `vcmi_mod_assets_installer.py` runs, it performs the following steps:

### Step 1: Read Configuration
- Reads `settings.ini` file
- Extracts paths:
  - `mod_data_folder`: Source folder containing H3 mod archives (.pac, .snd, .vid files)
  - `vcmi_mod_folder`: Destination VCMI mod folder
- Extracts archive names to process

### Step 2: Setup Output Directories
- Creates `out/` folder in current directory (if doesn't exist)
- Creates `out/mod_data/` temporary folder for extracted assets
- **Optimization**: If `out/mod_data/` already exists and contains files, prompts user to reuse it (skips extraction)

### Step 3: Extract Original Mod Assets
**Script**: `mod_data_extractor.py` → `extract_files()`

- Uses `vcmiextract.exe` to extract archives from H3 mod
- Processes each archive specified in settings.ini:
  - `.pac` files (graphics/sprites)
  - `.snd` files (sounds)
  - `.vid` files (videos)
- Copies MP3 files from `mp3/` folder (located one level up from Data folder)
- Removes unwanted file types (.txt, .msk, .msg, .fnt, .pal)
- **Output**: All extracted assets in `out/mod_data/`

### Step 4: Scan VCMI Mod JSON Files
**Script**: `extract_resources_and_their_relative_paths.py` → `process_json_files()`

- Recursively scans all `.json` files in VCMI mod folder (except `mod.json`)
- Extracts asset references from JSON data:
  - Looks for strings containing `/` or ending with valid extensions (.def, .png, .bik, .smk, .mp3, .wav)
  - Processes nested JSON structures (dicts, lists)
- Normalizes file extensions:
  - Adds `.def` if no extension present
  - Converts `.bmp` → `.png`
  - Cleans up `.def:` patterns
- **Output**: `out/assets_to_paths_mapping_raw.txt`
  - Format: `"path/in/json" : "filename.ext",`
  - Includes source file comments for traceability

### Step 5: Calculate Actual Asset Paths
**Script**: `calculate_actual_relative_paths_for_assets.py` → `calculate_actual_paths_for_assets()`

- Reads `assets_to_paths_mapping_raw.txt`
- Determines output directory based on file extension:
  - `.def` → `Sprites/`
  - `.wav` → `Sounds/`
  - `.mp3` → `Music/`
  - `.bik` → `Video/`
  - `.png` → `Data/`
- Constructs full relative paths with proper directory structure
- Extracts relative root from source file comments (up to `Content/`)
- **Output**: `out/assets_to_paths_mapping.txt`
  - Format: `"full/relative/path/to/asset" : "filename.ext",`

### Step 6: Copy Assets to VCMI Mod
**Script**: `copy_mod_files.py` → `copy_assets()`

Performs two copy operations:

#### 6a. Copy Main Assets
- Reads `assets_to_paths_mapping.txt`
- For each entry:
  - Source: `out/mod_data/filename.ext`
  - Destination: `vcmi_mod_folder/full/relative/path/to/asset`
  - Creates destination directories as needed
  - Reports missing files

#### 6b. Copy Overridden Assets
- Searches for `overridden_assets.txt` files in VCMI mod folder
- These files contain manually specified asset overrides
- Copies additional assets not found in JSON files
- Same format and process as main assets

## File Structure

```
vcmi_mod_assets_installer/
├── vcmi_mod_assets_installer.py          # Main orchestrator
├── mod_data_extractor.py                 # Step 3: Extract H3 archives
├── extract_resources_and_their_relative_paths.py  # Step 4: Scan JSON files
├── calculate_actual_relative_paths_for_assets.py  # Step 5: Calculate paths
├── copy_mod_files.py                     # Step 6: Copy assets
├── settings.ini                          # Configuration
├── vcmi_extract/                         # External extraction tool
│   └── vcmiextract.exe
└── out/                                  # Generated output (gitignored)
    ├── mod_data/                         # Extracted H3 assets
    ├── assets_to_paths_mapping_raw.txt   # Raw asset list
    └── assets_to_paths_mapping.txt       # Final asset mapping
```

## Key Design Decisions

### Extraction Optimization
- Reuses existing `out/mod_data/` if present
- Saves time during iterative development
- User can force re-extraction if needed

## Dependencies

- **Python 3.x**
- **json5**: For parsing JSON files with comments
- **vcmiextract**: External tool for extracting H3 archives (included in `vcmi_extract/`)

## Common Use Cases

### First Run
1. Configure `settings.ini` with correct paths
2. Run script → extracts everything from scratch
3. Assets copied to VCMI mod folder

### Iterative Development
1. Modify VCMI mod JSON files
2. Run script → reuses existing extracted assets
3. Only recalculates paths and copies needed files

