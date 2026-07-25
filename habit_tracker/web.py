import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

from . import db


def create_app(test_config=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_mapping(SECRET_KEY="dev")
    # Ensure a writable instance folder and default database path
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config["DATABASE"] = os.environ.get(
        "DATABASE", str(Path(app.instance_path) / "habits.db")
    )

    if test_config:
        app.config.update(test_config)

    # Ensure database exists when app is created (compatible with Flask 3)
    db.init_db(app.config.get("DATABASE"))

    @app.route("/")
    def index():
        habits = db.list_habits(app.config.get("DATABASE"))
        return render_template("index.html", habits=habits)

    @app.route("/add", methods=["POST"])
    def add():
        name = request.form.get("name")
        description = request.form.get("description", "")
        if not name:
            flash("Name required")
            return redirect(url_for("index"))
        db.add_habit(name, description, app.config.get("DATABASE"))
        return redirect(url_for("index"))

    @app.route("/complete/<int:hid>", methods=["POST"])
    def complete(hid):
        # support JSON (fetch) or form submission with optional remark
        remark = None
        if request.is_json:
            payload = request.get_json()
            remark = payload.get("remark") if payload else None
        else:
            remark = request.form.get("remark")
        try:
            db.complete_habit(hid, app.config.get("DATABASE"), remark or "")
            flash("Marked complete")
        except ValueError:
            flash("Habit not found")
        return redirect(url_for("index"))

    @app.route("/delete/<int:hid>", methods=["POST"])
    def delete(hid):
        ok = db.delete_habit(hid, app.config.get("DATABASE"))
        flash("Deleted" if ok else "Not found")
        return redirect(url_for("index"))

    @app.route('/history')
    def history():
        completions = db.get_completions(db_path=app.config.get('DATABASE'))
        return render_template('history.html', completions=completions)

    @app.route('/motivation')
    def motivation():
        # a set of motivational speeches/lines delivered on the client via Web Speech API
        speeches = [
            "Today is another chance to make progress.",
            "Small steps every day lead to big changes.",
            "Consistency is your superpower.",
            "Celebrate the effort, not just the outcome."
        ]
        return render_template('motivation.html', speeches=speeches)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
