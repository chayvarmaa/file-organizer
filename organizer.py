import os
import shutil


def organize_folder(folder_path, scan_results):
    moved = []
    errors = []

    for category, files in scan_results.items():
        if not files:
            continue

        # create subfolder for this category
        subfolder = os.path.join(folder_path, category)
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        for file in files:
            src = file["path"]
            dst = os.path.join(subfolder, file["name"])

            # handle duplicate filenames
            if os.path.exists(dst):
                name, ext = os.path.splitext(file["name"])
                counter = 1
                while os.path.exists(dst):
                    dst = os.path.join(subfolder, name + "_" + str(counter) + ext)
                    counter += 1

            try:
                shutil.move(src, dst)
                moved.append({
                    "file": file["name"],
                    "category": category,
                    "destination": dst
                })
            except Exception as e:
                errors.append({
                    "file": file["name"],
                    "error": str(e)
                })

    return moved, errors


def undo_organize(folder_path, moved):
    restored = []
    errors = []

    for item in moved:
        src = item["destination"]
        dst = os.path.join(folder_path, item["file"])

        try:
            shutil.move(src, dst)
            restored.append(item["file"])
        except Exception as e:
            errors.append({
                "file": item["file"],
                "error": str(e)
            })

    return restored, errors