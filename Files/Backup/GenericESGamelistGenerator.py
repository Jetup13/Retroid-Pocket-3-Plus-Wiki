import os
from xml.dom import minidom

def confirm_action(prompt):
    while True:
        user_input = input(f"{prompt} (Press Enter to confirm, or Esc to cancel): ").lower()
        if user_input == '':
            return True
        elif user_input == '\x1b':  # Check for Escape key (ASCII code)
            return False
        else:
            print("Invalid input. Please press Enter or Esc.")

def create_gamelist():
    script_folder = os.path.dirname(os.path.realpath(__file__))
    rom_folder = script_folder  # Use the script's folder as the ROM folder
    xml_file_path = os.path.join(script_folder, 'gamelist.xml')

    # Confirm before deleting existing gamelist.xml if it exists
    if os.path.exists(xml_file_path):
        if not confirm_action("Existing 'gamelist.xml' found. Do you want to delete it?"):
            print("Operation canceled. Press Enter to exit.")
            input()
            return
        os.remove(xml_file_path)
        print("Deleted existing gamelist.xml")

    # Create gamelist.xml or update if it doesn't exist
    root = minidom.Document()
    game_list = root.createElement('gameList')
    root.appendChild(game_list)

    # Get user input for ROM extensions
    user_input = input("Enter ROM extensions (separated by commas): ")
    rom_extensions = [ext.strip() for ext in user_input.split(',')]

    # Flag to check if any ROMs were added
    roms_added = False

    print("Searching for files with extensions:", rom_extensions)

    for file_name in os.listdir(rom_folder):
        file_path = os.path.join(rom_folder, file_name)

        # Check if the file is a ROM file and matches the specified extensions
        if os.path.isfile(file_path) and file_name.lower().endswith(tuple(rom_extensions)):
            print("Found matching file:", file_name)
            
            roms_added = True
            game_elem = root.createElement('game')

            # Add path
            path_elem = root.createElement('path')
            path_elem.appendChild(root.createTextNode(f'./{file_name}'))
            game_elem.appendChild(path_elem)

            # Extract name from file name
            name_elem = root.createElement('name')
            name_elem.appendChild(root.createTextNode(''.join([c for c in file_name.split('(')[0].strip()])))
            game_elem.appendChild(name_elem)

            # Add image path
            image_elem = root.createElement('image')
            image_elem.appendChild(root.createTextNode(f'./media/box2dfront/{os.path.splitext(file_name)[0]}.png'))
            game_elem.appendChild(image_elem)

            game_list.appendChild(game_elem)

    if not roms_added:
        print("No new ROMs added. Press Enter to exit.")
        input()
        return

    # Write to gamelist.xml with formatting
    with open(xml_file_path, 'wb') as file:
        file.write(root.toprettyxml(indent="    ").encode('utf-8'))

    print("Script executed successfully. Press Enter to exit.")
    input()

if __name__ == "__main__":
    create_gamelist()
