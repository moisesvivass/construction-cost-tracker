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
        return redirect(url_for("main.dashboard"))

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
        return redirect(url_for("main.dashboard"))

    if request.method == "POST":
        email    = request.form["email"].strip().lower()
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("main.login"))

        login_user(user)
        flash(f"Welcome back, {user.username}!", "success")
        return redirect(url_for("main.dashboard"))

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
    return redirect(url_for("main.dashboard"))


# ── Setup ─────────────────────────────────────────────────────────────────────
@main.route("/setup")
def setup():
    import os
    from datetime import date
    key = request.args.get("key")
    if key != os.getenv("SETUP_KEY"):
        return "Unauthorized", 403

    if User.query.filter_by(email="demo@costtracker.com").first():
        return "Demo data already exists!", 200

    demo = User(username="demo", email="demo@costtracker.com")
    demo.set_password("demo1234")
    db.session.add(demo)
    db.session.commit()

    p1 = Project(name="Riverside Renovation", client="John & Sarah Mitchell", budget=85000.00, start_date=date(2024, 1, 15), status="completed", user_id=demo.id)
    db.session.add(p1)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p1.id, description="Concrete foundation repair",   category="Materials",  amount=4200.00,  date=date(2024, 1, 20)),
        Expense(project_id=p1.id, description="Framing crew — week 1",        category="Labor",      amount=6800.00,  date=date(2024, 1, 27)),
        Expense(project_id=p1.id, description="Lumber and structural beams",  category="Materials",  amount=3150.00,  date=date(2024, 2, 3)),
        Expense(project_id=p1.id, description="Electrical rough-in",          category="Labor",      amount=5200.00,  date=date(2024, 2, 10)),
        Expense(project_id=p1.id, description="Plumbing rough-in",            category="Labor",      amount=4800.00,  date=date(2024, 2, 17)),
        Expense(project_id=p1.id, description="Drywall materials",            category="Materials",  amount=2900.00,  date=date(2024, 2, 24)),
        Expense(project_id=p1.id, description="Excavator rental — 3 days",   category="Tools",      amount=1800.00,  date=date(2024, 3, 2)),
        Expense(project_id=p1.id, description="Material delivery — truck",    category="Transport",  amount=650.00,   date=date(2024, 3, 9)),
        Expense(project_id=p1.id, description="Interior painting crew",       category="Labor",      amount=3200.00,  date=date(2024, 3, 16)),
        Expense(project_id=p1.id, description="Flooring installation",        category="Materials",  amount=8400.00,  date=date(2024, 3, 23)),
    ])
    db.session.commit()

    p2 = Project(name="Downtown Office Fit-out", client="Apex Consulting Group", budget=120000.00, start_date=date(2024, 3, 1), status="completed", user_id=demo.id)
    db.session.add(p2)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p2.id, description="Demolition crew",              category="Labor",      amount=8500.00,  date=date(2024, 3, 5)),
        Expense(project_id=p2.id, description="Steel stud framing",           category="Materials",  amount=6200.00,  date=date(2024, 3, 12)),
        Expense(project_id=p2.id, description="HVAC system installation",     category="Labor",      amount=18000.00, date=date(2024, 3, 19)),
        Expense(project_id=p2.id, description="Acoustic ceiling tiles",       category="Materials",  amount=4100.00,  date=date(2024, 3, 26)),
        Expense(project_id=p2.id, description="Commercial flooring",          category="Materials",  amount=9800.00,  date=date(2024, 4, 2)),
        Expense(project_id=p2.id, description="Electrical panel upgrade",     category="Labor",      amount=7200.00,  date=date(2024, 4, 9)),
        Expense(project_id=p2.id, description="Scaffolding rental — 2 weeks", category="Tools",     amount=2400.00,  date=date(2024, 4, 16)),
        Expense(project_id=p2.id, description="Paint and finishing crew",     category="Labor",      amount=5600.00,  date=date(2024, 4, 23)),
        Expense(project_id=p2.id, description="Equipment transport",          category="Transport",  amount=980.00,   date=date(2024, 4, 30)),
        Expense(project_id=p2.id, description="Glass partition walls",        category="Materials",  amount=14200.00, date=date(2024, 5, 7)),
        Expense(project_id=p2.id, description="Security system installation", category="Labor",      amount=6800.00,  date=date(2024, 5, 14)),
    ])
    db.session.commit()

    p3 = Project(name="Westside Parking Lot", client="City of Toronto", budget=45000.00, start_date=date(2024, 5, 1), status="completed", user_id=demo.id)
    db.session.add(p3)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p3.id, description="Asphalt materials",            category="Materials",  amount=12000.00, date=date(2024, 5, 5)),
        Expense(project_id=p3.id, description="Grading and excavation crew",  category="Labor",      amount=8500.00,  date=date(2024, 5, 12)),
        Expense(project_id=p3.id, description="Line marking equipment",       category="Tools",      amount=1200.00,  date=date(2024, 5, 19)),
        Expense(project_id=p3.id, description="Drainage pipe materials",      category="Materials",  amount=3400.00,  date=date(2024, 5, 26)),
        Expense(project_id=p3.id, description="Paving crew",                  category="Labor",      amount=7800.00,  date=date(2024, 6, 2)),
        Expense(project_id=p3.id, description="Material transport — 4 loads", category="Transport",  amount=1600.00,  date=date(2024, 6, 9)),
    ])
    db.session.commit()

    p4 = Project(name="Lakeview School Gymnasium", client="Toronto District School Board", budget=210000.00, start_date=date(2024, 6, 1), status="active", user_id=demo.id)
    db.session.add(p4)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p4.id, description="Foundation and concrete work",  category="Materials",  amount=28000.00, date=date(2024, 6, 8)),
        Expense(project_id=p4.id, description="Structural steel installation", category="Labor",      amount=22000.00, date=date(2024, 6, 15)),
        Expense(project_id=p4.id, description="Roofing materials",             category="Materials",  amount=16500.00, date=date(2024, 6, 22)),
        Expense(project_id=p4.id, description="Roofing crew",                  category="Labor",      amount=12000.00, date=date(2024, 6, 29)),
        Expense(project_id=p4.id, description="Crane rental — 1 week",        category="Tools",      amount=8500.00,  date=date(2024, 7, 6)),
        Expense(project_id=p4.id, description="Electrical rough-in",          category="Labor",      amount=9800.00,  date=date(2024, 7, 13)),
        Expense(project_id=p4.id, description="Heavy equipment transport",    category="Transport",  amount=2200.00,  date=date(2024, 7, 20)),
    ])
    db.session.commit()

    p5 = Project(name="Harbourfront Condo Lobby", client="Harbourfront Condo Corp", budget=62000.00, start_date=date(2024, 7, 10), status="completed", user_id=demo.id)
    db.session.add(p5)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p5.id, description="Marble flooring materials",    category="Materials",  amount=18000.00, date=date(2024, 7, 15)),
        Expense(project_id=p5.id, description="Tile installation crew",       category="Labor",      amount=7500.00,  date=date(2024, 7, 22)),
        Expense(project_id=p5.id, description="Custom reception desk",        category="Materials",  amount=8200.00,  date=date(2024, 7, 29)),
        Expense(project_id=p5.id, description="Lighting upgrade",             category="Materials",  amount=4600.00,  date=date(2024, 8, 5)),
        Expense(project_id=p5.id, description="Electrician — lighting install", category="Labor",    amount=3800.00,  date=date(2024, 8, 12)),
        Expense(project_id=p5.id, description="Painting and finishing",       category="Labor",      amount=2900.00,  date=date(2024, 8, 19)),
        Expense(project_id=p5.id, description="Delivery — marble slabs",      category="Transport",  amount=1100.00,  date=date(2024, 8, 26)),
    ])
    db.session.commit()

    p6 = Project(name="Etobicoke Warehouse Expansion", client="GTA Logistics Inc.", budget=175000.00, start_date=date(2024, 8, 1), status="active", user_id=demo.id)
    db.session.add(p6)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p6.id, description="Site preparation and grading", category="Labor",      amount=14000.00, date=date(2024, 8, 8)),
        Expense(project_id=p6.id, description="Concrete slab pour",           category="Materials",  amount=32000.00, date=date(2024, 8, 15)),
        Expense(project_id=p6.id, description="Steel frame structure",        category="Materials",  amount=41000.00, date=date(2024, 8, 22)),
        Expense(project_id=p6.id, description="Welding and assembly crew",    category="Labor",      amount=18500.00, date=date(2024, 8, 29)),
        Expense(project_id=p6.id, description="Forklift rental — 2 weeks",   category="Tools",      amount=3200.00,  date=date(2024, 9, 5)),
        Expense(project_id=p6.id, description="Steel delivery — 3 loads",    category="Transport",  amount=2800.00,  date=date(2024, 9, 12)),
    ])
    db.session.commit()

    p7 = Project(name="King Street Restaurant", client="Moreno Hospitality Group", budget=95000.00, start_date=date(2024, 9, 1), status="completed", user_id=demo.id)
    db.session.add(p7)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p7.id, description="Commercial kitchen equipment", category="Materials",  amount=28000.00, date=date(2024, 9, 8)),
        Expense(project_id=p7.id, description="Kitchen installation crew",    category="Labor",      amount=9500.00,  date=date(2024, 9, 15)),
        Expense(project_id=p7.id, description="Bar and counter materials",    category="Materials",  amount=11200.00, date=date(2024, 9, 22)),
        Expense(project_id=p7.id, description="Plumbing — kitchen & bar",     category="Labor",      amount=8800.00,  date=date(2024, 9, 29)),
        Expense(project_id=p7.id, description="Exhaust hood system",          category="Materials",  amount=6400.00,  date=date(2024, 10, 6)),
        Expense(project_id=p7.id, description="Interior design crew",         category="Labor",      amount=7200.00,  date=date(2024, 10, 13)),
        Expense(project_id=p7.id, description="Equipment delivery",           category="Transport",  amount=1500.00,  date=date(2024, 10, 20)),
        Expense(project_id=p7.id, description="Power tools rental",           category="Tools",      amount=850.00,   date=date(2024, 10, 27)),
    ])
    db.session.commit()

    p8 = Project(name="Highway 27 Bridge Repair", client="Ontario Ministry of Transport", budget=380000.00, start_date=date(2024, 10, 1), status="active", user_id=demo.id)
    db.session.add(p8)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p8.id, description="Structural assessment crew",   category="Labor",      amount=22000.00, date=date(2024, 10, 8)),
        Expense(project_id=p8.id, description="Concrete repair materials",    category="Materials",  amount=45000.00, date=date(2024, 10, 15)),
        Expense(project_id=p8.id, description="Steel reinforcement bars",     category="Materials",  amount=38000.00, date=date(2024, 10, 22)),
        Expense(project_id=p8.id, description="Heavy equipment rental",       category="Tools",      amount=24000.00, date=date(2024, 10, 29)),
        Expense(project_id=p8.id, description="Concrete pouring crew",        category="Labor",      amount=31000.00, date=date(2024, 11, 5)),
        Expense(project_id=p8.id, description="Material transport — 8 loads", category="Transport",  amount=6400.00,  date=date(2024, 11, 12)),
    ])
    db.session.commit()

    p9 = Project(name="Scarborough Medical Clinic", client="HealthFirst Properties", budget=130000.00, start_date=date(2024, 11, 1), status="active", user_id=demo.id)
    db.session.add(p9)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p9.id, description="Partition wall framing",       category="Materials",  amount=8500.00,  date=date(2024, 11, 8)),
        Expense(project_id=p9.id, description="Framing and drywall crew",     category="Labor",      amount=12000.00, date=date(2024, 11, 15)),
        Expense(project_id=p9.id, description="Medical grade flooring",       category="Materials",  amount=14200.00, date=date(2024, 11, 22)),
        Expense(project_id=p9.id, description="HVAC filtration upgrade",      category="Materials",  amount=18500.00, date=date(2024, 11, 29)),
        Expense(project_id=p9.id, description="Electrical and data wiring",   category="Labor",      amount=11000.00, date=date(2024, 12, 6)),
        Expense(project_id=p9.id, description="Specialized equipment delivery", category="Transport", amount=1800.00, date=date(2024, 12, 13)),
    ])
    db.session.commit()

    p10 = Project(name="Yorkville Rooftop Deck", client="Prime Properties Ltd.", budget=58000.00, start_date=date(2025, 1, 10), status="active", user_id=demo.id)
    db.session.add(p10)
    db.session.commit()
    db.session.add_all([
        Expense(project_id=p10.id, description="Waterproof membrane materials", category="Materials", amount=9800.00,  date=date(2025, 1, 17)),
        Expense(project_id=p10.id, description="Membrane installation crew",    category="Labor",     amount=7200.00,  date=date(2025, 1, 24)),
        Expense(project_id=p10.id, description="Composite decking boards",      category="Materials", amount=12400.00, date=date(2025, 1, 31)),
        Expense(project_id=p10.id, description="Carpentry crew",                category="Labor",     amount=8500.00,  date=date(2025, 2, 7)),
        Expense(project_id=p10.id, description="Glass railing system",          category="Materials", amount=7600.00,  date=date(2025, 2, 14)),
        Expense(project_id=p10.id, description="Material hoisting equipment",   category="Tools",     amount=2100.00,  date=date(2025, 2, 21)),
        Expense(project_id=p10.id, description="Rooftop material delivery",     category="Transport", amount=950.00,   date=date(2025, 2, 28)),
    ])
    db.session.commit()

    return "✅ Demo data seeded successfully! 10 projects created.", 200


# ── Dashboard ────────────────────────────────────────────────────────────────
@main.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@main.route("/dashboard")
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()

    total_projects  = len(projects)
    total_budget    = sum(p.budget for p in projects)
    total_spent     = sum(sum(e.amount for e in p.expenses) for p in projects)
    total_remaining = total_budget - total_spent

    category_totals = {}
    for project in projects:
        for expense in project.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

    recent_projects = sorted(projects, key=lambda p: p.start_date, reverse=True)[:5]

    return render_template("dashboard.html",
        total_projects  = total_projects,
        total_budget    = total_budget,
        total_spent     = total_spent,
        total_remaining = total_remaining,
        category_totals = category_totals,
        projects        = projects,
        recent_projects = recent_projects,
    )


# ── Projects ─────────────────────────────────────────────────────────────────
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


# ── Export ───────────────────────────────────────────────────────────────────
@main.route("/project/<int:project_id>/export")
@login_required
def export_project(project_id):
    import csv
    import io
    from flask import Response

    project = Project.query.filter_by(id=project_id, user_id=current_user.id).first_or_404()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Project", "Client", "Budget", "Status", "Start Date"])
    writer.writerow([project.name, project.client, project.budget, project.status, project.start_date])
    writer.writerow([])
    writer.writerow(["Date", "Description", "Category", "Amount"])

    for expense in sorted(project.expenses, key=lambda e: e.date):
        writer.writerow([expense.date, expense.description, expense.category, expense.amount])

    writer.writerow([])
    writer.writerow(["", "", "Total", sum(e.amount for e in project.expenses)])

    output.seek(0)
    filename = f"{project.name.replace(' ', '_')}_expenses.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@main.route("/dashboard/export")
@login_required
def export_all():
    import csv
    import io
    from flask import Response

    projects = Project.query.filter_by(user_id=current_user.id).all()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Project", "Client", "Budget", "Status", "Start Date", "Date", "Description", "Category", "Amount"])

    for project in projects:
        for expense in sorted(project.expenses, key=lambda e: e.date):
            writer.writerow([
                project.name,
                project.client,
                project.budget,
                project.status,
                project.start_date,
                expense.date,
                expense.description,
                expense.category,
                expense.amount
            ])

    output.seek(0)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=all_projects.csv"}
    )


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