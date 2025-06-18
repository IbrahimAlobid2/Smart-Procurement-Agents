import os

def clean_report(file_path: str, strip_lines: int = 1):
    """
    Clean the final output HTML file by removing a specific number of lines 
    from the top and bottom. Default: 1 line from top and bottom.

    Args:
        file_path (str): Path to the HTML file.
        strip_lines (int): Number of lines to remove from top and bottom.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) <= 2 * strip_lines:
        raise ValueError("File content too short to strip safely.")

    cleaned_lines = lines[strip_lines: -strip_lines]

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    print(f"[INFO] Cleaned {strip_lines} lines from top and bottom of {file_path}")
