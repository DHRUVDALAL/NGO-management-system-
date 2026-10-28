import os
import random
import string
from functools import wraps
from datetime import datetime, date

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify, abort
)
from sqlalchemy import func

from config import Config
from database.db import db
from database.models import Admin, Volunteer, Student, CampEvent, Donation, ContactMessage
from database.seed_data import seed_database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database folder exists for SQLite fallback
    db_folder = os.path.join(app.root_path, 'database')
    os.makedirs(db_folder, exist_ok=True)

    db.init_app(app)

    # Initialize tables and seed realistic sample records
    with app.app_context():
        db.create_all()
        seed_database()

    # -------------------------------------------------------------------------
    # Authentication Decorator
    # -------------------------------------------------------------------------
    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('admin_id'):
                flash('Please log in with administrative credentials to access the control center.', 'warning')
                return redirect(url_for('admin_login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function

    def generate_receipt_number():
        """Generates a unique receipt code: YSF-2026-XXXX"""
        suffix = ''.join(random.choices(string.digits, k=4))
        return f"YSF-{datetime.utcnow().year}-{suffix}"

    # -------------------------------------------------------------------------
    # Public Routes
    # -------------------------------------------------------------------------
    @app.route('/')
    def home():
        total_volunteers = Volunteer.query.count()
        active_volunteers = Volunteer.query.filter_by(status='Active').count()
        total_students = Student.query.count()
        total_donations = db.session.query(func.coalesce(func.sum(Donation.amount), 0.0)).scalar()
        events = CampEvent.query.order_by(CampEvent.event_date.asc()).all()

        return render_template(
            'index.html',
            total_volunteers=total_volunteers,
            active_volunteers=active_volunteers,
            total_students=total_students,
            total_donations=float(total_donations),
            events=events
        )

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/programs')
    def programs():
        return render_template('programs.html')

    @app.route('/events')
    def events():
        all_events = CampEvent.query.order_by(CampEvent.event_date.asc()).all()
        return render_template('events.html', events=all_events)

    # Volunteer Registration (Chapter 5.4)
    @app.route('/volunteer-register', methods=['GET', 'POST'])
    def volunteer_register():
        if request.method == 'POST':
            full_name = request.form.get('full_name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            date_of_birth_str = request.form.get('date_of_birth', '').strip()
            address = request.form.get('address', '').strip()
            skills = request.form.get('skills', '').strip()
            preferred_activity = request.form.get('preferred_activity', '').strip()

            if not full_name or not email or not phone or not preferred_activity:
                flash('Please fill in all required fields (Name, Email, Phone, Preferred Activity).', 'error')
                return render_template('volunteer_register.html')

            dob = None
            if date_of_birth_str:
                try:
                    dob = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
                except ValueError:
                    dob = None

            new_volunteer = Volunteer(
                full_name=full_name,
                email=email,
                phone=phone,
                date_of_birth=dob,
                address=address,
                skills=skills,
                preferred_activity=preferred_activity,
                status='Active',
                joined_date=date.today()
            )

            db.session.add(new_volunteer)
            db.session.commit()

            flash(f'Thank you, {full_name}! Your volunteer registration has been successfully recorded in our foundation database.', 'success')
            return redirect(url_for('home'))

        return render_template('volunteer_register.html')

    # Donation Form & 80G Receipt (Chapter 5.5)
    @app.route('/donate', methods=['GET', 'POST'])
    def donate():
        events_list = CampEvent.query.order_by(CampEvent.event_date.desc()).all()
        selected_event_id = request.args.get('event_id', type=int)

        if request.method == 'POST':
            donor_name = request.form.get('donor_name', '').strip()
            donor_email = request.form.get('donor_email', '').strip()
            donor_phone = request.form.get('donor_phone', '').strip()
            amount_str = request.form.get('amount', '').strip()
            event_id = request.form.get('event_id', type=int)
            payment_mode = request.form.get('payment_mode', 'UPI').strip()
            transaction_ref = request.form.get('transaction_ref', '').strip()

            if not donor_name or not donor_email or not amount_str:
                flash('Please provide donor name, valid email, and contribution amount.', 'error')
                return render_template('donate.html', events=events_list, selected_event_id=selected_event_id)

            try:
                amount = float(amount_str)
                if amount <= 0:
                    raise ValueError()
            except ValueError:
                flash('Please enter a valid positive donation amount.', 'error')
                return render_template('donate.html', events=events_list, selected_event_id=selected_event_id)

            # Determine cause name and update event raised budget if linked
            cause_name = 'General Foundation Fund'
            if event_id:
                ev = CampEvent.query.get(event_id)
                if ev:
                    cause_name = f"Camp: {ev.title}"
                    ev.raised_budget = float(ev.raised_budget or 0) + amount

            # Generate unique reference if blank
            if not transaction_ref:
                transaction_ref = f"PAY_{payment_mode.upper()}_{random.randint(100000, 999999)}"

            receipt_number = generate_receipt_number()
            # Ensure unique receipt number
            while Donation.query.filter_by(receipt_number=receipt_number).first():
                receipt_number = generate_receipt_number()

            new_donation = Donation(
                donor_name=donor_name,
                donor_email=donor_email,
                donor_phone=donor_phone,
                amount=amount,
                event_id=event_id if event_id else None,
                cause_name=cause_name,
                payment_mode=payment_mode,
                transaction_ref=transaction_ref,
                receipt_number=receipt_number,
                donation_date=date.today()
            )

            db.session.add(new_donation)
            db.session.commit()

            flash(f'Thank you, {donor_name}! Your contribution of ₹{amount:,.2f} has been verified and recorded.', 'success')
            return redirect(url_for('view_receipt', receipt_no=receipt_number))

        return render_template('donate.html', events=events_list, selected_event_id=selected_event_id)

    @app.route('/receipt/<receipt_no>')
    def view_receipt(receipt_no):
        donation = Donation.query.filter_by(receipt_number=receipt_no).first_or_404()
        return render_template('receipt.html', donation=donation)

    # Student Beneficiary Registration (User Request Addition)
    @app.route('/student-register', methods=['GET', 'POST'])
    def student_register():
        if request.method == 'POST':
            student_name = request.form.get('student_name', '').strip()
            dob_str = request.form.get('dob', '').strip()
            age_str = request.form.get('age', '').strip()
            gender = request.form.get('gender', '').strip()
            guardian_name = request.form.get('guardian_name', '').strip()
            guardian_phone = request.form.get('guardian_phone', '').strip()
            school_grade = request.form.get('school_grade', '').strip()
            assistance_type = request.form.get('assistance_type', '').strip()

            if not student_name or not dob_str or not age_str or not guardian_name or not guardian_phone:
                flash('Please complete all mandatory student and guardian fields.', 'error')
                return render_template('student_register.html')

            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                age = int(age_str)
            except ValueError:
                flash('Invalid date of birth or age provided.', 'error')
                return render_template('student_register.html')

            new_student = Student(
                student_name=student_name,
                dob=dob,
                age=age,
                gender=gender,
                guardian_name=guardian_name,
                guardian_phone=guardian_phone,
                school_grade=school_grade,
                assistance_type=assistance_type,
                status='Active',
                enrolled_date=date.today()
            )

            db.session.add(new_student)
            db.session.commit()

            flash(f'Beneficiary profile for {student_name} successfully enrolled in YuvaShakti Welfare Program.', 'success')
            return redirect(url_for('home'))

        return render_template('student_register.html')

    # Contact Inquiries (Chapter 5.6)
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()

            if not name or not email or not subject or not message:
                flash('Please provide your name, email, subject, and message.', 'error')
                return render_template('contact.html')

            new_msg = ContactMessage(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                status='New'
            )

            db.session.add(new_msg)
            db.session.commit()

            flash('Your inquiry has been logged in our system. An administrator will respond shortly.', 'success')
            return redirect(url_for('contact'))

        return render_template('contact.html')

    # -------------------------------------------------------------------------
    # Admin Authentication
    # -------------------------------------------------------------------------
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if session.get('admin_id'):
            return redirect(url_for('admin_dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()

            admin = Admin.query.filter_by(username=username).first()

            if admin and admin.check_password(password):
                session['admin_id'] = admin.id
                session['admin_username'] = admin.username
                session['admin_name'] = admin.full_name
                admin.last_login = datetime.utcnow()
                db.session.commit()

                flash(f'Welcome back, {admin.full_name}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('admin_dashboard'))
            else:
                flash('Invalid username or password. Please verify credentials.', 'error')

        return render_template('admin/login.html')

    @app.route('/admin/logout')
    def admin_logout():
        session.clear()
        flash('You have been signed out from the Admin Control Center.', 'info')
        return redirect(url_for('admin_login'))

    # -------------------------------------------------------------------------
    # Admin Dashboard & Operations (Chapter 5.7)
    # -------------------------------------------------------------------------
    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        total_volunteers = Volunteer.query.count()
        active_volunteers = Volunteer.query.filter_by(status='Active').count()
        total_students = Student.query.count()
        total_donors = db.session.query(func.count(func.distinct(Donation.donor_email))).scalar() or 0
        total_donations = db.session.query(func.coalesce(func.sum(Donation.amount), 0.0)).scalar() or 0.0
        total_camps = CampEvent.query.count()

        # Volunteer preferred activity distribution for Chart.js
        activity_stats = (
            db.session.query(Volunteer.preferred_activity, func.count(Volunteer.id))
            .group_by(Volunteer.preferred_activity)
            .all()
        )
        activity_labels = [row[0] for row in activity_stats] if activity_stats else ["No data"]
        activity_counts = [row[1] for row in activity_stats] if activity_stats else [0]

        # Donation cause breakdown for Chart.js
        donation_stats = (
            db.session.query(Donation.cause_name, func.sum(Donation.amount))
            .group_by(Donation.cause_name)
            .limit(6)
            .all()
        )
        donation_labels = [row[0] for row in donation_stats] if donation_stats else ["General Fund"]
        donation_amounts = [float(row[1]) for row in donation_stats] if donation_stats else [0.0]

        recent_volunteers = Volunteer.query.order_by(Volunteer.id.desc()).limit(5).all()
        recent_donations = Donation.query.order_by(Donation.id.desc()).limit(5).all()

        return render_template(
            'admin/dashboard.html',
            total_volunteers=total_volunteers,
            active_volunteers=active_volunteers,
            total_students=total_students,
            total_donors=total_donors,
            total_donations=float(total_donations),
            total_camps=total_camps,
            activity_labels=activity_labels,
            activity_counts=activity_counts,
            donation_labels=donation_labels,
            donation_amounts=donation_amounts,
            recent_volunteers=recent_volunteers,
            recent_donations=recent_donations
        )

    # Volunteers Management
    @app.route('/admin/volunteers')
    @admin_required
    def admin_volunteers():
        all_volunteers = Volunteer.query.order_by(Volunteer.id.desc()).all()
        return render_template('admin/volunteers.html', volunteers=all_volunteers)

    @app.route('/admin/volunteers/status', methods=['POST'])
    @admin_required
    def admin_volunteer_status():
        data = request.get_json() or {}
        vol_id = data.get('id')
        new_status = data.get('status')

        vol = Volunteer.query.get(vol_id)
        if not vol:
            return jsonify({'success': False, 'message': 'Volunteer not found'}), 404

        vol.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status})

    @app.route('/admin/volunteers/delete/<int:id>', methods=['POST'])
    @admin_required
    def admin_delete_volunteer(id):
        vol = Volunteer.query.get_or_404(id)
        db.session.delete(vol)
        db.session.commit()
        flash(f'Volunteer {vol.full_name} deleted from records.', 'info')
        return redirect(url_for('admin_volunteers'))

    # Donations Log
    @app.route('/admin/donations')
    @admin_required
    def admin_donations():
        all_donations = Donation.query.order_by(Donation.id.desc()).all()
        return render_template('admin/donations.html', donations=all_donations)

    # Student Beneficiaries Management
    @app.route('/admin/students')
    @admin_required
    def admin_students():
        all_students = Student.query.order_by(Student.id.desc()).all()
        return render_template('admin/students.html', students=all_students)

    @app.route('/admin/students/status', methods=['POST'])
    @admin_required
    def admin_student_status():
        data = request.get_json() or {}
        student_id = data.get('id')
        new_status = data.get('status')

        stu = Student.query.get(student_id)
        if not stu:
            return jsonify({'success': False, 'message': 'Student not found'}), 404

        stu.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status})

    @app.route('/admin/students/delete/<int:id>', methods=['POST'])
    @admin_required
    def admin_delete_student(id):
        stu = Student.query.get_or_404(id)
        db.session.delete(stu)
        db.session.commit()
        flash(f'Beneficiary record for {stu.student_name} deleted.', 'info')
        return redirect(url_for('admin_students'))

    # Camps & Events Management
    @app.route('/admin/events')
    @admin_required
    def admin_events():
        all_events = CampEvent.query.order_by(CampEvent.event_date.desc()).all()
        return render_template('admin/events.html', events=all_events)

    @app.route('/admin/events/create', methods=['POST'])
    @admin_required
    def admin_create_event():
        title = request.form.get('title', '').strip()
        event_type = request.form.get('event_type', '').strip()
        description = request.form.get('description', '').strip()
        venue = request.form.get('venue', '').strip()
        event_date_str = request.form.get('event_date', '').strip()
        target_budget = request.form.get('target_budget', 0, type=float)
        volunteer_capacity = request.form.get('volunteer_capacity', 25, type=int)

        if not title or not event_date_str or not venue:
            flash('Please provide event title, date, and venue.', 'error')
            return redirect(url_for('admin_events'))

        try:
            ev_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid event date specified.', 'error')
            return redirect(url_for('admin_events'))

        new_event = CampEvent(
            title=title,
            event_type=event_type,
            description=description,
            venue=venue,
            event_date=ev_date,
            target_budget=target_budget,
            raised_budget=0.0,
            volunteer_capacity=volunteer_capacity,
            status='Upcoming'
        )

        db.session.add(new_event)
        db.session.commit()

        flash(f'Welfare event "{title}" successfully scheduled.', 'success')
        return redirect(url_for('admin_events'))

    @app.route('/admin/events/status', methods=['POST'])
    @admin_required
    def admin_event_status():
        data = request.get_json() or {}
        event_id = data.get('id')
        new_status = data.get('status')

        ev = CampEvent.query.get(event_id)
        if not ev:
            return jsonify({'success': False, 'message': 'Event not found'}), 404

        ev.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status})

    @app.route('/admin/events/delete/<int:id>', methods=['POST'])
    @admin_required
    def admin_delete_event(id):
        ev = CampEvent.query.get_or_404(id)
        db.session.delete(ev)
        db.session.commit()
        flash(f'Event "{ev.title}" removed from schedule.', 'info')
        return redirect(url_for('admin_events'))

    # Contact Inquiries Management
    @app.route('/admin/messages')
    @admin_required
    def admin_messages():
        all_messages = ContactMessage.query.order_by(ContactMessage.id.desc()).all()
        return render_template('admin/messages.html', messages=all_messages)

    @app.route('/admin/messages/status', methods=['POST'])
    @admin_required
    def admin_message_status():
        data = request.get_json() or {}
        msg_id = data.get('id')
        new_status = data.get('status')

        msg = ContactMessage.query.get(msg_id)
        if not msg:
            return jsonify({'success': False, 'message': 'Message not found'}), 404

        msg.status = new_status
        db.session.commit()
        return jsonify({'success': True, 'status': new_status})

    @app.route('/admin/messages/delete/<int:id>', methods=['POST'])
    @admin_required
    def admin_delete_message(id):
        msg = ContactMessage.query.get_or_404(id)
        db.session.delete(msg)
        db.session.commit()
        flash('Inquiry message removed.', 'info')
        return redirect(url_for('admin_messages'))

    return app

app = create_app()

if __name__ == '__main__':
    # Run development server on port 5001
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
