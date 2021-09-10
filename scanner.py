import os

CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".m4v"],
    "audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"],
    "code": [".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".go", ".rb", ".php"],
    "archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "others": []
}


def get_category(extension):
    for category, extensions in CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return "others"


def scan_folder(folder_path):
    results = {category: [] for category in CATEGORIES}
    total_size = 0

    if not os.path.exists(folder_path):
        return None, "folder does not exist"

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # skip subfolders, only scan files
        if not os.path.isfile(filepath):
            continue

        extension = os.path.splitext(filename)[1]
        category = get_category(extension)
        size = os.path.getsize(filepath)
        total_size += size

        results[category].append({
            "name": filename,
            "path": filepath,
            "extension": extension.lower(),
            "size": size
        })

    return results, total_size


def format_size(size_bytes):
    if size_bytes < 1024:
        return str(size_bytes) + " B"
    elif size_bytes < 1024 * 1024:
        return str(round(size_bytes / 1024, 1)) + " KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return str(round(size_bytes / (1024 * 1024), 1)) + " MB"
    else:
        return str(round(size_bytes / (1024 * 1024 * 1024), 2)) + " GB"