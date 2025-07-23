import random
import json
import os
from typing import Optional, Dict, Any, Union, List

script_dir = os.path.dirname(os.path.abspath(__file__))
LOOT_TABLES_DIR = os.path.join(script_dir, 'loot_tables')
DEFAULT_LOOT_TABLE = 'default.json'


# populate list of .json files to be used to populate the gradio dropdown.
def get_available_loot_tables() -> list[str]:
    if not os.path.isdir(LOOT_TABLES_DIR):
        print(f"Warning: Loot tables directory not found at {LOOT_TABLES_DIR}")
        return [DEFAULT_LOOT_TABLE]
    
    files = [f for f in os.listdir(LOOT_TABLES_DIR) if f.endswith('.json')]
    
    # Ensure 'default.json' is always first in the list if it exists
    if DEFAULT_LOOT_TABLE in files:
        files.remove(DEFAULT_LOOT_TABLE)
        files.insert(0, DEFAULT_LOOT_TABLE)
        
    return files


# load the loot table to be used elsewhere
def load_loot_tables(filename: str = DEFAULT_LOOT_TABLE) -> Dict[str, Any]:
    path_to_load = os.path.join(LOOT_TABLES_DIR, filename)

    try:
        with open(path_to_load, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Loot table file not found at: {path_to_load}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in file: {path_to_load}. Error: {e}")


# Represents a single entry from a loot table's 'type' dictionary, providing convenient attribute access to its properties.
class LootTable:
    def __init__(self, entry_key: str, entry_data: Dict[str, Any]):
        self.key: str = entry_key # The original key, e.g., "no_treasure"
        self.min: Optional[int] = entry_data.get('min')
        self.max: Optional[int] = entry_data.get('max')
        self.name: Optional[str] = entry_data.get('name') # User-friendly name
        self.description: Optional[str] = entry_data.get('description')
        
        die_size_val = entry_data.get('die_size')
        self.die_size: Optional[int] = int(die_size_val) if die_size_val is not None else None
        
        self.mod: Optional[int] = entry_data.get('mod')
        self.add_level: Optional[bool] = entry_data.get('add_level')
        self.ps_die_size: Optional[int] = entry_data.get('ps_die_size')
        self.ps_mod: Optional[int] = entry_data.get('ps_mod')
        self.use_prefix: Optional[bool] = entry_data.get('use_prefix')
        self.use_suffix: Optional[bool] = entry_data.get('use_suffix')
        self._raw_data: dict = entry_data # Store original data for access to other keys

    def __repr__(self) -> str:
        return f"<LootTable key='{self.key}', name='{self.name}'>"


class LootGenerator:
    def __init__(self, loot_table_name: str, set_level: int):
        self.loot_table = load_loot_tables(loot_table_name)
        self.set_level = set_level
        self.results_log: List[Dict[str, Any]] = []

    def _roll_and_log(self, die_size: int, description: str) -> int:
        roll = random.randint(1, die_size)
        self.results_log.append({"description": description, "roll": roll, "die_size": die_size})
        return roll

    def PrimaryTreasureRoller(self) -> tuple[Union[LootTable, str], int]:
        primary_treasure_data = self.loot_table['loot_tables']['primary_treasure_roll']
        primary_treasure_types = primary_treasure_data['type']
        die_size = primary_treasure_data.get('die_size')
        add_level = primary_treasure_data.get('add_level', False)

        if die_size is None:
            raise ValueError("primary_treasure_roll entry in the loot table requires a 'die_size' to be defined.")

        primary_roll = self._roll_and_log(die_size, "Primary Treasure Roll")
        if add_level is True:
            original_roll = primary_roll
            primary_roll += self.set_level
            self.results_log.append({
                "description": "Primary Treasure Roll with level mod",
                "value": f"{original_roll} + {self.set_level} = {primary_roll}"
            })

        for entry_key, entry_data in primary_treasure_types.items():
            loot_table_entry = LootTable(entry_key, entry_data)
            min_val = loot_table_entry.min
            max_val = loot_table_entry.max

            if min_val is not None and max_val is not None and min_val <= primary_roll <= max_val:
                return loot_table_entry, primary_roll

        return 'Roll outside expected range.', primary_roll

    def NormalTreasureRoller(self, normal_treasure_data: Dict[str, Any]) -> int:
        die_size = normal_treasure_data.get('die_size')
        mod = normal_treasure_data.get('mod', 0)
        mult_level = normal_treasure_data.get('mult_level', False)

        if die_size is None:
            raise ValueError("normal_treasure entry in the loot table requires a 'die_size' to be defined.")

        normal_roll = self._roll_and_log(die_size, "Normal Treasure Roll")

        if mult_level is True:
            return normal_roll * self.set_level + mod
        else:
            return normal_roll + mod
        
    def AdvancedTreasureRoller(self) -> tuple[Union[LootTable, str], int, int, bool, bool]:
        advanced_treasure_data = self.loot_table['loot_tables']['advanced_treasure_roll']
        advanced_treasure_types = advanced_treasure_data['type']
        die_size = advanced_treasure_data.get('die_size')
        add_level = advanced_treasure_data.get('add_level', False)

        if die_size is None:
            raise ValueError("advanced_treasure_roll entry in the loot table requires a 'die_size' to be defined.")
        
        advanced_roll = self._roll_and_log(die_size, "Advanced Treasure Roll")
        if add_level:
            original_roll = advanced_roll
            advanced_roll += self.set_level
            self.results_log.append({
                "description": "Advanced Treasure Roll with level mod",
                "value": f"{original_roll} + {self.set_level} = {advanced_roll}"
            })

        for entry_key, entry_data in advanced_treasure_types.items():
            loot_table_entry = LootTable(entry_key, entry_data)
            min_val = loot_table_entry.min
            max_val = loot_table_entry.max
            type_die_size = loot_table_entry.die_size
            type_prefix = loot_table_entry.use_prefix
            type_suffix = loot_table_entry.use_suffix

            if min_val is not None and max_val is not None and min_val <= advanced_roll <= max_val:
                return loot_table_entry, advanced_roll, type_die_size, type_prefix, type_suffix

        return 'Roll outside expected range.', advanced_roll, 0, False, False

    def BaseItemTypeRoller(self, type_die_size: int) -> tuple[Union[LootTable, str], int]:
        base_item_type_data = self.loot_table['loot_tables']['base_item_type']
        base_item_type_types = base_item_type_data['type']
        item_die_size = base_item_type_data.get('die_size')
        item_add_level = base_item_type_data.get('add_level', False)
        item_ps_die_size = base_item_type_data.get('ps_die_size')
        item_ps_mod = base_item_type_data.get('ps_mod', 0)
        item_use_prefix = base_item_type_data.get('use_prefix', False)
        item_use_suffix = base_item_type_data.get('use_suffix', False)

        if type_die_size is None:
            raise ValueError("All type keys under advanced_treasure_roll in the loot table require a 'die_size' to be defined.")

        base_item_type_roll = self._roll_and_log(type_die_size, "Base Item Type Roll")

        for entry_key, entry_data in base_item_type_types.items():
            loot_table_entry = LootTable(entry_key, entry_data)
            min_val = loot_table_entry.min
            max_val = loot_table_entry.max

            if min_val is not None and max_val is not None and min_val <= base_item_type_roll <= max_val:
                return loot_table_entry, base_item_type_roll

        return 'Roll outside expected range.', base_item_type_roll
    
    def BaseItemRoller(self, item_type_result: LootTable) -> tuple[Union[LootTable, str], int]:
        base_item_category = item_type_result.key
        die_size = item_type_result.die_size
        add_level = item_type_result.add_level


        if base_item_category not in self.loot_table['loot_tables']['base_items']:
            return f"Base item category '{base_item_category}' not found in loot tables.", 0

        base_item_table = self.loot_table['loot_tables']['base_items'][base_item_category]

        if die_size is None:
            raise ValueError(f"Base item type '{base_item_category}' requires a 'die_size'.")

        roll = self._roll_and_log(die_size, f"Base Item Roll for {item_type_result.name}")

        if add_level:
            original_roll = roll
            roll += self.set_level
            self.results_log.append({
                "description": f"Base Item Roll for {item_type_result.name} with level mod",
                "value": f"{original_roll} + {self.set_level} = {roll}"
            })

        for item_key, item_data in base_item_table.items():
            loot_table_entry = LootTable(item_key, item_data)
            min_val = loot_table_entry.min
            max_val = loot_table_entry.max

            if min_val is not None and max_val is not None and min_val <= roll <= max_val:
                self.results_log.append({
                    "description": "Base Item",
                    "value": loot_table_entry.name,
                    "effect": loot_table_entry._raw_data.get('effect', ''),
                    "xp": loot_table_entry._raw_data.get('xp', 0),
                    "gp": loot_table_entry._raw_data.get('gp', 0)
                })
                return loot_table_entry, roll

        return 'Roll outside expected range.', roll

    def GemTypeRoller(self) -> tuple[Union[LootTable, str], int]:
        gem_type_data = self.loot_table['gems']
        die_size = gem_type_data.get('die_size')

        if die_size is None:
            raise ValueError("gems entry in the loot table requires a 'die_size' to be defined.")

        roll = self._roll_and_log(die_size, "Gem Type Roll")

        for entry_key, entry_data in gem_type_data.items():
            if entry_key == 'die_size':
                continue

            loot_table_entry = LootTable(entry_key, entry_data)
            min_val = loot_table_entry.min
            max_val = loot_table_entry.max

            if min_val is not None and max_val is not None and min_val <= roll <= max_val:
                return loot_table_entry, roll

        return 'Roll outside expected range.', roll

    def BodyPartRoller(self) -> tuple[Union[LootTable, str], int]:
        body_part_data = self.loot_table['monstrous_body_part']
        die_size = body_part_data.get('die_size')

        if die_size is None:
            raise ValueError("monstrous_body_part entry in the loot table requires a 'die_size' to be defined.")

        roll = self._roll_and_log(die_size, "Body Part Roll")

        for entry_key, entry_data in body_part_data.items():
            if entry_key == 'die_size':
                continue

            loot_table_entry = LootTable(entry_key, entry_data)
            min_val = loot_table_entry.min
            max_val = loot_table_entry.max

            if min_val is not None and max_val is not None and min_val <= roll <= max_val:
                return loot_table_entry, roll

        return 'Roll outside expected range.', roll
    
    def AffixTypeRoller(self, adv_result: LootTable, item_type_result: LootTable) -> None:
        def _roll_and_apply_affix(is_prefix: bool):
            affix_type_str = "prefixes" if is_prefix else "suffixes"
            log_affix_type = "Prefix" if is_prefix else "Suffix"
            affix_type_roll_table = self.loot_table['modifiers'][f'{affix_type_str}_type']

            # Start with values from BaseItemRoller
            current_die_size = item_type_result.ps_die_size
            current_mod = item_type_result.ps_mod

            final_affix_type = None

            while True:
                if current_die_size is None:
                    return

                unmodified_roll = self._roll_and_log(current_die_size, f"{log_affix_type} Type Roll")
                modified_roll = unmodified_roll + current_mod

                # Log both unmodified and modified roll
                self.results_log.append({
                    "description": f"{log_affix_type} Type Roll (raw)",
                    "roll": unmodified_roll,
                    "die_size": current_die_size
                })
                self.results_log.append({
                    "description": f"{log_affix_type} Type Roll (modified)",
                    "value": f"{unmodified_roll} + {current_mod} = {modified_roll}"
                })

                chosen_type = None
                for _, data in affix_type_roll_table.items():
                    if data['min'] <= modified_roll <= data['max']:
                        chosen_type = data
                        break

                if not chosen_type:
                    return

                if chosen_type['name'].lower() == 'capricious':
                    self.results_log.append({"description": "Capricious reroll", "value": f"Rerolling for {log_affix_type}"})
                    current_die_size = chosen_type['die_size']
                    current_mod = chosen_type['add_level']
                else:
                    final_affix_type = chosen_type
                    break

            # Correctly determine die_size and mod for AffixRoller
            if final_affix_type['name'].lower() == 'cursed':
                property_roll_die_size = item_type_result.ps_die_size
                property_roll_mod = item_type_result.ps_mod
            else:
                property_roll_die_size = final_affix_type['die_size']
                property_roll_mod = 0  # Default to 0
                if final_affix_type.get('add_level', False):
                    property_roll_mod = self.set_level

            if property_roll_die_size == 0:
                self.results_log.append({
                    "description": f"Special handling for {final_affix_type['name']}",
                    "value": "Using BaseItemRoller values for affix property roll."
                })
                property_roll_die_size = item_type_result.ps_die_size
                property_roll_mod = item_type_result.ps_mod
            
            self.AffixRoller(is_prefix, final_affix_type, property_roll_die_size, property_roll_mod)
            self.results_log.append({"description": f"{log_affix_type} Type", "value": final_affix_type['name']})

        # Check for prefix
        if adv_result.use_prefix and item_type_result.use_prefix:
            _roll_and_apply_affix(is_prefix=True)

        # Check for suffix
        if adv_result.use_suffix and item_type_result.use_suffix:
            _roll_and_apply_affix(is_prefix=False)
        
    def AffixRoller(self, is_prefix: bool, affix_type_info: Dict[str, Any], die_size: int, mod: int) -> Optional[str]:
        """
        Rolls for a specific affix (prefix or suffix) based on the type and roll parameters.
        Returns the key of the rolled affix.
        """
        affix_kind = "prefixes" if is_prefix else "suffixes"
        log_kind = "Prefix" if is_prefix else "Suffix"

        # Find the key for the affix type by looking up its name in the type table.
        affix_type_roll_table = self.loot_table['modifiers'][f'{affix_kind}_type']
        affix_table_key = None
        for key, data in affix_type_roll_table.items():
            if data['name'] == affix_type_info['name']:
                affix_table_key = key
                break
        
        if affix_table_key is None:
            self.results_log.append({"description": f"Could not find affix type key for name", "value": affix_type_info['name']})
            return None

        affix_tables = self.loot_table['modifiers'][affix_kind]

        if affix_table_key not in affix_tables:
            self.results_log.append({"description": f"Affix table not found", "value": affix_table_key})
            return None

        property_table = affix_tables[affix_table_key]
        
        if die_size is None:
            return None

        roll = self._roll_and_log(die_size, f"{log_kind} Roll")
        modified_roll = roll + mod
        
        self.results_log.append({
            "description": f"{log_kind} Roll (modified)",
            "value": f"{roll} + {mod} = {modified_roll}"
        })

        for key, data in property_table.items():
            if data['min'] <= modified_roll <= data['max']:
                self.results_log.append({
                    "description": f"{log_kind}",
                    "value": data['name'],
                    "effect": data.get('effect', ''),
                    "xp": data.get('xp', 0),
                    "gp": data.get('gp', 0)
                })
                return key
        
        return None
        

    def generate(self, mode: str = "Full") -> None:
        if mode == "Full":
            result, roll = self.PrimaryTreasureRoller()
        elif mode == "Force Normal Treasure":
            result = LootTable("normal_treasure", self.loot_table['loot_tables']['primary_treasure_roll']['type']['normal_treasure'])
        elif mode == "Force Advanced Treasure":
            result = LootTable("advanced_treasure", self.loot_table['loot_tables']['primary_treasure_roll']['type']['advanced_treasure'])
        elif mode == "Force Perishable":
            result = LootTable("advanced_treasure", self.loot_table['loot_tables']['primary_treasure_roll']['type']['advanced_treasure'])
        elif mode == "Gem Type":
            gem_result, gem_roll = self.GemTypeRoller()
            if isinstance(gem_result, LootTable):
                self.results_log.append({"description": "Gem Type", "value": gem_result.name})
            else:
                self.results_log.append({"description": "Gem Type", "value": gem_result})
            return
        elif mode == "Monstrous Body Part Type":
            body_part_result, body_part_roll = self.BodyPartRoller()
            if isinstance(body_part_result, LootTable):
                self.results_log.append({"description": "Monstrous Body Part", "value": body_part_result.name})
            else:
                self.results_log.append({"description": "Monstrous Body Part", "value": body_part_result})
            return

        if isinstance(result, LootTable):
            if result.key == 'normal_treasure':
                gold_amount = self.NormalTreasureRoller(result._raw_data)
                self.results_log.append({"description": "Total Gold", "value": gold_amount})
            elif result.key == 'advanced_treasure':
                if mode == "Force Perishable":
                    adv_result = LootTable("prefix_base_item_suffix", self.loot_table['loot_tables']['advanced_treasure_roll']['type']['prefix_base_item_suffix'])
                    type_die_size = adv_result.die_size
                else:
                    adv_result, adv_roll, type_die_size, use_prefix, use_suffix = self.AdvancedTreasureRoller()
                
                if isinstance(adv_result, LootTable):
                    self.results_log.append({"description": "Advanced Treasure Result", "value": adv_result.name})
                    if mode == "Force Perishable":
                        item_type_result = LootTable("perishables", self.loot_table['loot_tables']['base_item_type']['type']['perishables'])
                    else:
                        item_type_result, item_type_roll = self.BaseItemTypeRoller(type_die_size)

                    if isinstance(item_type_result, LootTable):
                        self.results_log.append({"description": "Base Item Type", "value": item_type_result.name})
                        base_item_result, base_item_roll = self.BaseItemRoller(item_type_result)
                        if isinstance(base_item_result, LootTable):
                            self.results_log.append({"description": "Base Item", "value": base_item_result.name})
                            self.AffixTypeRoller(adv_result, item_type_result)
                        else:
                            self.results_log.append({"description": "Base Item", "value": base_item_result})
                    else:
                        self.results_log.append({"description": "Base Item Type", "value": item_type_result})
                else:
                    self.results_log.append({"description": "Advanced Treasure Result", "value": adv_result})


    def get_formatted_log(self) -> str:
        log_entries = []
        for entry in self.results_log:
            if "roll" in entry:
                log_entries.append(f"{entry['description']}: Rolled {entry['roll']} (1d{entry['die_size']})")
            elif "effect" in entry:
                # Skip user-friendly entries in the detailed log
                pass
            else:
                log_entries.append(f"{entry['description']}: {entry['value']}")
        return "\n".join(log_entries)

    def get_user_friendly_log(self) -> str:
        item_name = ""
        prefix = ""
        suffix = ""
        effects = []
        total_xp = 0
        total_gp = 0
        is_cursed_item = False

        for entry in self.results_log:
            if entry['description'] == "Base Item":
                item_name = entry['value']
                if entry.get('effect'):
                    effects.append({"name": entry['description'], "effect": entry['effect']})
                total_xp += entry.get('xp', 0)
                total_gp += entry.get('gp', 0)
            elif entry['description'] == "Prefix":
                prefix = entry['value']
                if entry.get('effect'):
                    effects.append({"name": entry['description'], "effect": entry['effect']})
                total_xp += entry.get('xp', 0)
                total_gp += entry.get('gp', 0)
            elif entry['description'] == "Suffix":
                suffix = entry['value']
                if entry.get('effect'):
                    effects.append({"name": entry['description'], "effect": entry['effect']})
                total_xp += entry.get('xp', 0)
                total_gp += entry.get('gp', 0)
            elif entry['description'] in ("Gem Type", "Monstrous Body Part"):
                item_name = entry['value']
            elif entry.get('description') in ("Prefix Type", "Suffix Type") and entry.get('value').lower() == 'cursed':
                is_cursed_item = True

        full_item_name = f"{prefix} {item_name} {suffix}".strip()

        log_str = f"<span style='font-size:1.5em; font-weight:bold;'>Item Name: {full_item_name}</span><br>"
        log_str += "<hr>"
        if is_cursed_item:
            log_str += "<span style='font-size:1.2em;'> Cursed Item</span><br>"
            log_str += "<br>"
        log_str += "<span style='font-size:1.2em; font-weight:bold;'>Effects:</span><br>"       
        if effects:
            log_str += "<ul>"
            for effect in effects:
                log_str += f"<li style='font-size:1em;'>{effect['name']}: {effect['effect']}</li>"
            log_str += "</ul>"
        log_str += "<hr>"
        log_str += f"<span style='font-size:1.1em;'>XP: {total_xp}</span><br>"
        log_str += f"<span style='font-size:1.1em;'>GP: {total_gp}</span><br>"

        return log_str
    
    def get_user_friendly_csv(self) -> str:
        item_name = ""
        prefix = ""
        suffix = ""
        effects = []
        total_xp = 0
        total_gp = 0
        is_cursed_item = False
    
        for entry in self.results_log:
            if entry['description'] == "Base Item":
                item_name = entry['value']
                if entry.get('effect'):
                    effects.append({"name": entry['description'], "effect": entry['effect']})
                total_xp += entry.get('xp', 0)
                total_gp += entry.get('gp', 0)
            elif entry['description'] == "Prefix":
                prefix = entry['value']
                if entry.get('effect'):
                    effects.append({"name": entry['description'], "effect": entry['effect']})
                total_xp += entry.get('xp', 0)
                total_gp += entry.get('gp', 0)
            elif entry['description'] == "Suffix":
                suffix = entry['value']
                if entry.get('effect'):
                    effects.append({"name": entry['description'], "effect": entry['effect']})
                total_xp += entry.get('xp', 0)
                total_gp += entry.get('gp', 0)
            elif entry['description'] in ("Gem Type", "Monstrous Body Part"):
                item_name = entry['value']
            elif entry.get('description') in ("Prefix Type", "Suffix Type") and entry.get('value').lower() == 'cursed':
                is_cursed_item = True
    
        full_item_name = f"{prefix} {item_name} {suffix}".strip()
        effects_str = "; ".join([f"{e['name']}: {e['effect']}" for e in effects])
    
        # CSV header and row
        csv_str = f'"{full_item_name}","{effects_str}",{total_xp},{total_gp},{is_cursed_item}\n'
        return csv_str
