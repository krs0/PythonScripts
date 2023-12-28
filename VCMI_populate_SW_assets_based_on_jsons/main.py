import os
import json
import re


def remove_comments(json_str):
    # Use regular expression to remove // comments
    return re.sub(r'//[^\n]*', '', json_str)


def get_animation_strings(data, file_name):
    animation_strings = set()

    def explore(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "animation" and isinstance(value, str):
                    # Check if the animation file has .def extension, if not, add it
                    animation_file = value + (".def" if not value.endswith(".def") else "")
                    animation_strings.add(animation_file)
                else:
                    explore(value)
        elif isinstance(node, list):
            for item in node:
                explore(item)

    explore(data)
    return animation_strings


def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            json_content = file.read()
            json_content_without_comments = remove_comments(json_content)
            json_data = json.loads(json_content_without_comments)
            animation_strings = get_animation_strings(json_data, os.path.basename(file_path))
            return animation_strings

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return set()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{file_path}': {e}")
        return set()


def parse_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        return set()

    all_animation_strings = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                animation_strings = parse_json_file(file_path)
                all_animation_strings.update(animation_strings)

    return all_animation_strings


def main():
    # Replace 'your_folder_path' with the path to the folder containing JSON files
    folder_path = r"d:\git\succession_wars\Mods"

    all_animation_strings = parse_folder(folder_path)

    print("Animation Strings:")
    for string in all_animation_strings:
        print(string)


if __name__ == "__main__":
    main()
