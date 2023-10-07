import os
import json
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load the rules from the JSON file
with open("rules.json", "r") as f:
    rules = json.load(f)

# Define the directory where downloaded files are placed
download_dir = "$HOME/Downloads"

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        # Get the file extension
        file_name, file_ext = os.path.splitext(event.src_path)

        # Determine the target directory based on the file extension
        target_dir = rules.get(file_ext, "Other")

        # Create the target directory if it doesn't exist
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Move the file to the target directory
        shutil.move(event.src_path, os.path.join(target_dir, os.path.basename(event.src_path)))

if __name__ == "__main__":
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=download_dir, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

