import os
import json
import re
from tkinter import Tk, Button, filedialog, Label, messagebox

def sanitize_filename(name):
    # Replace colon with ' - '
    name = name.replace(':', ' - ')
    # Remove any other illegal characters
    return re.sub(r'[<>:"/\\|?*]', '', name)

def parse_ini_file(ini_file_path):
    app_data = {}
    moonlight_uuid = None

    with open(ini_file_path, 'r') as ini_file:
        lines = ini_file.readlines()

    for line in lines:
        if line.startswith("1\\apps\\"):
            parts = line.strip().split('=')
            key = parts[0]
            value = parts[1] if len(parts) > 1 else ""
            keys = key.split('\\')
            
            if len(keys) >= 4 and keys[2].isdigit():
                app_num = keys[2]
                app_key = keys[3]

                if app_key == 'name':
                    current_app = value
                    app_data[current_app] = {'id': None}
                elif app_key == 'id' and current_app:
                    app_data[current_app]['id'] = value
        elif line.startswith("1\\uuid="):
            moonlight_uuid = line.strip().split('=')[1]

    return app_data, moonlight_uuid

def create_daijishou_files(ini_file_path):
    app_data, moonlight_uuid = parse_ini_file(ini_file_path)
    save_folder = os.path.join(os.path.dirname(ini_file_path), "moonlight")
    os.makedirs(save_folder, exist_ok=True)

    for app_name, data in app_data.items():
        if 'id' in data and data['id']:
            sanitized_name = sanitize_filename(app_name)
            moonlight_filename = os.path.join(save_folder, f"{sanitized_name}.moonlight")
            content = f"# Daijishou Player Template\n[moonlight_id] {data['id']}\n..."
            
            with open(moonlight_filename, 'w') as moonlight_file:
                moonlight_file.write(content)

            print(f"Created {moonlight_filename}")

    if moonlight_uuid:
        moonlight_json_content = {
            "databaseVersion": 14,
            "revisionNumber": 2,
            "platform": {
                "name": "Moonlight Streaming",
                "uniqueId": "moonlight",
                "shortname": "moonlight",
                "description": None,
                "acceptedFilenameRegex": "^(?!(?:\\._|\\.).*).*$",
                "scraperSourceList": [],
                "boxArtAspectRatioId": 0,
                "useCustomBoxArtAspectRatio": False,
                "customBoxArtAspectRatio": None,
                "screenAspectRatioId": 1,
                "useCustomScreenAspectRatio": False,
                "customScreenAspectRatio": None,
                "retroAchievementsAlias": None,
                "extra": ""
            },
            "playerList": [
                {
                    "name": "moonlight",
                    "uniqueId": "moonlight.com.limelight",
                    "description": "Supported extensions: moonlight",
                    "acceptedFilenameRegex": "^(.*)\\.(?:moonlight)$",
                    "amStartArguments": f"-n com.limelight/com.limelight.ShortcutTrampoline\n --es UUID {moonlight_uuid}\n --es AppId {{tags.moonlight_id}}",
                    "killPackageProcesses": True,
                    "killPackageProcessesWarning": True,
                    "extra": ""
                }
            ]
        }

        moonlight_json_filename = os.path.join(save_folder, "Moonlight.json")
        with open(moonlight_json_filename, 'w') as json_file:
            json.dump(moonlight_json_content, json_file, indent=2)

        print(f"Created {moonlight_json_filename}")

    messagebox.showinfo("Daijishou Files", "Daijishou moonlight files created successfully.")

def create_esde_files(ini_file_path):
    app_data, moonlight_uuid = parse_ini_file(ini_file_path)
    save_folder = os.path.join(os.path.dirname(ini_file_path), "moonlight")
    os.makedirs(save_folder, exist_ok=True)

    for app_name, data in app_data.items():
        if 'id' in data and data['id']:
            sanitized_name = sanitize_filename(app_name)
            moonlight_filename = os.path.join(save_folder, f"{sanitized_name}.moonlight")
            content = f"{data['id']}"
            
            with open(moonlight_filename, 'w') as moonlight_file:
                moonlight_file.write(content)

            print(f"Created {moonlight_filename}")

    if moonlight_uuid:
        uuid_filename = os.path.join(save_folder, "Moonlight.uuid")
        with open(uuid_filename, 'w') as uuid_file:
            uuid_file.write(moonlight_uuid)

        print(f"Created {uuid_filename}")

        es_systems_content = """<systemList>
    <system>
        <name>moonlight</name>
        <fullname>Moonlight Game Streaming</fullname>
        <path>%ROMPATH%/moonlight</path>
        <extension>.moonlight</extension>
        <command label="Moonlight">%EMULATOR_Moonlight% %EXTRA_UUID%=%INJECT%=Moonlight.uuid %EXTRA_AppId%=%INJECT%=%BASENAME%.moonlight</command>
        <platform>moonlight</platform>
        <theme>moonlight</theme>
    </system>
</systemList>"""

        es_find_rules_content = """<ruleList>
    <emulator name="Moonlight">
        <rule type="androidpackage">
            <entry>com.limelight/com.limelight.ShortcutTrampoline</entry>
        </rule>
    </emulator>
</ruleList>"""

        es_systems_filename = os.path.join(save_folder, "es_systems.xml")
        with open(es_systems_filename, 'w') as es_systems_file:
            es_systems_file.write(es_systems_content)

        print(f"Created {es_systems_filename}")

        es_find_rules_filename = os.path.join(save_folder, "es_find_rules.xml")
        with open(es_find_rules_filename, 'w') as es_find_rules_file:
            es_find_rules_file.write(es_find_rules_content)

        print(f"Created {es_find_rules_filename}")

    messagebox.showinfo("ESDE Files", "ES-DE moonlight files created successfully.")

def select_ini_file(action):
    ini_file_path = filedialog.askopenfilename(title="Select Moonlight.ini file", filetypes=[("INI files", "*.ini")])
    if ini_file_path:
        if action == "daijishou":
            create_daijishou_files(ini_file_path)
        elif action == "esde":
            create_esde_files(ini_file_path)

def main():
    root = Tk()
    root.title("Moonlight Files Creator")

    label = Label(root, text="Select an action:")
    label.pack(pady=10)

    daijishou_button = Button(root, text="Create Daijishou Moonlight files", command=lambda: select_ini_file("daijishou"))
    daijishou_button.pack(pady=5)

    esde_button = Button(root, text="Create ES-DE Moonlight files", command=lambda: select_ini_file("esde"))
    esde_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
