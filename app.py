import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from scanner import scan_folder, format_size
from organizer import organize_folder, undo_organize

last_moved = []
last_folder = ""


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)


def run_scan():
    folder = folder_var.get().strip()
    if not folder:
        messagebox.showwarning("no folder", "please select a folder first.")
        return

    results, total_size = scan_folder(folder)

    if results is None:
        messagebox.showerror("error", total_size)
        return

    for widget in results_frame.winfo_children():
        widget.destroy()

    total_files = sum(len(files) for files in results.values())

    tk.Label(
        results_frame,
        text="found " + str(total_files) + " files  |  total size: " + format_size(total_size),
        font=("Helvetica", 12, "bold")
    ).grid(row=0, column=0, columnspan=4, pady=(10, 8))

    # header row
    for col, text in enumerate(["category", "files", "size", "proportion"]):
        tk.Label(
            results_frame,
            text=text,
            font=("Helvetica", 10, "bold"),
            width=14,
            anchor="center",
            relief="groove",
            padx=5,
            pady=4
        ).grid(row=1, column=col, padx=2, pady=2)

    row_num = 2
    for category, files in results.items():
        if not files:
            continue

        count = len(files)
        size = sum(f["size"] for f in files)

        tk.Label(
            results_frame,
            text=category,
            font=("Helvetica", 10),
            width=14,
            anchor="center",
            relief="ridge",
            pady=5
        ).grid(row=row_num, column=0, padx=2, pady=2)

        tk.Label(
            results_frame,
            text=str(count),
            font=("Helvetica", 10),
            width=14,
            anchor="center",
            relief="ridge",
            pady=5
        ).grid(row=row_num, column=1, padx=2, pady=2)

        tk.Label(
            results_frame,
            text=format_size(size),
            font=("Helvetica", 10),
            width=14,
            anchor="center",
            relief="ridge",
            pady=5
        ).grid(row=row_num, column=2, padx=2, pady=2)

        bar = ttk.Progressbar(results_frame, length=120, mode="determinate")
        bar["value"] = (count / total_files) * 100 if total_files > 0 else 0
        bar.grid(row=row_num, column=3, padx=10, pady=2)

        row_num += 1

    app.scan_results = results
    organize_btn.config(state="normal")
    undo_btn.config(state="disabled")
    status_var.set("scan complete. " + str(total_files) + " files found.")


def run_organize():
    global last_moved, last_folder

    folder = folder_var.get().strip()
    confirm = messagebox.askyesno(
        "confirm",
        "this will move files into subfolders inside:\n" + folder + "\n\ncontinue?"
    )
    if not confirm:
        return

    moved, errors = organize_folder(folder, app.scan_results)
    last_moved = moved
    last_folder = folder

    msg = str(len(moved)) + " files organized."
    if errors:
        msg += " " + str(len(errors)) + " errors."

    messagebox.showinfo("done", msg)
    status_var.set(msg)
    organize_btn.config(state="disabled")
    undo_btn.config(state="normal")
    run_scan()


def run_undo():
    global last_moved
    if not last_moved:
        messagebox.showinfo("nothing to undo", "no organize action to undo.")
        return

    confirm = messagebox.askyesno("undo", "move all files back to original folder?")
    if not confirm:
        return

    restored, errors = undo_organize(last_folder, last_moved)
    last_moved = []

    messagebox.showinfo("undo complete", str(len(restored)) + " files restored.")
    status_var.set(str(len(restored)) + " files restored.")
    undo_btn.config(state="disabled")
    run_scan()


# ---- main window ----
app = tk.Tk()
app.title("File Organizer")
app.geometry("640x550")
app.resizable(False, False)
app.scan_results = {}

# center all content
app.grid_columnconfigure(0, weight=1)

# title
tk.Label(
    app,
    text="File Organizer",
    font=("Helvetica", 20, "bold")
).grid(row=0, column=0, pady=(20, 4))

tk.Label(
    app,
    text="scan a folder, see what's inside, and organize it automatically",
    font=("Helvetica", 10),
    fg="#555555"
).grid(row=1, column=0, pady=(0, 15))

# folder picker row
folder_frame = tk.Frame(app)
folder_frame.grid(row=2, column=0, pady=5)

folder_var = tk.StringVar()

tk.Entry(
    folder_frame,
    textvariable=folder_var,
    font=("Helvetica", 11),
    width=42
).grid(row=0, column=0, padx=(0, 8))

tk.Button(
    folder_frame,
    text="browse",
    command=browse_folder,
    font=("Helvetica", 10),
    width=8
).grid(row=0, column=1)

# action buttons
btn_frame = tk.Frame(app)
btn_frame.grid(row=3, column=0, pady=12)

tk.Button(
    btn_frame,
    text="scan folder",
    command=run_scan,
    font=("Helvetica", 11),
    width=14
).grid(row=0, column=0, padx=6)

organize_btn = tk.Button(
    btn_frame,
    text="organize files",
    command=run_organize,
    font=("Helvetica", 11),
    width=14,
    state="disabled"
)
organize_btn.grid(row=0, column=1, padx=6)

undo_btn = tk.Button(
    btn_frame,
    text="undo",
    command=run_undo,
    font=("Helvetica", 11),
    width=14,
    state="disabled"
)
undo_btn.grid(row=0, column=2, padx=6)

# results table
results_frame = tk.Frame(app)
results_frame.grid(row=4, column=0, pady=5)
results_frame.grid_columnconfigure(0, weight=1)

# status bar
status_var = tk.StringVar()
status_var.set("select a folder to get started.")

tk.Label(
    app,
    textvariable=status_var,
    font=("Helvetica", 9),
    relief="sunken",
    anchor="w",
    padx=8
).grid(row=5, column=0, sticky="ew", pady=(10, 0))

app.mainloop()