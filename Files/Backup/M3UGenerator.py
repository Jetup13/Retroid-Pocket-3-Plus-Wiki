import os

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

    prefix = input("Enter prefix to add to the beginning of each line (press enter for no prefix): ")

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