from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    password   = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects   = db.relationship("Project", backref="owner", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Project(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    client     = db.Column(db.String(100), nullable=False)
    budget     = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    status     = db.Column(db.String(20), default="active")
    user_id    = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    expenses = db.relationship("Expense", backref="project", lazy=True, cascade="all, delete-orphan")


class Expense(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    project_id  = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    category    = db.Column(db.String(50), nullable=False)
    amount      = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    date        = db.Column(db.Date, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)