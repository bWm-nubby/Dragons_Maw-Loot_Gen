# Dragon's Maw Loot Generator

This project is a loot generator inspired by Diablo 2, designed for use in AD&D 2nd edition tabletop RPG sessions. It generates randomized treasure based on customizable loot tables. 

---

## Features
- Randomized loot generation based on JSON loot tables
- Easy to customize and extend loot tables
- Simple browser based GUI for ease of use
- Output logs to CSV for tracking generated treasure

## To-Do
- Add customized loot table with only weapons and armor present in AD&D 1e
- Add recommended sell price to items (gp value * 0.25)
- Upload downloadable .zip version with python included
- Add automatic updating capability to the start-windows.bat script
- Add Linux installation instructions
- Consider adding all spells to facilitate rolling the specific spell for items that include spells.

---

# Windows Only

## **RECOMENDED** Portable Installation (No Python or Git Required)
1. Download the portable ZIP version from: [REPLACE_WITH_ZIP_LINK]
2. Unzip the contents to a folder of your choice.
3. Double-click `start-windows.bat` to run the generator.
4. The application should then be accessible via your web browser, usually at `http://127.0.0.1:7860`.

## Manual Installation

## Requirements
- [Git](https://git-scm.com/)
- Python >=3.10 - Tested with [Python 3.12.10](https://www.python.org/downloads/release/python-31210/) - other versions should work but have not been tested.

### 1. Install Git
Download and install Git from [git-scm.com](https://git-scm.com/download/win).

### 2. Install Python 3.12.10
Download and install Python 3.12.10 from [python.org](https://www.python.org/downloads/release/python-31210/).
If you're unsure which version you need, it's most likely the Windows installer (64-bit) version in the Files section click the name of the installer to download it.
Make sure to check "Add Python to PATH" during installation.

### 3. Clone the Repository
Open CMD and run:
```bash
git clone https://github.com/bWm-nubby/Dragons_Maw_Loot_Gen.git
cd Diablo-2-Loot-Gen
```

### 4. Install Dependancies and Run the Application
1. Run: start-windows.bat
    This will attempt to create a Python Virtual Environment and install dependencies on the first run and will launch normally without reinstalling afterwards. 
    If you would prefer to create your own venv it should be named `venv` and be located in the root of this repository. Be sure to install requirements.txt if you create your own venv.
2. The application should then be accessible via your web browser, usually at `http://127.0.0.1:7860`.

---

# Linux & macOS

## Manual Installation

### Requirements
- [Git](https://git-scm.com/)
- Python >=3.10 - Tested with [Python 3.12.10](https://www.python.org/downloads/release/python-31210/) - other versions should work but have not been tested.

### 1. Install Git
Follow the instructions on [git-scm.com](https://git-scm.com/downloads) for your specific operating system.

### 2. Install Python 3.12.10
It is recommended to install Python via your system's package manager (e.g., `apt` on Debian/Ubuntu, `brew` on macOS) or from the official [python.org](https://www.python.org/downloads/) website.

### 3. Clone the Repository
Open your terminal and run:
```bash
git clone https://github.com/bWm-nubby/Dragons_Maw_Loot_Gen.git
cd Diablo-2-Loot-Gen
```

### 4. Set up Virtual Environment and Run the Application
It is highly recommended to use a Python virtual environment to manage dependencies.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
The application should then be accessible via your web browser, usually at `http://127.0.0.1:7860`.

---

## Usage
The generator uses loot tables defined in `loot_tables/default.json`. Generated loot is saved in `logs/treasure.csv` which can be imported into a spreadsheet application such as Excel for tracking and analysis. To clear the log file simply delete, move, or rename the `treasure.csv` file and a new one will be created the next time you click the Save to Log button in the UI.

## Customization
Edit or add JSON files in the `loot_tables/` directory to create your own loot tables.

## License
This project is released under the MIT License.
