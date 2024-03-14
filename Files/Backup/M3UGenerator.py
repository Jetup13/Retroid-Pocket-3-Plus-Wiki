import os
import json
import shutil

def save_profile(profile_name, prefix):
    profiles = {}
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    profiles[profile_name] = prefix
    with open("profiles.json", "w") as file:
        json.dump(profiles, file)

def load_profile(profile_name):
    with open("profiles.json", "r") as file:
        profiles = json.load(file)
    return profiles.get(profile_name, "")

def move_files_and_generate_m3u(directory, files_by_base, prefix="", add_folder_name=False):
    for base_name, filenames in files_by_base.items():
        m3u_name = f"{base_name}.m3u"
        folder_name = f"{base_name}.m3u"  # Append .m3u to folder name
        os.makedirs(folder_name, exist_ok=True)
        for filename in filenames:
            shutil.move(os.path.join(directory, filename), os.path.join(folder_name, filename))
        with open(os.path.join(folder_name, m3u_name), 'w', newline='\n') as m3u_file:
            lines = []
            for filename in sorted(filenames):
                if filename.endswith('.bin'):
                    continue
                line = prefix
                if add_folder_name:
                    line += f"{base_name}.m3u/"
                line += filename
                lines.append(line)
            lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines
            if lines:  # Only create M3U file if there are non-empty lines
                m3u_file.write("\n".join(lines))
    print("Files moved into separate directories based on M3U names.")
    input("Press Enter to close the dialog.")

def generate_m3u(directory):
    files_by_base = {}

    for filename in os.listdir(directory):
        if "(Disc" in filename or "(Disk" in filename:
            base_name = os.path.splitext(os.path.basename(filename))[0]
            base_name = base_name.split("(Disc")[0].strip()  # Remove "(Disc" and trim spaces
            base_name = base_name.split("(Disk")[0].strip()  # Remove "(Disk" and trim spaces

            # Extract revision number
            rev_start = filename.find("(Rev")
            if rev_start != -1:
                rev_end = filename.find(")", rev_start)
                if rev_end != -1:
                    revision = filename[rev_start:rev_end + 1].strip()
                    base_name += f" {revision}"

            if "(Rev" in filename:
                if "(Disc" not in filename:
                    continue  # Skip files with "(Rev" but without "(Disc"
                
            if base_name not in files_by_base:
                files_by_base[base_name] = set()

            files_by_base[base_name].add(filename)

    prefix_choice = input("Type 1 to not include prefix\nType 2 to manually enter prefix\nType 3 to enter a prefix and save as profile\nType 4 and profile name to use profile prefix\nType 5 to move files into separate directories based on M3U names:\n")

    if prefix_choice == "1":
        prefix = ""
        move_files = False
        add_folder_name = False
    elif prefix_choice == "2":
        prefix = input("Enter prefix to add to the beginning of each line: ")
        move_files = False
        add_folder_name = False
    elif prefix_choice == "3":
        prefix = input("Enter prefix to add to the beginning of each line: ")
        profile_name = input("Enter a name for this profile: ")
        save_profile(profile_name, prefix)
        move_files = False
        add_folder_name = False
    elif prefix_choice.startswith("4 "):
        profile_name = prefix_choice[2:]
        prefix = load_profile(profile_name)
        move_files = False
        add_folder_name = False
    elif prefix_choice == "5":
        prefix = input("Enter prefix to add to the beginning of each line: ")
        add_folder_name_choice = input("Do you want to add the folder name to the prefix path? (Y/N): ").lower()
        add_folder_name = add_folder_name_choice == "y"
        move_files = True
    else:
        prefix = ""
        move_files = False
        add_folder_name = False

    if move_files:
        move_files_and_generate_m3u(directory, files_by_base, prefix, add_folder_name)
    else:
        for base_name, filenames in files_by_base.items():
            m3u_name = f"{base_name}.m3u"
            with open(m3u_name, 'w', newline='\n') as m3u_file:
                lines = [filename for filename in sorted(filenames) if not filename.endswith('.bin')]
                lines = [prefix + line for line in lines]  # Add prefix to each line
                lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines
                if lines:  # Only create M3U file if there are non-empty lines
                    m3u_file.write("\n".join(lines))

        print("Files created:")
        for base_name in files_by_base.keys():
            print(f"{base_name}.m3u")

        input("Press Enter to close the dialog.")

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Use the script directory as the base directory
generate_m3u(script_directory)
