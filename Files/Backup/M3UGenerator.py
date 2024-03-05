import os
import json

def save_profile(profile_name, prefix):
    profiles = {}
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    profiles[profile_name] = prefix
    with open("profiles.json", "w") as file:
        json.dump(profiles, file)

def load_profile(profile_name):
    profiles = {}
    if os.path.exists("profiles.json"):
        with open("profiles.json", "r") as file:
            profiles = json.load(file)
    return profiles.get(profile_name, "")

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

    prefix_choice = input("Type 1 to manually enter prefix\nType 2 to enter a prefix and save as profile\nType 3 and profile name to use profile prefix\nType 4 to not include prefix:\n")

    prefix = ""
    if prefix_choice == "1":
        prefix = input("Enter prefix to add to the beginning of each line: ")
        profile_name = input("Enter a name for this profile: ")
        save_profile(profile_name, prefix)
    elif prefix_choice == "2":
        prefix = input("Enter prefix to add to the beginning of each line: ")
        profile_name = input("Enter a name for this profile: ")
        save_profile(profile_name, prefix)
    elif prefix_choice.startswith("3 "):
        profile_name = prefix_choice[2:]
        prefix = load_profile(profile_name)
    elif prefix_choice == "4":
        prefix = ""

    created_files = []

    for base_name, filenames in files_by_base.items():
        m3u_name = f"{base_name}.m3u"
        with open(m3u_name, 'w') as m3u_file:
            lines = [prefix + filename for filename in sorted(filenames)]
            lines = [line.strip() for line in lines if line.strip()]  # Remove empty lines
            if lines:  # Only create M3U file if there are non-empty lines
                m3u_file.write("\n".join(lines))
                created_files.append(m3u_name)

    if created_files:
        print("Files created:")
        for created_file in created_files:
            print(created_file)
    else:
        print("No files matching the criteria found.")

    input("Press Enter to close the dialog.")

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Use the script directory as the base directory
generate_m3u(script_directory)
