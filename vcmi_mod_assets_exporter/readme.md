# VCMI Mod Assets Exporter

## Overview
A simple GUI tool that extracts **only assets** (graphics, sounds, videos, etc.) from a VCMI mod folder to a designated output folder. This tool is useful for backing up, sharing, or analyzing mod assets without including configuration files or JSON data.

## Purpose
- Extract all asset files from a VCMI mod while preserving folder structure
- Exclude configuration files, JSON files, and documentation
- Prepare assets for distribution or backup
- Useful for mod developers who want to separate assets from mod logic

## How It Works

### Main Execution Flow

#### 1. Launch GUI
- Opens a simple window with two path inputs and a "Start extraction" button
- Loads previously used paths from `settings.ini` (if exists)

#### 2. Select Paths
**Source Path (VCMI mod folder):**
- The root folder of your VCMI mod
- Contains all mod files including JSON configs and assets

**Output Folder:**
- Where extracted assets will be copied
- Defaults to `out/` in current directory if not specified
- **Must be empty** - tool will warn if folder contains files

#### 3. Start Extraction
When you click "Start extraction":

**Step 1: Validate Output Folder**
- Checks if output folder exists and is empty
- Shows warning if folder is not empty (prevents accidental overwrites)
- Saves selected paths to `settings.ini` for next time

**Step 2: Copy Files with Filtering**
- Recursively walks through source folder
- Copies files while **excluding** non asset files

**Step 3: Preserve Structure**
- Maintains the exact folder structure from source

## File Structure

```
vcmi_mod_assets_exporter/
├── vcmi_mod_assets_exporter.py    # Main GUI application
├── settings.ini                   # Saved paths (auto-generated)
└── out/                           # Default output folder (if not specified)
```

## Usage

### First Time Use
1. Run `vcmi_mod_assets_exporter.py`
2. Click "Browse" next to "VCMI mod folder" and select your mod folder
3. Click "Browse" next to "Output Folder" and select where to save assets (or leave default)
4. Click "Start extraction"
5. Wait for completion message

## Configuration File

The tool automatically creates/updates `settings.ini`:

```ini
[Paths]
vcmi_mod_folder = D:\Games\VCMI\Mods\my_mod
output_folder = D:\Backup\mod_assets
```

## Safety Features

### Non-Destructive
- Never modifies source files
- Only copies files to destination
- Original mod folder remains untouched

## Common Use Cases

### 1. Backup Assets
Extract all assets from a mod for backup purposes:
- Source: Your working mod folder
- Output: Backup location
- Result: Clean asset backup without configs

## Dependencies

- **Python 3.x**
- **tkinter** (usually included with Python)
- **Standard library**: os, shutil, configparser

