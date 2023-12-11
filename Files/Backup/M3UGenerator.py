import os

def generate_m3u(directory):
    files_by_base = {}

    for filename in os.listdir(directory):
        if "(Disc" in filename or "(Disk" in filename:
            base_name = os.path.splitext(os.path.basename(filename))[0]
            base_name = base_name.split("(Disc")[0].strip()  # Remove "(Disc" and trim spaces
            base_name = base_name.split("(Disk")[0].strip()  # Remove "(Disk" and trim spaces

            if base_name not in files_by_base:
                files_by_base[base_name] = []
            files_by_base[base_name].append(filename)

    prefix = input("Enter prefix to add to the beginning of each line or press ENTER for no prefix: ")

    for base_name, file_list in files_by_base.items():
        m3u_name = f"{base_name}.m3u"
        with open(m3u_name, 'w') as m3u_file:
            lines = [prefix + filename for filename in file_list]
            lines = [line for line in lines if line.strip()]  # Remove empty lines
            m3u_file.write("\n".join(lines))
        print(f"M3U file '{m3u_name}' generated with {len(file_list)} files.")

# Get the directory of the script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Use the script directory as the base directory
generate_m3u(script_directory)
