# How to Install Succession Wars Mod on VCMI

This guide walks you through installing the Succession Wars mod for VCMI step by step.

## Prerequisites

Before you begin, ensure you have:
- VCMI installed on your system

## Installation Steps

### Step 1: Download the Original Succession Wars Mod

1. Go to the [Succession Wars ModDB page](https://www.moddb.com/mods/h3sw/downloads/h3sw-v082-installer)
2. Download **H3SW v0.8.2 Installer**

### Step 2: Install the Original Mod

> **Note:** It can be installed in any folder on your disk. Does not need to be installed within a H3 installation folder.

1. Run the downloaded installer
2. Follow the installation wizard
3. Note the installation path (you'll need this later).

### Step 3: Install VCMI Mod Files

1. Locate your VCMI mods folder:
   - **Windows**: `C:\Users\[YourUsername]\Documents\My Games\vcmi\Mods\`
   - **Linux**: `~/.local/share/vcmi/Mods/`
   - **macOS**: `~/Library/Application Support/vcmi/Mods/`

2. Extract the `succession_wars_vcmi_mod` archive to this folder

3. You should now have these folders in your VCMI Mods directory:
   - `succession_wars/` (the main SW VCMI mod)
   - `ban_things/` (companion mod that disables original H3 objects)

### Step 4: Configure the Asset Installer

Before running the asset installer, you need to configure the paths:

1. Navigate to the installer folder:
   ```
   <VCMI Mods folder>\succession_wars\VCMI_SW_mod_Installer\
   ```

2. Open `settings.ini` in a text editor and update the paths to match your system:

   ```ini
   [Paths]
   mod_data_folder = C:\Program Files (x86)\Succession Wars\Data
   vcmi_mod_folder = C:\Users\[YourUsername]\Documents\My Games\vcmi\Mods\succession_wars
   
   [Archives]
   files = h3sw.pac, h3sw.snd, h3sw.vid, ingame_map_towns_dummy.pac
   ```

> **Note:**  Verify the `mod_data_folder` path points to where you installed the original mod in Step 2

### Step 5: Run the Asset Installer

1. From the same folder, run `vcmi_mod_assets_installer.exe`

2. The installer will:
   - Extract assets from the original H3 mod archives
   - Process VCMI mod configuration files
   - Copy assets to the correct locations

3. **If prompted** about reusing existing `out/mod_data` folder:
   - Choose **Yes** if you've run this before and want to save time
   - Choose **No** if you want a fresh extraction

4. Wait for the process to complete (may take several minutes on first run)

5. You should see messages indicating successful file copying

### Step 6: Launch VCMI

1. Open the VCMI Launcher

2. Go to the **Mods** section

3. Enable **only** these mods:
   - ✅ Succession Wars
   - ✅ Ban Things
   - ❌ Disable all other mods

4. Click **Start Game**

## Playing the Mod

### Current Limitations
- **No scenario map support** at this time only Jebus Cross random maps and Battle Mode are supported

## Need More Help?

- **Developer Documentation**: See `DEVELOPER_README.md` for technical details
- **VCMI Forums**: [https://forum.vcmi.eu/](https://forum.vcmi.eu/)
- **Succession Wars ModDB**: [https://www.moddb.com/mods/h3sw](https://www.moddb.com/mods/h3sw)

