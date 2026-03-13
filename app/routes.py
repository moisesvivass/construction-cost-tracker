from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Project, Expense
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
        name   = request.form["name"].strip()
        client = request.form["client"].strip()

        if not name or not client:
            flash("Name and client are required.", "danger")
            return redirect(url_for("main.new_project"))

        if len(name) > 100 or len(client) > 100:
            flash("Name and client must be under 100 characters.", "danger")
            return redirect(url_for("main.new_project"))

        try:
            budget = float(request.form["budget"])
            if budget <= 0:
                raise ValueError
        except ValueError:
            flash("Budget must be a positive number.", "danger")
            return redirect(url_for("main.new_project"))

        try:
            start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("main.new_project"))

        project = Project(name=name, client=client, budget=budget, start_date=start_date)
        db.session.add(project)
        db.session.commit()

        flash("Project created successfully!", "success")
        return redirect(url_for("main.projects"))

    return render_template("new_project.html")


# ── Project detail ───────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("project_detail.html", project=project)


# ── Add expense ──────────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>/add-expense", methods=["POST"])
def add_expense(project_id):
    project = Project.query.get_or_404(project_id)

    description = request.form["description"].strip()
    category    = request.form["category"]

    if not description:
        flash("Description is required.", "danger")
        return redirect(url_for("main.project_detail", project_id=project_id))

    if len(description) > 200:
        flash("Description must be under 200 characters.", "danger")
        return redirect(url_for("main.project_detail", project_id=project_id))

    try:
        amount = float(request.form["amount"])
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Amount must be a positive number.", "danger")
        return redirect(url_for("main.project_detail", project_id=project_id))

    try:
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format.", "danger")
        return redirect(url_for("main.project_detail", project_id=project_id))

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


# ── Delete expense ───────────────────────────────────────────────────────────
@main.route("/expense/<int:expense_id>/delete", methods=["POST"])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    project_id = expense.project_id

    db.session.delete(expense)
    db.session.commit()

    flash("Expense deleted successfully!", "success")
    return redirect(url_for("main.project_detail", project_id=project_id))


# ── Edit project ─────────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        name   = request.form["name"].strip()
        client = request.form["client"].strip()

        if not name or not client:
            flash("Name and client are required.", "danger")
            return redirect(url_for("main.edit_project", project_id=project_id))

        if len(name) > 100 or len(client) > 100:
            flash("Name and client must be under 100 characters.", "danger")
            return redirect(url_for("main.edit_project", project_id=project_id))

        try:
            budget = float(request.form["budget"])
            if budget <= 0:
                raise ValueError
        except ValueError:
            flash("Budget must be a positive number.", "danger")
            return redirect(url_for("main.edit_project", project_id=project_id))

        try:
            start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("main.edit_project", project_id=project_id))

        project.name       = name
        project.client     = client
        project.budget     = budget
        project.start_date = start_date

        db.session.commit()

        flash("Project updated successfully!", "success")
        return redirect(url_for("main.project_detail", project_id=project.id))

    return render_template("edit_project.html", project=project)


# ── Edit expense ─────────────────────────────────────────────────────────────
@main.route("/expense/<int:expense_id>/edit", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == "POST":
        description = request.form["description"].strip()
        category    = request.form["category"]

        if not description:
            flash("Description is required.", "danger")
            return redirect(url_for("main.edit_expense", expense_id=expense_id))

        if len(description) > 200:
            flash("Description must be under 200 characters.", "danger")
            return redirect(url_for("main.edit_expense", expense_id=expense_id))

        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Amount must be a positive number.", "danger")
            return redirect(url_for("main.edit_expense", expense_id=expense_id))

        try:
            date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return redirect(url_for("main.edit_expense", expense_id=expense_id))

        expense.description = description
        expense.category    = category
        expense.amount      = amount
        expense.date        = date

        db.session.commit()

        flash("Expense updated successfully!", "success")
        return redirect(url_for("main.project_detail", project_id=expense.project_id))

    return render_template("edit_expense.html", expense=expense)