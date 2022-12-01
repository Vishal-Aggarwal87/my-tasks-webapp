from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.id} - {self.title}"


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
def my_tasks():
    all_tasks = ""
    all_tasks = (
        Tasks.query.all()
    )  # for displaying all tasks in the format which we return in __repr__ function
    return render_template("index.html", all_tasks=all_tasks)


@app.route("/add", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":

        title = request.form["title"]
        desc = request.form["description"]
        task = Tasks(title=title, desc=desc)
        db.session.add(task)
        db.session.commit()  # for saving all data in db
    return redirect("/")


@app.route("/delete/<int:id>/", methods=["GET", "POST"])
def delete_task(id):
    task = db.get_or_404(Tasks, id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")


@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update_task(id):
    task = db.get_or_404(Tasks, id)
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        task.title = title
        task.desc = desc
        db.session.add(task)
        db.session.commit()
        return redirect("/")

    return render_template("update.html", task=task)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
