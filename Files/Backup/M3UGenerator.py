import os

def create_m3u_playlists(folder_path):
    files = [file for file in os.listdir(folder_path) if (file.endswith('.chd') or file.endswith('.cue')) and '(Disc' in file]

    path_prefix = input("Enter the path prefix (press Enter for no prefix): ").strip()

    name_groups = {}
    for file in files:
        base_name, region_info = get_base_name_and_region(file)
        key = (base_name, region_info)
        if key not in name_groups:
            name_groups[key] = []
        name_groups[key].append(os.path.join(folder_path, file))

    for (base_name, region_info), file_paths in name_groups.items():
        create_m3u_playlist(file_paths, base_name, region_info, path_prefix)

def get_base_name_and_region(file_name):
    # Extract the base name and region information
    # Modify this function based on your file naming convention
    parts = file_name.split(' ')
    base_name_parts = []
    region_info_parts = []

    for part in parts:
        if part.startswith('(Disc') or part.startswith('(Rev'):
            break
        if part.startswith('('):
            region_info_parts.append(part)
        else:
            base_name_parts.append(part)

    base_name = ' '.join(base_name_parts)
    region_info = ' '.join(region_info_parts)
    
    return base_name, region_info

def create_m3u_playlist(file_paths, base_name, region_info, path_prefix):
    m3u_name = f'{base_name} {region_info}'.strip() if region_info else base_name
    lines = [path_prefix + os.path.basename(path) for path in file_paths]

    with open(m3u_name + '.m3u', 'w') as playlist_file:
        playlist_file.write('\n'.join(lines))

# Get the current script's directory
script_directory = os.path.dirname(os.path.realpath(__file__))

# Example usage:
create_m3u_playlists(script_directory)
