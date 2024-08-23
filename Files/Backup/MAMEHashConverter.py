import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

def indent(elem, level=0):
    i = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level + 1)
        if not subelem.tail or not subelem.tail.strip():
            subelem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return elem

def convert_xml(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".xml"):
            tree = ET.parse(os.path.join(input_folder, filename))
            root = tree.getroot()

            gamelist = ET.Element("gameList")

            for software in root.findall("software"):
                game = ET.SubElement(gamelist, "game")

                software_name = software.get("name")
                path = f"./{software_name}.cmd"
                ET.SubElement(game, "path").text = path

                description = software.find("description")
                if description is not None:
                    # Replace &amp; with & in the name tag
                    name_text = description.text.replace("&amp;", "&")
                    ET.SubElement(game, "name").text = name_text

            gamelist = indent(gamelist)
            output_tree = ET.ElementTree(gamelist)
            output_filename = os.path.join(output_folder, filename)
            output_tree.write(output_filename, encoding="utf-8", xml_declaration=True)

    messagebox.showinfo("Success", "XML files have been converted and saved!")

def generate_cmd_files(input_folder):
    target_files = {
        "apple2_flop_orig.xml": "apple2",
        "apple2gs_flop_orig.xml": "apple2gs",
        "vc4000.xml": "vc4000"
    }

    chosen_files = [file for file in os.listdir(input_folder) if file in target_files]
    
    for file in chosen_files:
        system = target_files[file]
        cmd_output_folder = os.path.join(input_folder, file.replace(".xml", ""))
        if not os.path.exists(cmd_output_folder):
            os.makedirs(cmd_output_folder)

        tree = ET.parse(os.path.join(input_folder, file))
        root = tree.getroot()

        if file == "apple2_flop_orig.xml":
            system = simpledialog.askstring(f"{file} - System Choice", "Choose a system: apple2, apple2p, apple2e, apple2ee, apple2c, apple2cp, apple2gs")
            option = simpledialog.askstring(f"{file} - Option Choice", "Choose an option: -gameio joy, -gameio compeyes, -gameio paddles")
        elif file == "apple2gs_flop_orig.xml":
            option = simpledialog.askstring(f"{file} - Option Choice", "Choose an option: -gameio joy, -gameio compeyes, -gameio paddles")
        else:
            option = None

        for software in root.findall("software"):
            software_name = software.get("name")
            cmd_filename = f"{software_name}.cmd"
            cmd_content = f"{system} {software_name} {option if option else ''}".strip()

            with open(os.path.join(cmd_output_folder, cmd_filename), 'w') as cmd_file:
                cmd_file.write(cmd_content)

    messagebox.showinfo("Success", "CMD files have been generated!")

def browse_input_folder():
    folder_selected = filedialog.askdirectory()
    input_entry.delete(0, tk.END)
    input_entry.insert(0, folder_selected)

def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_selected)

def run_conversion():
    input_folder = input_entry.get()
    output_folder = output_entry.get()
    
    if not input_folder or not output_folder:
        messagebox.showwarning("Warning", "Please select both input and output folders!")
        return
    
    convert_xml(input_folder, output_folder)

def run_cmd_generation():
    input_folder = input_entry.get()
    
    if not input_folder:
        messagebox.showwarning("Warning", "Please select the input folder!")
        return
    
    generate_cmd_files(input_folder)

# GUI setup
root = tk.Tk()
root.title("MAME hash gamelist & cmd converter")

tk.Label(root, text="MAME Hash xml files input folder:").grid(row=0, column=0, padx=10, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_input_folder).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Daijishou gamelist.xml output folder:").grid(row=1, column=0, padx=10, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_output_folder).grid(row=1, column=2, padx=10, pady=5)

tk.Button(root, text="Generate playlist", command=run_conversion).grid(row=2, column=1, pady=10)
tk.Button(root, text="Generate CMD files", command=run_cmd_generation).grid(row=3, column=1, pady=10)

root.mainloop()
