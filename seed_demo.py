from app import create_app, db
from app.models import User, Project, Expense
from datetime import date

app = create_app()

with app.app_context():

    # ── Delete existing demo data ────────────────────────────────────────────
    demo_user = User.query.filter_by(email="demo@costtracker.com").first()
    if demo_user:
        Project.query.filter_by(user_id=demo_user.id).delete()
        db.session.delete(demo_user)
        db.session.commit()
        print("Old demo data deleted.")

    # ── Create demo user ─────────────────────────────────────────────────────
    demo = User(username="demo", email="demo@costtracker.com")
    demo.set_password("demo1234")
    db.session.add(demo)
    db.session.commit()
    print("Demo user created.")

    # ── Project 1: Residential Renovation ────────────────────────────────────
    p1 = Project(
        name       = "Riverside Renovation",
        client     = "John & Sarah Mitchell",
        budget     = 85000.00,
        start_date = date(2024, 1, 15),
        status     = "active",
        user_id    = demo.id
    )
    db.session.add(p1)
    db.session.commit()

    db.session.add_all([
        Expense(project_id=p1.id, description="Concrete foundation repair",  category="Materials",  amount=4200.00,  date=date(2024, 1, 20)),
        Expense(project_id=p1.id, description="Framing crew — week 1",       category="Labor",      amount=6800.00,  date=date(2024, 1, 27)),
        Expense(project_id=p1.id, description="Lumber and structural beams",  category="Materials",  amount=3150.00,  date=date(2024, 2, 3)),
        Expense(project_id=p1.id, description="Electrical rough-in",          category="Labor",      amount=5200.00,  date=date(2024, 2, 10)),
        Expense(project_id=p1.id, description="Plumbing rough-in",            category="Labor",      amount=4800.00,  date=date(2024, 2, 17)),
        Expense(project_id=p1.id, description="Drywall materials",            category="Materials",  amount=2900.00,  date=date(2024, 2, 24)),
        Expense(project_id=p1.id, description="Excavator rental — 3 days",   category="Tools",      amount=1800.00,  date=date(2024, 3, 2)),
        Expense(project_id=p1.id, description="Material delivery — truck",    category="Transport",  amount=650.00,   date=date(2024, 3, 9)),
    ])
    db.session.commit()
    print("Project 1 created.")

    # ── Project 2: Commercial Office Fit-out ──────────────────────────────────
    p2 = Project(
        name       = "Downtown Office Fit-out",
        client     = "Apex Consulting Group",
        budget     = 120000.00,
        start_date = date(2024, 3, 1),
        status     = "active",
        user_id    = demo.id
    )
    db.session.add(p2)
    db.session.commit()

    db.session.add_all([
        Expense(project_id=p2.id, description="Demolition crew",              category="Labor",      amount=8500.00,  date=date(2024, 3, 5)),
        Expense(project_id=p2.id, description="Steel stud framing",           category="Materials",  amount=6200.00,  date=date(2024, 3, 12)),
        Expense(project_id=p2.id, description="HVAC system installation",     category="Labor",      amount=18000.00, date=date(2024, 3, 19)),
        Expense(project_id=p2.id, description="Acoustic ceiling tiles",       category="Materials",  amount=4100.00,  date=date(2024, 3, 26)),
        Expense(project_id=p2.id, description="Commercial flooring",          category="Materials",  amount=9800.00,  date=date(2024, 4, 2)),
        Expense(project_id=p2.id, description="Electrical panel upgrade",     category="Labor",      amount=7200.00,  date=date(2024, 4, 9)),
        Expense(project_id=p2.id, description="Scaffolding rental — 2 weeks", category="Tools",      amount=2400.00,  date=date(2024, 4, 16)),
        Expense(project_id=p2.id, description="Paint and finishing crew",     category="Labor",      amount=5600.00,  date=date(2024, 4, 23)),
        Expense(project_id=p2.id, description="Equipment transport",          category="Transport",  amount=980.00,   date=date(2024, 4, 30)),
    ])
    db.session.commit()
    print("Project 2 created.")

    # ── Project 3: Parking Lot ────────────────────────────────────────────────
    p3 = Project(
        name       = "Westside Parking Lot",
        client     = "City of Toronto",
        budget     = 45000.00,
        start_date = date(2024, 5, 1),
        status     = "active",
        user_id    = demo.id
    )
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
    print("Project 3 created.")

    print("\n✅ Demo data seeded successfully!")
    print("   Email:    demo@costtracker.com")
    print("   Password: demo1234")