import os
import re
import msvcrt  # For Windows-specific keyboard input detection

def prompt_user():
    print("Press Enter to start the renaming process or press Escape to skip.")
    while True:
        key = msvcrt.getch()
        if key == b'\r':  # Enter key
            return True
        elif key == b'\x1b':  # Escape key
            return False

def rename_files_to_sfc_recursive(directory="."):
    if not prompt_user():
        print("Exiting without renaming.")
        return

    renamed_files = []

    for root, dirs, files in os.walk(directory):
        # Find the sfc files in the current subfolder
        sfc_files = [file for file in files if file.lower().endswith('.sfc')]

        if len(sfc_files) == 1:
            sfc_file = sfc_files[0]
            base_name_sfc, _ = os.path.splitext(sfc_file)

            # Rename pcm files with numbers at the end using the sfc file's base name
            for file in files:
                if file.lower().endswith('.pcm') and re.match(r'.+-(\d+)\.pcm$', file):
                    match_pcm = re.match(r'^(.+)-(\d+)\.pcm$', file)
                    if match_pcm:
                        base_name_pcm, number_pcm = match_pcm.groups()
                        new_name = f"{base_name_sfc}-{number_pcm}.pcm"
                        os.rename(os.path.join(root, file), os.path.join(root, new_name))
                        print(f"Renamed {file} to {new_name}")
                        renamed_files.append(new_name)
                elif file.lower().endswith(('.bps', '.msu', '.ips')):
                    extension = os.path.splitext(file)[1]
                    new_name = f"{base_name_sfc}{extension}"
                    os.rename(os.path.join(root, file), os.path.join(root, new_name))
                    print(f"Renamed {file} to {new_name}")
                    renamed_files.append(new_name)

    print("\nRenamed Files:")
    for file in renamed_files:
        print(file)

    print("\nPress Enter to exit.")
    while True:
        key = msvcrt.getch()
        if key == b'\r':  # Enter key
            break

if __name__ == "__main__":
    # Get the directory of the script
    script_directory = os.path.dirname(__file__)
    rename_files_to_sfc_recursive(script_directory)
