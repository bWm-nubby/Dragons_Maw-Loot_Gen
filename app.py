import sys
import os

# Add the script's directory to the Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import gradio as gr
import generator 

# Get the list of loot tables once, when the app starts.
available_tables = generator.get_available_loot_tables()

LOG_DIR = 'logs'
LOG_FILE = os.path.join(LOG_DIR, 'treasure.csv')

def generate_loot_wrapper(loot_table_filename, character_level, mode):
    loot_generator = generator.LootGenerator(loot_table_filename, character_level)
    loot_generator.generate(mode)
    return (
        loot_generator.get_user_friendly_log(),
        loot_generator.get_formatted_log(),
        loot_generator.get_user_friendly_csv()
    )

def refresh_loot_tables_list():
    """
    Refreshes the list of available loot tables in the dropdown.
    """
    new_choices = generator.get_available_loot_tables()
    return gr.update(choices=new_choices, value=generator.DEFAULT_LOOT_TABLE)

def save_to_log(csv_data):
    """
    Saves the generated CSV data to a log file.
    """
    if not csv_data or not csv_data.strip():
        return "Nothing to save."

    try:
        # Ensure the log directory exists
        os.makedirs(LOG_DIR, exist_ok=True)
        
        # Check if the file exists to determine if we need to write headers
        file_exists = os.path.isfile(LOG_FILE)
        
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            if not file_exists:
                # Add a header row for new files
                f.write('"Item Name","Effects","XP","GP","Is Cursed"\n')
            
            # The csv_data from generator already includes a newline
            f.write(csv_data)
            
        return f"Successfully saved to {LOG_FILE}"
    except Exception as e:
        print(f"Error saving to log: {e}")
        return f"Error: Could not save to file. Check console for details."

with open("gradio.css", "r") as f:
    css = f.read()

with gr.Blocks(css=css) as demo:
    gr.Markdown("# AD&D Loot Generator")
    
    with gr.Row():
        character_level = gr.Number(
            label="Set Level",
            value=1, 
            step=1, 
            minimum=1,
            scale=1,
        )
        loot_table_dropdown = gr.Dropdown(
            label="Loot Table",
            choices=available_tables,
            value=generator.DEFAULT_LOOT_TABLE,
            scale=6
        )
        refresh_button = gr.Button(
            "🔄", 
            variant="secondary",
            scale=0,
            elem_id="refresh_button",
        )
    
    mode_selection = gr.Radio(
        ["Full", "Force Normal Treasure", "Force Advanced Treasure", "Force Perishable", "Gem Type", "Monstrous Body Part Type"],
        label="Generation Mode",
        value="Full"
    )

    generate_button = gr.Button("Generate Loot!", variant="primary")
    
    with gr.Row():
        with gr.Group(elem_id="item_description_output"):
            output_text_user = gr.Markdown(label="Item Description")
        output_text_dev = gr.Textbox(label="Generation Details", interactive=False, scale=1, lines=24)
    
    csv_textbox = gr.Textbox(
        label="CSV Output", 
        interactive=False, 
        lines=2, 
        elem_id="csv_output_textbox",
        visible=False # This field is now hidden from the user
    )

    with gr.Row():
        save_button = gr.Button("Save To Log", scale=1)
        status_textbox = gr.Textbox(label="Status", interactive=False, scale=3)


    # The click event now calls the wrapper function.
    generate_button.click(
        fn=generate_loot_wrapper,
        inputs=[loot_table_dropdown, character_level, mode_selection],
        outputs=[output_text_user, output_text_dev, csv_textbox]
    )

    # Refresh the available loot tables
    refresh_button.click(
        fn=refresh_loot_tables_list, 
        outputs=[loot_table_dropdown]
    )

    # Wire up the save button
    save_button.click(
        fn=save_to_log,
        inputs=[csv_textbox],
        outputs=[status_textbox]
    )

demo.launch()
