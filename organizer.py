import os
import shutil
from pathlib import Path

def organize_directory(target_directory):
    """
    Scans the target directory, groups files by extension, 
    creates subfolders dynamically, and moves files safely.
    """
    target_path = Path(target_directory)

    if not target_path.exists() or not target_path.is_dir():
        print(f"Error: The directory '{target_directory}' does not exist or is not a valid directory.")
        return

    # Define extension mapping dictionary
    EXTENSION_MAPPING = {
        # Documents
        '.pdf': 'Documents', '.docx': 'Documents', '.doc': 'Documents',
        '.txt': 'Documents', '.xlsx': 'Documents', '.pptx': 'Documents',
        # Images
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
        '.gif': 'Images', '.svg': 'Images', '.webp': 'Images',
        # Videos
        '.mp4': 'Videos', '.mkv': 'Videos', '.avi': 'Videos', '.mov': 'Videos',
        # Archives
        '.zip': 'Archives', '.rar': 'Archives', '.tar': 'Archives', '.gz': 'Archives',
        # Code & Scripts
        '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code', '.cpp': 'Code', '.java': 'Code'
    }

    print(f"\n=== Starting File Organization for: {target_path.resolve()} ===")
    
    files_moved = 0
    folders_created = set()
    skipped_files = 0

    try:
        # Use os.scandir() to scan the directory efficiently
        with os.scandir(target_path) as entries:
            for entry in entries:
                # Skip directories and hidden files (starting with '.')
                if entry.is_dir() or entry.name.startswith('.'):
                    continue

                file_path = Path(entry.path)
                file_ext = file_path.suffix.lower()

                # Determine category folder; default to 'Others' if extension is unknown
                category = EXTENSION_MAPPING.get(file_ext, 'Others')
                dest_folder = target_path / category

                # Create category subfolder if it doesn't exist
                if not dest_folder.exists():
                    dest_folder.mkdir(parents=True, exist_ok=True)
                    folders_created.add(category)

                dest_path = dest_folder / file_path.name

                # Handle naming collisions (if file already exists in destination)
                if dest_path.exists():
                    base_name = file_path.stem
                    counter = 1
                    while True:
                        new_filename = f"{base_name}_{counter}{file_ext}"
                        dest_path = dest_folder / new_filename
                        if not dest_path.exists():
                            break
                        counter += 1

                # Safely move the file while handling permission exceptions
                try:
                    shutil.move(str(file_path), str(dest_path))
                    print(f"Moved: {file_path.name} -> {category}/")
                    files_moved += 1
                except PermissionError:
                    print(f"Permission Denied: Could not move '{file_path.name}'. Skipping.")
                    skipped_files += 1
                except Exception as e:
                    print(f"Error moving '{file_path.name}': {e}")
                    skipped_files += 1

    except PermissionError:
        print(f"Permission Denied: Cannot access directory '{target_directory}'.")
        return

    # Print Formatted Execution Summary
    print("\n" + "="*50)
    print(f"{'ORGANIZATION EXECUTION SUMMARY':^50}")
    print("="*50)
    print(f"Target Directory : {target_path.name}")
    print(f"Categories Used  : {', '.join(folders_created) if folders_created else 'None'}")
    print(f"Total Files Moved: {files_moved}")
    print(f"Files Skipped    : {skipped_files}")
    print("="*50)

if __name__ == "__main__":
    # Example usage: Pass your target directory path here (e.g., a test folder path)
    user_dir = input("Enter the path of the directory to organize (leave blank for current directory): ").strip()
    if not user_dir:
        user_dir = "."
    
    organize_directory(user_dir)
