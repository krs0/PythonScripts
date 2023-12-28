import os
import json
import re


def remove_comments(json_str):
    # Use regular expression to remove // comments
    return re.sub(r'//[^\n]*', '', json_str)


def replace_content_with_sprites(path):
    # Split the path into components
    path_parts = path.split(os.path.sep)

    # Find the index of 'content' case-insensitively
    content_index = next((i for i, part in enumerate(path_parts) if part.lower() == 'content'), None)

    if content_index is not None:
        # Replace everything after 'content' with 'sprites'
        path_parts[content_index + 1:] = ['sprites']
        # Join the modified components back into a path
        modified_path = os.path.join(*path_parts)
        return modified_path
    else:
        # If 'content' is not found, return the original path
        return path


def get_animation_strings(data, json_file_path, folder_path):
    animation_strings = set()

    def explore(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "animation" and isinstance(value, str):
                    # Check if the animation file has .def extension, if not, add it
                    animation_file = value + (".def" if not value.endswith(".def") else "")
                    relative_path_to_mods = os.path.relpath(json_file_path, folder_path)
                    # Replace 'config' with 'sprites' in the path
                    full_animation_path = replace_content_with_sprites(relative_path_to_mods)
                    full_animation_path = os.path.join(
                        relative_path_to_mods,
                        animation_file
                    )
                    animation_strings.add(full_animation_path)
                else:
                    explore(value)
        elif isinstance(node, list):
            for item in node:
                explore(item)

    explore(data)
    return animation_strings


def parse_json_file(file_path, folder_path):
    try:
        with open(file_path, 'r') as file:
            json_content = file.read()
            json_content_without_comments = remove_comments(json_content)
            json_data = json.loads(json_content_without_comments)
            animation_strings = get_animation_strings(json_data, file_path, folder_path)
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
                animation_strings = parse_json_file(file_path, folder_path)
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
