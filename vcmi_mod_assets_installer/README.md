# VCMI Mod Assets Installer

## Overview

A tool that automates the extraction and installation of assets from original Heroes 3 mods into VCMI mods. This installer bridges the gap between classic H3 mod formats and the VCMI engine.

## What It Does

The installer performs these tasks automatically:
- Extracts assets from H3 mod archives (.pac, .snd, .vid files)
- Scans VCMI mod JSON files to determine which assets are needed
- Organizes assets into proper folders (Sprites, Sounds, Music, Video, Data)
- Copies assets to the correct locations in your VCMI mod

## Quick Start

### For Users

**Installing a Mod:**
See [INSTALLATION.md](INSTALLATION.md) for step-by-step instructions on installing the Succession Wars mod.

### For Developers

**Understanding the Tool:**
See [DEVELOPER.md](DEVELOPER.md) for technical documentation on how the installer works internally.

## Features

✅ **Automatic Asset Extraction** - Uses vcmiextract to unpack H3 archives  
✅ **Smart Path Calculation** - Determines correct folder structure based on file types  
✅ **JSON Processing** - Scans mod configs to find required assets  
✅ **Extraction Optimization** - Reuses previously extracted files to save time  
✅ **Music/Sound Separation** - Organizes .mp3 files into Music folder, .wav into Sounds  
✅ **Overridden Assets Support** - Handles manually specified asset overrides  

## Requirements

- **Python 3.x** (for running from source)
- **json5** library (install via `pip install json5`)
- **vcmiextract** tool (included in `vcmi_extract/` folder)
- Original H3 mod files to extract from
- VCMI mod folder to install assets into

## Usage

### Running the Executable

```bash
vcmi_mod_assets_installer.exe
```

### Running from Source

```bash
python vcmi_mod_assets_installer.py
```

## Building the Executable

To create a standalone .exe:

```bash
pip install pyinstaller
python -m PyInstaller --onefile --console --name vcmi_mod_assets_installer vcmi_mod_assets_installer.py
```

## Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - User guide for installing mods
- **[DEVELOPER.md](DEVELOPER.md)** - Technical documentation for developers
- **[settings.ini](settings.ini)** - Configuration file

## Project Structure

```
vcmi_mod_assets_installer/
├── README.md                          # This file
├── INSTALLATION.md                    # User installation guide
├── DEVELOPER.md                       # Developer documentation
├── vcmi_mod_assets_installer.py       # Main script
├── mod_data_extractor.py              # H3 archive extraction
├── extract_resources_and_their_relative_paths.py  # JSON scanning
├── calculate_actual_relative_paths_for_assets.py  # Path calculation
├── copy_mod_files.py                  # Asset copying
├── settings.ini                       # Configuration
├── vcmi_extract/                      # Extraction tool
│   └── vcmiextract.exe
└── out/                               # Generated files (gitignored)
```

## License

This tool is part of the VCMI Succession Wars mod project.

## Credits

- Uses [vcmiextract](https://github.com/IvanSavenko/vcmiextract) for H3 archive extraction
- Built for the [VCMI](https://vcmi.eu/) engine
- Designed for [Succession Wars](https://www.moddb.com/mods/h3sw) mod

