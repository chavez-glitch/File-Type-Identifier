import sys
import tkinter as tk
from tkinter import filedialog

MAGIC_NUMBERS = {
    b"\x25\x50\x44\x46": "PDF",
    b"\x89\x50\x4E\x47": "PNG Image",
    b"\xFF\xD8\xFF": "JPEG Image",
    b"\x50\x4B\x03\x04": "ZIP Archive",
    b"\x4D\x5A": "Windows Executable (EXE)",
}


def identify_file(filename):
    try:
        with open(filename, "rb") as file:
            file_header = file.read(8)
    except FileNotFoundError:
        return f"File not found: {filename}"
    except PermissionError:
        return f"Permission denied: {filename}"
    except OSError as error:
        return f"Could not read file '{filename}': {error}"

    for magic, filetype in MAGIC_NUMBERS.items():
        if file_header.startswith(magic):
            return filetype

    return "Unknown file type"


def select_file():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected_file = filedialog.askopenfilename(title="Select a file to identify")
    root.destroy()
    return selected_file


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else select_file()

    if not filename:
        print("No file selected.")
    else:
        print(identify_file(filename))
