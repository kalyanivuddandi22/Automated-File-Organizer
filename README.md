# Automated File Organizer — Web App

A local Flask web app for CodeNova **Task 3: Automated File Organizer**.

## Requirements covered
- Interactive source and target directory path entry.
- File categories: Images, Documents, Archives, Media, Python, Code, and Others.
- Duplicate filenames preserved with incremental suffixes such as `notes (1).txt`.
- Preview/dry-run shows planned moves without moving files or creating category folders.
- Separate confirmation required before actual moves.
- Execution log reports moved, skipped, and failed files.
- Top-level files only; subdirectories and symbolic links are skipped. Permission/locked-file errors are logged.

## Run on Windows
1. Extract the ZIP and open the folder in VS Code.
2. Open Terminal → New Terminal.
3. Check Python with `python --version` (or `py --version`).
4. Install Flask: `python -m pip install -r requirements.txt` (or `py -m pip install -r requirements.txt`).
5. Run `python app.py` (or `py app.py`).
6. Visit **http://127.0.0.1:5001** in your browser. Keep the terminal open.

## Safe test
Create separate test folders and use copies, not important files:
```powershell
New-Item -ItemType Directory -Force C:\FileOrganizerDemo\Incoming
New-Item -ItemType Directory -Force C:\FileOrganizerDemo\Organized
Set-Content C:\FileOrganizerDemo\Incoming\notes.txt "sample document"
Set-Content C:\FileOrganizerDemo\Incoming\script.py "print('hello')"
Set-Content C:\FileOrganizerDemo\Incoming\unknown.xyz "sample other file"
```
Enter those full paths in the website and click **Preview only** first. Review the plan. To move files, preview again, tick the confirmation box, and choose **Organize files**.

## Safety
- Preview mode does not change files.
- Target must be outside source; the app enforces this.
- Existing files are not overwritten; numbered suffixes are used.
- Only regular files directly inside source are processed. Subfolders are untouched.
- App binds to `127.0.0.1` and is for local use, not a public internet deployment. Back up important files before organizing.

## Structure
`app.py` (Flask routes), `organizer.py` (organizing logic), `templates/`, `static/style.css`, `requirements.txt`, `.gitignore`.

## Submission
Add screenshots of the home page, preview, and execution log. Push code and README to a public GitHub repository as required. This is a local web app, not a hosted public demo.
