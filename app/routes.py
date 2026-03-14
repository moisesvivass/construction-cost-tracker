from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, limiter
from app.models import Project, Expense, User
from datetime import datetime

main = Blueprint("main", __name__)


# ── Auth routes ──────────────────────────────────────────────────────────────
@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.projects"))

    if request.method == "POST":
        username = request.form["username"].strip()
        email    = request.form["email"].strip().lower()
        password = request.form["password"]

        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("main.register"))

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
            return redirect(url_for("main.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("main.register"))

        if User.query.filter_by(username=username).first():
            flash("Username already taken.", "danger")
            return redirect(url_for("main.register"))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.projects"))

    if request.method == "POST":
        email    = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("main.login"))

        login_user(user)
        flash(f"Welcome back, {user.username}!", "success")
        return redirect(url_for("main.projects"))

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))

@main.route("/demo-login")
@limiter.limit("5 per minute")
def demo_login():
    demo_user = User.query.filter_by(email="demo@costtracker.com").first()
    if not demo_user:
        flash("Demo account not available.", "warning")
        return redirect(url_for("main.login"))
    login_user(demo_user)
    flash("You are now viewing the demo account!", "info")
    return redirect(url_for("main.projects"))


# ── Projects ─────────────────────────────────────────────────────────────────
@main.route("/")
def index():
    return redirect(url_for("main.projects"))


@main.route("/projects")
@login_required
def projects():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "all")

    query = Project.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(
            db.or_(
                Project.name.ilike(f"%{search}%"),
                Project.client.ilike(f"%{search}%")
            )
        )

    if status != "all":
        query = query.filter_by(status=status)

    all_projects = query.all()

    return render_template("projects.html", projects=all_projects,
                           search=search, status=status)


@main.route("/projects/new", methods=["GET", "POST"])
@login_required
def new_project():
    if request.method == "POST":
        name   = request.form["name"].strip()
        client = request.form["client"].strip()

        if not name or not client:
            flash("Name and client are required.", "danger")
            return render_template("new_project.html", form_data=request.form)

        if len(name) > 100 or len(client) > 100:
            flash("Name and client must be under 100 characters.", "danger")
            return render_template("new_project.html", form_data=request.form)

        try:
            budget = float(request.form["budget"])
            if budget <= 0:
                raise ValueError
        except ValueError:
            flash("Budget must be a positive number.", "danger")
            return render_template("new_project.html", form_data=request.form)

        try:
            start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return render_template("new_project.html", form_data=request.form)

        project = Project(name=name, client=client, budget=budget,
                          start_date=start_date, user_id=current_user.id)
        db.session.add(project)
        db.session.commit()

        flash("Project created successfully!", "success")
        return redirect(url_for("main.projects"))

    return render_template("new_project.html", form_data=None)


# ── Project detail ───────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>")
@login_required
def project_detail(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()
    return render_template("project_detail.html", project=project)


# ── Add expense ──────────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>/add-expense", methods=["POST"])
@login_required
def add_expense(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()

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
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    project = Project.query.filter_by(id=expense.project_id, user_id=current_user.id).first_or_404()

    db.session.delete(expense)
    db.session.commit()

    flash("Expense deleted successfully!", "success")
    return redirect(url_for("main.project_detail", project_id=project.id))


# ── Edit project ─────────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        name   = request.form["name"].strip()
        client = request.form["client"].strip()

        if not name or not client:
            flash("Name and client are required.", "danger")
            return render_template("edit_project.html", project=project, form_data=request.form)

        if len(name) > 100 or len(client) > 100:
            flash("Name and client must be under 100 characters.", "danger")
            return render_template("edit_project.html", project=project, form_data=request.form)

        try:
            budget = float(request.form["budget"])
            if budget <= 0:
                raise ValueError
        except ValueError:
            flash("Budget must be a positive number.", "danger")
            return render_template("edit_project.html", project=project, form_data=request.form)

        try:
            start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return render_template("edit_project.html", project=project, form_data=request.form)

        project.name       = name
        project.client     = client
        project.budget     = budget
        project.start_date = start_date

        db.session.commit()

        flash("Project updated successfully!", "success")
        return redirect(url_for("main.project_detail", project_id=project.id))

    return render_template("edit_project.html", project=project, form_data=None)


# ── Delete project ───────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()

    db.session.delete(project)
    db.session.commit()

    flash("Project deleted successfully!", "success")
    return redirect(url_for("main.projects"))


# ── Edit expense ─────────────────────────────────────────────────────────────
@main.route("/expense/<int:expense_id>/edit", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    project = Project.query.filter_by(id=expense.project_id, user_id=current_user.id).first_or_404()

    if request.method == "POST":
        description = request.form["description"].strip()
        category    = request.form["category"]

        if not description:
            flash("Description is required.", "danger")
            return render_template("edit_expense.html", expense=expense, form_data=request.form)

        if len(description) > 200:
            flash("Description must be under 200 characters.", "danger")
            return render_template("edit_expense.html", expense=expense, form_data=request.form)

        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash("Amount must be a positive number.", "danger")
            return render_template("edit_expense.html", expense=expense, form_data=request.form)

        try:
            date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
        except ValueError:
            flash("Invalid date format.", "danger")
            return render_template("edit_expense.html", expense=expense, form_data=request.form)

        expense.description = description
        expense.category    = category
        expense.amount      = amount
        expense.date        = date

        db.session.commit()

        flash("Expense updated successfully!", "success")
        return redirect(url_for("main.project_detail", project_id=project.id))

    return render_template("edit_expense.html", expense=expense, form_data=None)