# Dragon's Maw Loot Generator

This project is a loot generator inspired by Diablo 2, designed for use in AD&D 2nd edition tabletop RPG sessions. It generates randomized treasure based on customizable loot tables using the [Mersenne Twister](https://en.wikipedia.org/wiki/Mersenne_Twister) PRNG algorithm. The included default loot tables are capable of generating more than 1 million unique magic items ranging from simple healing potions to magical suits of armor that might increase the wearer's stats as well as reducing the damage they take. But don't worry, not all of these effects will aid the characters, some items are cursed maybe even twice... How does a *Clumsy Great Sword of Pox*, which gives -2 to hit and reduces base damage to 1 as well as preventing the user from regaining hit points while in possession of the item, sound to you?

---

## Features
- Randomized loot generation based on JSON loot tables
- Easy to customize and extend loot tables
- Simple browser based GUI for ease of use
- Output logs to CSV for tracking generated treasure

## To-Do
~~- Add customized loot table with only weapons and armor more appropriate to AD&D 1e~~
- Add recommended sell price to items in the UI (gp value * 0.25)
~~- Upload downloadable .zip version with python included~~
~~- Add automatic updating capability to the start-windows.bat script~~
~~- Add Linux installation instructions~~
- Consider adding all spells to facilitate rolling the specific spell for items that include spells

---

# Windows Only

## **RECOMENDED** Portable Installation (No Python or Git Required)
1. Download the latest portable ZIP version from the [Releases page](https://github.com/bWm-nubby/Dragons_Maw_Loot_Gen/releases)
2. Unzip the contents to a folder of your choice and open it.
3. Double-click `start-windows.bat` to run the generator.
4. The application should then be accessible via your web browser, usually at `http://127.0.0.1:7860`.
If you have trouble unzipping the file, `right click the file -> properties -> unblock` and try again.

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
cd Dragons_Maw_Loot_Gen
```

### 4. Install Dependancies and Run the Application
1. Run: `start-windows.bat`
    This will attempt to create a Python Virtual Environment and install dependencies on the first run and will launch normally without reinstalling afterwards. 
    If you would prefer to create your own venv it should be named `venv` and be located in the root of this repository. Be sure to install requirements.txt if you create your own venv.
2. The application should then be accessible via your web browser, usually at `http://127.0.0.1:7860`.

## Updating
1. Run: `update-windows.bat`
That's it... Really. Just let it finish, if no errors are given, your application is now up to date and you can launch it normally.

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
cd Dragons_Maw_Loot_Gen
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

### 5. Run the Application once installed
Once the application has been installed for the first time, you start it again you only need to open a terminal in the `Dragons_Maw_Loot_Gen` directory or cd to it then run the following:
```bash
source venv/bin/activate
python3 app.py
```

---

## Usage
The generator uses loot tables defined in `loot_tables/default.json`. Generated loot is saved in `logs/treasure.csv` which can be imported into a spreadsheet application such as Excel for tracking and analysis. To clear the log file simply delete, move, or rename the `treasure.csv` file and a new one will be created the next time you click the Save to Log button in the UI.

## Customization
1. Make a copy of `default.json` inside the `./loot_tables` directory and name it whatever you want to begin creating your own loot tables.
2. Open the copy you created in any editor program that supports JSON files. [Notepad++](https://notepad-plus-plus.org) is a lightweight free option for Windows systems that is offered under GNU GPL.
The document is arranged for the most part such that tables that lead to another are closer to the top and I've tried to use keys that are descriptive of what they do. 
For example, the first roll when the "Full" mode is selected in the UI occurs on the `loot_tables.primary_treasure_roll` table which is the first one in the document. This roll determines the type of treasure that will be rolled. The `die_size` key determines the size of die to use, `add_level` determines whether or not to add the level as a flat modifier to the roll, the result of the simulated die roll is then compared to the `min` and `max` keys for each entry and the `type` key that matches is returned. By default we use 1d20 unmodified by level for this roll. A result of 1-12 (60%) results in no treasure, 13-17 (25%) results in normal treasure such as coins or art objects, 18-999 (15% when using an unmodified d20) results in advanced treasure which means we move on to the rest of the tables. Mode selector radio buttons exist in the UI to bypass this roll for when you simply want to roll the treasure instead of determining whether there is treasure at all.
When the Advanced Treasure mode is selected or the result of the primary_treasure_roll indicates a result of advanced_treasure, the rest of the tables will be used. In the following order:
    1. **loot_tables.advanced_treasure_roll** - this determines whether the result will be a simple item or if it is allowed to include a prefix and/or suffix. The `die_size` for each entry controls the die size used for the next step.
    2. **loot_tables.base_item_type** - This determines the category of item that is rolled. Notice that each category has a `die_size` and `add_level` key which are used to roll the specific item in the next step these can be safely modified to alter the chance of specific items. They also contain a `ps_die_size` and `ps_mod` which are used in determining any applicable prefix or suffix for the item, caution should be used when modifying these as certain categories of prefixes and suffixes are not appropriate for all item types. For example armor probably shouldn't normally increase the wearer's chance to hit or damage dealt on a successful hit. If you add your own categories, it is recommended that you find an existing category that is comparable and copy the `ps_die_size` and `ps_mod` values from that entry. The `use_prefix` or `use_suffix` keys must be true for both the result from step 1 and step 2 in order for the resulting item to have a prefix or suffix.
    3. **loot_tables.base_items** - This determines the specific item that is found. First we match the result of step 2 with the matching key for it's category, then we find the entry within that table that matches the result of the new die roll. This is where you would most likely be making changes if you want to add, remove, or modify items. Always ensure that the range of `min` and `max` values for any given category has no gaps or overlapping ranges. The last item in a given category should have a high enough max value to ensure that the die roll + level will never be greater than it. I chose 999 which should allow more than enough headroom even if you're playing a system other than AD&D. Notice that some results in the default tables may not even be possible to achieve until a certain level is reached. At `loot_tables.base_item_type.type.armor` you can see that armor uses a 1d20 + level when determining the specific item. At `loot_tables.base_items.armor.full_plate_mail` you can see that Full Plate Mail requires a roll of at least 36 to be found, meaning that it will never show up until players have reached either level 16 or have ventured to level 16 of the dungeon. Depending on your game, you you may want to adjust these values or the die size from the category  (in step 2) if these levels are not expected to be reached and you still want the items to be possible to find. Keep in mind since we are using a simulated die roll, you can use die sizes that you would never find normally such as a 39 sided die.
    4. **loot_tables.modifiers.prefixes_type** & **loot_tables.modifiers.suffixes_type** - Next we determine any applicable prefixes and suffixes for the item. This is handled much the same as step 2 but using the `ps_die_size` and `ps_mod` keys to determine the die roll. There are 2 entries in these tables which have special handling. The first is `cursed` which has a `die_size` value of 0, when the `die_size` of any key within these tables is set to 0, we will reuse the `ps_die_size` and `ps_mod` from step 2 to roll on the next tables to determine the specific prefix or suffix. The 2nd is `capricious` in this case we roll again on the same table using an unmodified d100 until a different result is found. This allows every item type that is capable or rolling the value specified for this result to have a small chance of any prefix or suffix, even those that it would not normally be able to have, so that example of a suit or armor that increases the wearer's chance to hit or damage dealt is possible after all. `capricious` should always be a very rare result to limit the number of these unpredictable items that are present in the game.
    5. **loot_tables.prefixes** & **loot_tables.suffixes** - finally we determine the specific prefix and/or suffix that will be applied to the item. This is handled basically the same as step 3 so I won't go into much detail. Notice that the item from step 3 and the prefixes and suffixes all have an xp and gp value. These are added together to determine the value of the item. If using this app to generate loot for games other than 1st or 2nd edition AD&D, you will almost certainly need to adjust the xp and gp values of items to be appropriate for your system.
    

## License
This project is released under the GPL-3.0 License.
