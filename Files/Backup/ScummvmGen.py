import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to parse the ScummVM.dat file
def parse_scummvm_dat(filepath):
    games = []
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
        game_entries = re.findall(r'<game>\s*name "(.*?)"\s*code "(.*?)"\s*</game>', content)
        for name, code in game_entries:
            games.append((name, code))
    return games

# Function to sanitize filenames
def sanitize_filename(name):
    contains_non_ascii = not name.isascii()
    
    # Log original name if it contains illegal characters or non-ASCII characters
    if re.search(r'[\\/*?:"<>|{}]', name) or contains_non_ascii:
        log_warning(f"Name contains illegal or non-ASCII characters: {name}")
    
    # Remove illegal characters
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    # Remove characters within curly braces
    name = re.sub(r'{.*?}', '', name)
    # Remove non-ASCII characters
    sanitized_name = ''.join(c for c in name if c.isascii())
    
    return sanitized_name.strip(), contains_non_ascii  # Return sanitized name and flag

# Function to create .dpt files
def create_daijishou_files(games):
    filenames = {}
    for name, code in games:
        sanitized_name, contains_non_ascii = sanitize_filename(name)
        filename = f'{sanitized_name}.dpt'
        if sanitized_name in filenames:
            filename = f'{sanitized_name}-{code.split("-")[-1]}.dpt'
        filenames[sanitized_name] = code
        content = f"# Daijishou Player Template\n[scummvm_id] {code}\n...\n"
        write_to_file(filename, content, contains_non_ascii)

# Function to create .scummvm files
def create_scummvm_files(games):
    filenames = {}
    for name, code in games:
        sanitized_name, contains_non_ascii = sanitize_filename(name)
        filename = f'{sanitized_name}.scummvm'
        if sanitized_name in filenames:
            filename = f'{sanitized_name}-{code.split("-")[-1]}.scummvm'
        filenames[sanitized_name] = code
        content = f'{code}\n'
        write_to_file(filename, content, contains_non_ascii)

# Function to write content to a file in the output directory
def write_to_file(filename, content, contains_non_ascii):
    output_dir = os.path.join(script_dir, 'scummvm')
    if contains_non_ascii:
        output_dir = os.path.join(output_dir, 'Non-ASCII')
    
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        log_error(f"Error writing file {filename}: {str(e)}")

# Function to log errors
def log_error(message):
    with open(os.path.join(script_dir, 'output.txt'), 'a', encoding='utf-8') as error_log:
        error_log.write(message + '\n')

# Function to log warnings
def log_warning(message):
    with open(os.path.join(script_dir, 'warnings.txt'), 'a', encoding='utf-8') as warning_log:
        warning_log.write(message + '\n')

# Function to handle button clicks
def on_button_click(option):
    filepath = filedialog.askopenfilename(filetypes=[("DAT Files", "*.dat")])
    if filepath:
        try:
            games = parse_scummvm_dat(filepath)
            if option == 'daijishou':
                create_daijishou_files(games)
            elif option == 'esde' or option == 'retroarch':
                create_scummvm_files(games)
            messagebox.showinfo("Success", f"Files created successfully in {os.path.join(script_dir, 'scummvm')}")
        except Exception as e:
            log_error(f"Error processing file {filepath}: {str(e)}")

# GUI setup
script_dir = os.path.dirname(os.path.abspath(__file__))
root = tk.Tk()
root.title("ScummVM File Generator")

tk.Button(root, text="Create Daijishou scummvm .dpt files", command=lambda: on_button_click('daijishou')).pack(pady=10)
tk.Button(root, text="Create ES-DE scummvm .scummvm files", command=lambda: on_button_click('esde')).pack(pady=10)
tk.Button(root, text="Create RetroArch scummvm .scummvm files", command=lambda: on_button_click('retroarch')).pack(pady=10)

root.mainloop()
