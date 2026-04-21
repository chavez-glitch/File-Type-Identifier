import sys
import tkinter as tk
from tkinter import filedialog

# Each entry is (byte_offset, signature_bytes, detected_type).
MAGIC_SIGNATURES = [
    (0, b"\x25\x50\x44\x46", "PDF"),
    (0, b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", "PNG Image"),
    (0, b"\xFF\xD8\xFF", "JPEG Image"),
    (0, b"GIF87a", "GIF Image"),
    (0, b"GIF89a", "GIF Image"),
    (0, b"BM", "BMP Image"),
    (0, b"II*\x00", "TIFF Image (Little Endian)"),
    (0, b"MM\x00*", "TIFF Image (Big Endian)"),
    (0, b"RIFF", "RIFF Container"),
    (8, b"WEBP", "WEBP Image"),
    (8, b"WAVE", "WAV Audio"),
    (8, b"AVI ", "AVI Video"),
    (4, b"ftyp", "MP4/MOV Video"),
    (0, b"ID3", "MP3 Audio"),
    (0, b"\xFF\xFB", "MP3 Audio"),
    (0, b"fLaC", "FLAC Audio"),
    (0, b"OggS", "OGG Container"),
    (0, b"\x50\x4B\x03\x04", "ZIP Archive"),
    (0, b"\x50\x4B\x05\x06", "ZIP Archive (Empty)"),
    (0, b"\x50\x4B\x07\x08", "ZIP Archive (Spanned)"),
    (0, b"\x1F\x8B\x08", "GZIP Archive"),
    (0, b"Rar!\x1A\x07\x00", "RAR Archive (v1.5+)"),
    (0, b"Rar!\x1A\x07\x01\x00", "RAR Archive (v5+)"),
    (0, b"7z\xBC\xAF\x27\x1C", "7-Zip Archive"),
    (0, b"\x4D\x5A", "Windows Executable (EXE/DLL)"),
]


def is_probably_text(data):
    # Empty files are treated as text.
    if not data:
        return True

    # Null bytes are a strong indicator of binary data.
    if b"\x00" in data:
        return False

    # Allow printable ASCII plus tabs/newlines/carriage returns.
    text_bytes = sum(
        1 for byte in data if byte in (9, 10, 13) or 32 <= byte <= 126
    )
    return (text_bytes / len(data)) > 0.95


def identify_file(filename):
    print(f"[INFO] Opening file: {filename}")
    try:
        with open(filename, "rb") as file:
            # Header is used for fixed-signature checks at known offsets.
            file_header = file.read(64)
            # Larger sample improves text-vs-binary fallback detection.
            file_sample = file_header + file.read(960)
    except FileNotFoundError:
        return f"File not found: {filename}"
    except PermissionError:
        return f"Permission denied: {filename}"
    except OSError as error:
        return f"Could not read file '{filename}': {error}"

    print("[INFO] Checking known file signatures...")
    for offset, signature, filetype in MAGIC_SIGNATURES:
        if file_header[offset : offset + len(signature)] == signature:
            print(f"[INFO] Matched signature at offset {offset}: {filetype}")
            return filetype

    # If no known binary signature matches, try a text heuristic.
    print("[INFO] No signature match found. Running text-file heuristic...")
    if is_probably_text(file_sample):
        print("[INFO] Content looks like plain text.")
        return "Text File (TXT)"

    print("[INFO] File type could not be identified.")
    return "Unknown file type"

#
def select_file():
    # Open a native file picker when no CLI path is provided.
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected_file = filedialog.askopenfilename(title="Select a file to identify")
    root.destroy()
    return selected_file


if __name__ == "__main__":
    print("[INFO] Starting file type identifier...")
    filename = sys.argv[1] if len(sys.argv) > 1 else select_file()

    if not filename:
        print("No file selected.")
    else:
        print(f"[INFO] File selected: {filename}")
        file_type = identify_file(filename)
        print(f"The file type is {file_type}")
