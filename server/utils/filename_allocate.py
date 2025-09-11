def allocate_filename(filename, exist_files):
    if filename not in exist_files:
        return filename
    i = 1
    while f"{filename}_{i}" in exist_files:
        i += 1
    return f"{filename}_{i}"
