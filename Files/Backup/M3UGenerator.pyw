import os
import json
import shutil
import sys  # Import sys for restarting the program
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

def save_profile(profile_name, prefix):
    """Save the profile with the given name and prefix."""
    profiles = load_profiles()
    profiles[profile_name] = prefix
    with open("profiles.json", "w") as file:
        json.dump(profiles, file)

def load_profiles():
    """Load the profiles from the profiles.json file."""
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as file:
            return json.load(file)
    return {}

def move_files_and_generate_m3u(directory, files_by_base, prefix="", add_folder_name=False):
    """Move files into separate directories based on M3U names and generate M3U files."""
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

def clean_m3u_files(directory):
    """Remove all .m3u files in the given directory."""
    response = messagebox.askyesno("Confirm Action", "Do you want to delete all .m3u files from the directory?")
    if response:
        removed_files = []
        for filename in os.listdir(directory):
            if filename.endswith(".m3u"):
                os.remove(os.path.join(directory, filename))
                removed_files.append(filename)
        if removed_files:
            messagebox.showinfo("Info", f"Removed the following .m3u files:\n{', '.join(removed_files)}")
        else:
            messagebox.showinfo("Info", "No .m3u files were found in the directory.")

def move_files_to_main_directory(directory):
    """Moves all files from subfolders back to the main directory."""
    move_response = messagebox.askyesno("Move Files", "Would you like to move files back into the script directory?")
    if not move_response:
        return  # Exit if the user chooses "No"

    # Second confirmation: warns user that m3u files will be deleted from subfolders
    delete_m3u_response = messagebox.askyesno("Delete .m3u Files", "This will delete .m3u files in subfolders. Do you want to continue?")
    if not delete_m3u_response:
        return  # Exit if the user chooses "No"

    removed_m3u_files = []
    # First, go through subfolders and delete .m3u files
    for root, dirs, files in os.walk(directory):
        if root != directory:  # Skip the main directory
            for file in files:
                if file.endswith(".m3u"):
                    m3u_path = os.path.join(root, file)
                    os.remove(m3u_path)
                    removed_m3u_files.append(m3u_path)
    if removed_m3u_files:
        messagebox.showinfo("Info", f"Deleted the following .m3u files:\n{', '.join(removed_m3u_files)}")

    # Now move all files from subfolders to the main directory
    subfolders = []
    for root, dirs, files in os.walk(directory):
        if root != directory:
            for file in files:
                shutil.move(os.path.join(root, file), os.path.join(directory, file))
            subfolders.append(root)  # Keep track of the subfolder paths

    messagebox.showinfo("Info", "All files have been moved back into the script directory.")

def delete_empty_subfolders(directory):
    """Delete only empty subfolders in the main directory."""
    warning_response = messagebox.askyesno(
        "Warning",
        "This action will delete all empty subfolders under the script directory and cannot be undone. Do you want to proceed?"
    )
    if not warning_response:
        return  # Exit if the user chooses "No"

    confirm_response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the empty subfolders?")
    if not confirm_response:
        return  # Exit if the user chooses "No"

    for root, dirs, _ in os.walk(directory):
        for subfolder in dirs:
            folder_path = os.path.join(root, subfolder)
            if not os.listdir(folder_path):  # Check if the folder is empty
                try:
                    shutil.rmtree(folder_path)
                except Exception as e:
                    print(f"Could not delete {folder_path}: {e}")

    messagebox.showinfo("Info", "All empty subfolders have been deleted.")

def generate_m3u(directory):
    """Generate M3U files for the given directory."""
    files_by_base = {}

    for filename in os.listdir(directory):
        if "(Disc" in filename or "(Disk" in filename:
            base_name = os.path.splitext(os.path.basename(filename))[0]
            base_name = base_name.split("(Disc")[0].strip()
            base_name = base_name.split("(Disk")[0].strip()

            # Handle revision names
            rev_start = filename.find("(Rev")
            if rev_start != -1:
                rev_end = filename.find(")", rev_start)
                if rev_end != -1:
                    base_name += f" {filename[rev_start:rev_end + 1].strip()}"
            
            if base_name not in files_by_base:
                files_by_base[base_name] = set()
            files_by_base[base_name].add(filename)

    def on_submit():
        """Handle the user's choice and execute the appropriate actions."""
        prefix_choice = var.get()
        prefix = ""
        move_files = False
        add_folder_name = False

        # Handle prefix and file movement options
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
            add_folder_name = messagebox.askyesno("Question", "Do you want to add the folder name to the prefix path?\nThis option is only used for Dolphin.")
            move_files = True
        elif prefix_choice == "6":
            clean_m3u_files(directory)
            return
        elif prefix_choice == "7":
            move_files_to_main_directory(directory)
            return
        elif prefix_choice == "8":
            delete_empty_subfolders(directory)
            return

        if move_files:
            move_files_and_generate_m3u(directory, files_by_base, prefix, add_folder_name)
        else:
            # Generate M3U files without moving them
            for base_name, filenames in files_by_base.items():
                m3u_name = f"{base_name}.m3u"
                with open(m3u_name, 'w') as m3u_file:
                    lines = [prefix + filename for filename in sorted(filenames) if not filename.endswith('.bin')]
                    m3u_file.write("\n".join([line.strip() for line in lines if line.strip()]))

            messagebox.showinfo("Info", "M3U files created.")

    def reload_program():
        """Reload the program by restarting the script."""
        response = messagebox.askyesno("Reload Profiles", "Do you want to restart the script to reload profile dropdown list?")
        if response:
            # Restart the program
            python = sys.executable
            os.execl(python, python, *sys.argv)

    root = tk.Tk()
    root.title("M3U Generator")

    tk.Label(root, text="M3U Tools").pack()

    m3u_frame = tk.Frame(root)
    m3u_frame.pack(pady=10)

    var = tk.StringVar(value="1")
    m3u_options = [
        ("M3U files without folder prefix", "1"),
        ("M3U files with folder prefix", "2"),
        ("Create Profile", "3"),
        ("Use saved profile", "4"),
        ("M3U as directory (ES-DE)", "5")
    ]
    for text, value in m3u_options:
        tk.Radiobutton(m3u_frame, text=text, variable=var, value=value).pack(anchor=tk.W)

    profiles = load_profiles()

    profile_frame = tk.Frame(root)
    profile_frame.pack(pady=5)

    profile_var = tk.StringVar()
    profile_dropdown = ttk.Combobox(profile_frame, textvariable=profile_var)
    profile_dropdown['values'] = list(profiles.keys())
    profile_dropdown.pack(side=tk.LEFT)

    tk.Label(root, text="Folder Cleaning Tools").pack()

    cleaning_frame = tk.Frame(root)
    cleaning_frame.pack(pady=10)

    cleaning_options = [
        ("Clean script directory of .m3u files", "6"),
        ("Move files back to script directory", "7"),
        ("Delete all empty subfolders", "8")
    ]

    for text, value in cleaning_options:
        tk.Radiobutton(cleaning_frame, text=text, variable=var, value=value).pack(anchor=tk.W)

    # Add the reload button to restart the program
    tk.Button(root, text="Reload Profile", command=reload_program).pack(pady=10)

    tk.Button(root, text="Submit", command=on_submit).pack(pady=10)
    root.mainloop()

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Use the script directory as the base directory
generate_m3u(script_directory)
