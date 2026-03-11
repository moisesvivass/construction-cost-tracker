from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Project, Expense   # 👈 agregamos Expense
from datetime import datetime

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return redirect(url_for("main.projects"))


@main.route("/projects")
def projects():
    all_projects = Project.query.all()
    return render_template("projects.html", projects=all_projects)


@main.route("/projects/new", methods=["GET", "POST"])
def new_project():
    if request.method == "POST":
        name = request.form["name"]
        client = request.form["client"]
        budget = float(request.form["budget"])
        start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()

        project = Project(name=name, client=client, budget=budget, start_date=start_date)
        db.session.add(project)
        db.session.commit()

        flash("Project created successfully!", "success")
        return redirect(url_for("main.projects"))

    return render_template("new_project.html")


# ── NEW: Project detail ──────────────────────────────────────────────────────
@main.route("/project/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("project_detail.html", project=project)


# ── NEW: Add expense ─────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>/add-expense", methods=["POST"])
def add_expense(project_id):
    project = Project.query.get_or_404(project_id)

    description = request.form["description"]
    category    = request.form["category"]
    amount      = float(request.form["amount"])
    date        = datetime.strptime(request.form["date"], "%Y-%m-%d").date()

    expense = Expense(
        description = description,
        category    = category,
        amount      = amount,
        date        = date,
        project_id  = project.id
    )
    db.session.add(expense)
    db.session.commit()

    flash("Expense added successfully!", "success")
    return redirect(url_for("main.project_detail", project_id=project.id))