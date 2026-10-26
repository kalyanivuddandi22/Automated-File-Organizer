import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from organizer import validate_directories, build_plan, execute_plan

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-dev-only-change-before-deployment")

@app.get("/")
def index():
    return render_template("index.html", source=session.get("source", ""), target=session.get("target", ""))

@app.post("/preview")
def preview():
    source, target = request.form.get("source", "").strip(), request.form.get("target", "").strip()
    session["source"], session["target"] = source, target
    try:
        src, dst = validate_directories(source, target)
        plan = build_plan(src, dst)
        return render_template("preview.html", plan=plan, source=src, target=dst)
    except (ValueError, OSError) as e:
        flash(str(e)); return redirect(url_for("index"))

@app.post("/organize")
def organize():
    if request.form.get("confirm") != "yes":
        flash("Please confirm before moving files."); return redirect(url_for("index"))
    try:
        src, dst = validate_directories(session.get("source", ""), session.get("target", ""), create_target=True)
        log = execute_plan(build_plan(src, dst))
        return render_template("result.html", log=log, source=src, target=dst)
    except (ValueError, OSError) as e:
        flash(str(e)); return redirect(url_for("index"))

if __name__ == "__main__":
    # Local-only. Do not expose the development server to the internet.
    app.run(host="127.0.0.1", port=5001, debug=False)
