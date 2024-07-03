import os
import json
import shutil
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, ttk

def save_profile(profile_name, prefix):
    profiles = {}
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    profiles[profile_name] = prefix
    with open("profiles.json", "w") as file:
        json.dump(profiles, file)

def load_profiles():
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
        return profiles
    return {}

def move_files_and_generate_m3u(directory, files_by_base, prefix="", add_folder_name=False):
    for base_name, filenames in files_by_base.items():
        m3u_name = f"{base_name}.m3u"
        folder_name = f"{base_name}.m3u"
        os.makedirs(folder_name, exist_ok=True)
        for filename in filenames:
            shutil.move(os.path.join(directory, filename), os.path.join(folder_name, filename))
        with open(os.path.join(folder_name, m3u_name), 'w', newline='\n') as m3u_file:
            lines = []
            for filename in sorted(filenames):
                if filename.endswith('.bin'):
                    continue
                line = prefix if prefix else ""
                if add_folder_name:
                    line += f"{base_name}.m3u/"
                line += filename
                lines.append(line)
            lines = [line.strip() for line in lines if line.strip()]
            if lines:
                m3u_file.write("\n".join(lines))
    messagebox.showinfo("Info", "Files moved into separate directories based on M3U names.")

def generate_m3u(directory):
    files_by_base = {}

    for filename in os.listdir(directory):
        if "(Disc" in filename or "(Disk" in filename:
            base_name = os.path.splitext(os.path.basename(filename))[0]
            base_name = base_name.split("(Disc")[0].strip()
            base_name = base_name.split("(Disk")[0].strip()
            rev_start = filename.find("(Rev")
            if rev_start != -1:
                rev_end = filename.find(")", rev_start)
                if rev_end != -1:
                    revision = filename[rev_start:rev_end + 1].strip()
                    base_name += f" {revision}"
            if "(Rev" in filename:
                if "(Disc" not in filename:
                    continue
            if base_name not in files_by_base:
                files_by_base[base_name] = set()
            files_by_base[base_name].add(filename)

    def on_submit():
        prefix_choice = var.get()
        prefix = ""
        move_files = False
        add_folder_name = False

        if prefix_choice == "1":
            prefix = ""
        elif prefix_choice == "2":
            prefix = simpledialog.askstring("Input", "Enter prefix to add to the beginning of each line:")
        elif prefix_choice == "3":
            prefix = simpledialog.askstring("Input", "Enter prefix to add to the beginning of each line:")
            profile_name = simpledialog.askstring("Input", "Enter a name for this profile:")
            save_profile(profile_name, prefix)
        elif prefix_choice == "4":
            profile_name = profile_var.get()
            prefix = profiles.get(profile_name, "")
        elif prefix_choice == "5":
            prefix = simpledialog.askstring("Input", "Enter prefix to add to the beginning of each line:")
            add_folder_name_choice = messagebox.askyesno("Question", "Do you want to add the folder name to the prefix path?")
            add_folder_name = add_folder_name_choice
            move_files = True
        
        if not prefix:
            prefix = ""

        if move_files:
            move_files_and_generate_m3u(directory, files_by_base, prefix, add_folder_name)
        else:
            for base_name, filenames in files_by_base.items():
                m3u_name = f"{base_name}.m3u"
                with open(m3u_name, 'w', newline='\n') as m3u_file:
                    lines = [filename for filename in sorted(filenames) if not filename.endswith('.bin')]
                    lines = [prefix + line for line in lines]
                    lines = [line.strip() for line in lines if line.strip()]
                    if lines:
                        m3u_file.write("\n".join(lines))
            messagebox.showinfo("Info", "M3U files created.")

    def reload_profiles():
        profiles = load_profiles()
        profile_dropdown['values'] = list(profiles.keys())

    root = tk.Tk()
    root.title("M3U Generator")

    tk.Label(root, text="Select an option:").pack()

    var = tk.StringVar(value="1")
    options = [
        ("M3U files without prefix", "1"),
        ("M3U files with prefix", "2"),
        ("Create profile", "3"),
        ("Use profile", "4"),
        ("M3U as directory (ES-DE)", "5")
    ]

    for text, value in options:
        tk.Radiobutton(root, text=text, variable=var, value=value).pack(anchor=tk.W)

    profiles = load_profiles()
    
    profile_frame = tk.Frame(root)
    profile_frame.pack()

    tk.Label(profile_frame, text="Select profile:").pack(side=tk.LEFT)
    profile_var = tk.StringVar()
    profile_dropdown = ttk.Combobox(profile_frame, textvariable=profile_var)
    profile_dropdown['values'] = list(profiles.keys())
    profile_dropdown.pack(side=tk.LEFT)

    tk.Button(root, text="Submit", command=on_submit).pack()
    tk.Button(root, text="Reload Profiles", command=reload_profiles).pack()

    root.mainloop()

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Use the script directory as the base directory
generate_m3u(script_directory)
