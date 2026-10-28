from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), default='Administrator')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'last_login': self.last_login.strftime('%Y-%m-%d %H:%M') if self.last_login else None
        }


class Volunteer(db.Model):
    __tablename__ = 'volunteers'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    preferred_activity = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(30), default='Active', index=True)  # 'Active', 'Pending', 'Inactive'
    joined_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else '',
            'address': self.address or '',
            'skills': self.skills or '',
            'preferred_activity': self.preferred_activity,
            'status': self.status,
            'joined_date': self.joined_date.strftime('%Y-%m-%d') if self.joined_date else '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    guardian_name = db.Column(db.String(120), nullable=False)
    guardian_phone = db.Column(db.String(30), nullable=False)
    school_grade = db.Column(db.String(80), nullable=False)
    assistance_type = db.Column(db.String(120), nullable=False)  # 'Free Tuition', 'Scholarship', 'Nutrition Program', 'School Supplies Kit'
    status = db.Column(db.String(30), default='Active', index=True)  # 'Active', 'Graduated', 'Suspended'
    enrolled_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_name': self.student_name,
            'dob': self.dob.strftime('%Y-%m-%d') if self.dob else '',
            'age': self.age,
            'gender': self.gender,
            'guardian_name': self.guardian_name,
            'guardian_phone': self.guardian_phone,
            'school_grade': self.school_grade,
            'assistance_type': self.assistance_type,
            'status': self.status,
            'enrolled_date': self.enrolled_date.strftime('%Y-%m-%d') if self.enrolled_date else '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class CampEvent(db.Model):
    __tablename__ = 'camps_events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    event_type = db.Column(db.String(80), nullable=False)  # 'Health Camp', 'Blood Donation', 'Education Drive', 'Food Distribution'
    description = db.Column(db.Text, nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    target_budget = db.Column(db.Float, default=0.0)
    raised_budget = db.Column(db.Float, default=0.0)
    volunteer_capacity = db.Column(db.Integer, default=30)
    status = db.Column(db.String(30), default='Upcoming', index=True)  # 'Upcoming', 'Ongoing', 'Completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donations = db.relationship('Donation', backref='event', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'event_type': self.event_type,
            'description': self.description,
            'venue': self.venue,
            'event_date': self.event_date.strftime('%Y-%m-%d') if self.event_date else '',
            'target_budget': float(self.target_budget or 0),
            'raised_budget': float(self.raised_budget or 0),
            'volunteer_capacity': self.volunteer_capacity,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(120), nullable=False)
    donor_email = db.Column(db.String(120), nullable=False)
    donor_phone = db.Column(db.String(30), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('camps_events.id'), nullable=True)
    cause_name = db.Column(db.String(150), default='General Foundation Fund')
    payment_mode = db.Column(db.String(50), nullable=False)  # 'UPI', 'NetBanking', 'Credit/Debit Card', 'Cash'
    transaction_ref = db.Column(db.String(100), nullable=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False)
    donation_date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'donor_name': self.donor_name,
            'donor_email': self.donor_email,
            'donor_phone': self.donor_phone or '',
            'amount': float(self.amount),
            'event_id': self.event_id,
            'cause_name': self.cause_name or (self.event.title if self.event else 'General Foundation Fund'),
            'payment_mode': self.payment_mode,
            'transaction_ref': self.transaction_ref or 'N/A',
            'receipt_number': self.receipt_number,
            'donation_date': self.donation_date.strftime('%Y-%m-%d') if self.donation_date else '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='New', index=True)  # 'New', 'In Review', 'Resolved'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone or '',
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else ''
        }
