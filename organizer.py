import shutil
from pathlib import Path

RULES = {
 "Images": {".png",".jpg",".jpeg",".gif",".bmp",".svg",".webp",".tif",".tiff",".ico"},
 "Documents": {".pdf",".doc",".docx",".txt",".rtf",".odt",".xls",".xlsx",".ppt",".pptx",".csv",".md"},
 "Archives": {".zip",".rar",".7z",".tar",".gz",".bz2",".xz"},
 "Media": {".mp3",".wav",".aac",".flac",".ogg",".mp4",".mkv",".mov",".avi",".webm"},
 "Python": {".py",".pyw",".pyc",".ipynb"},
 "Code": {".js",".ts",".jsx",".tsx",".html",".htm",".css",".scss",".java",".c",".h",".cpp",".cs",".php",".rb",".go",".rs",".json",".xml",".yml",".yaml",".sql",".sh",".bat",".ps1"},
}
def category_for(path):
    for name, exts in RULES.items():
        if path.suffix.lower() in exts: return name
    return "Others"

def validate_directories(source, target, create_target=False):
    if not source or not target: raise ValueError("Enter both source and target folder paths.")
    src, dst = Path(source).expanduser().resolve(), Path(target).expanduser().resolve()
    if not src.is_dir(): raise ValueError(f"Source folder does not exist: {src}")
    if src == dst: raise ValueError("Source and target folders must be different.")
    try:
        dst.relative_to(src)
        raise ValueError("For safety, choose a target folder outside the source folder.")
    except ValueError as e:
        if "For safety" in str(e): raise
    if dst.exists() and not dst.is_dir(): raise ValueError("Target path exists but is not a directory.")
    if create_target: dst.mkdir(parents=True, exist_ok=True)
    return src, dst

def unique_path(path):
    if not path.exists(): return path
    n = 1
    while True:
        candidate = path.with_name(f"{path.stem} ({n}){path.suffix}")
        if not candidate.exists(): return candidate
        n += 1

def build_plan(source, target):
    plan = []
    for item in sorted(source.iterdir(), key=lambda p:p.name.lower()):
        if item.is_symlink() or not item.is_file(): continue
        cat = category_for(item)
        dest = unique_path(target / cat / item.name)
        plan.append({"source":item, "destination":dest, "category":cat,
                     "status":"Ready" if dest.name == item.name else "Rename to avoid duplicate"})
    return plan

def execute_plan(plan):
    log = []
    for item in plan:
        src, dest = item["source"], item["destination"]
        try:
            if not src.exists() or not src.is_file():
                log.append({**item, "result":"Skipped", "message":"Source file no longer exists."}); continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest = unique_path(dest)
            shutil.move(str(src), str(dest))
            log.append({**item, "destination":dest, "result":"Moved", "message":"Moved successfully."})
        except (OSError, shutil.Error) as e:
            log.append({**item, "result":"Error", "message":str(e)})
    return log
