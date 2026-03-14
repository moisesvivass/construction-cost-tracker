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
        name="Riverside Renovation",
        client="John & Sarah Mitchell",
        budget=85000.00,
        start_date=date(2024, 1, 15),
        status="completed",
        user_id=demo.id
    )
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
    print("Project 1 created.")

    # ── Project 2: Commercial Office Fit-out ──────────────────────────────────
    p2 = Project(
        name="Downtown Office Fit-out",
        client="Apex Consulting Group",
        budget=120000.00,
        start_date=date(2024, 3, 1),
        status="completed",
        user_id=demo.id
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
        Expense(project_id=p2.id, description="Glass partition walls",        category="Materials",  amount=14200.00, date=date(2024, 5, 7)),
        Expense(project_id=p2.id, description="Security system installation", category="Labor",      amount=6800.00,  date=date(2024, 5, 14)),
    ])
    db.session.commit()
    print("Project 2 created.")

    # ── Project 3: Parking Lot ────────────────────────────────────────────────
    p3 = Project(
        name="Westside Parking Lot",
        client="City of Toronto",
        budget=45000.00,
        start_date=date(2024, 5, 1),
        status="completed",
        user_id=demo.id
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

    # ── Project 4: School Gymnasium ───────────────────────────────────────────
    p4 = Project(
        name="Lakeview School Gymnasium",
        client="Toronto District School Board",
        budget=210000.00,
        start_date=date(2024, 6, 1),
        status="active",
        user_id=demo.id
    )
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
    print("Project 4 created.")

    # ── Project 5: Condo Lobby Renovation ─────────────────────────────────────
    p5 = Project(
        name="Harbourfront Condo Lobby",
        client="Harbourfront Condo Corp",
        budget=62000.00,
        start_date=date(2024, 7, 10),
        status="completed",
        user_id=demo.id
    )
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
    print("Project 5 created.")

    # ── Project 6: Warehouse Expansion ───────────────────────────────────────
    p6 = Project(
        name="Etobicoke Warehouse Expansion",
        client="GTA Logistics Inc.",
        budget=175000.00,
        start_date=date(2024, 8, 1),
        status="active",
        user_id=demo.id
    )
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
    print("Project 6 created.")

    # ── Project 7: Restaurant Fit-out ─────────────────────────────────────────
    p7 = Project(
        name="King Street Restaurant",
        client="Moreno Hospitality Group",
        budget=95000.00,
        start_date=date(2024, 9, 1),
        status="completed",
        user_id=demo.id
    )
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
    print("Project 7 created.")

    # ── Project 8: Highway Bridge Repair ─────────────────────────────────────
    p8 = Project(
        name="Highway 27 Bridge Repair",
        client="Ontario Ministry of Transport",
        budget=380000.00,
        start_date=date(2024, 10, 1),
        status="active",
        user_id=demo.id
    )
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
    print("Project 8 created.")

    # ── Project 9: Medical Clinic Renovation ──────────────────────────────────
    p9 = Project(
        name="Scarborough Medical Clinic",
        client="HealthFirst Properties",
        budget=130000.00,
        start_date=date(2024, 11, 1),
        status="active",
        user_id=demo.id
    )
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
    print("Project 9 created.")

    # ── Project 10: Rooftop Deck ──────────────────────────────────────────────
    p10 = Project(
        name="Yorkville Rooftop Deck",
        client="Prime Properties Ltd.",
        budget=58000.00,
        start_date=date(2025, 1, 10),
        status="active",
        user_id=demo.id
    )
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
    print("Project 10 created.")

    print("\n✅ Demo data seeded successfully!")
    print("   Email:    demo@costtracker.com")
    print("   Password: demo1234")
    print("   Projects: 10 (4 completed, 6 active)")