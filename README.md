# File Organizer

A desktop GUI application that scans any folder and automatically organizes 
files into categorized subfolders.

Built this because my Downloads folder was a complete mess and I wanted to 
learn how to build desktop apps with Python.

## What it does

- Browse and select any folder on your computer
- Scans all files and categorizes them by type
- Shows a table with file counts, sizes, and proportions per category
- Organizes files into subfolders with one click
- Undo button to restore everything back to original location

## Categories

images, videos, audio, documents, code, archives, fonts, others

## Requirements

- Python 3.x
- tkinter (built into Python)

## Setup
```bash
git clone https://github.com/yourusername/file-organizer
cd file-organizer
python3 app.py
```

## What I learned

- Building desktop GUI applications with Tkinter
- Event-driven programming - buttons triggering callback functions
- The Tkinter grid layout system
- File system operations with os and shutil modules
- Handling duplicate filenames during file moves
- Implementing an undo system by tracking file move history