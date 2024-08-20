import os

def list_directory_structure(folder_dir, prefix='', file=None):
    # Get the list of files and directories
    items = os.listdir(folder_dir)
    items.sort()  # Sort to ensure consistent output order

    for i, item in enumerate(items):
        if item == '.DS_Store':
            continue  # Skip .DS_Store files

        path = os.path.join(folder_dir, item)
        if os.path.isdir(path):
            # Write the directory name
            file.write(f"{prefix}├── {item}/\n")
            # Recursive call for the directory contents
            list_directory_structure(path, prefix + "│   ", file)
        else:
            # Write the file name
            if i == len(items) - 1:
                file.write(f"{prefix}└── {item}\n")
            else:
                file.write(f"{prefix}├── {item}\n")

# Usage example:
folder_dir = 'output_files/IGCSE/Physics 2023'
output_file = 'physics_gcse.txt'

with open(output_file, 'w') as file:
    file.write(f"{folder_dir}/\n")
    list_directory_structure(folder_dir, file=file)

print(f"Directory structure has been written to {output_file}.")
