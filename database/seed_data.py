from datetime import date, datetime, timedelta
from database.db import db
from database.models import Admin, Volunteer, Student, CampEvent, Donation, ContactMessage

def seed_database():
    """Seeds the database with realistic initial data if tables are empty."""

    # 1. Seed Admin
    if not Admin.query.first():
        admin = Admin(
            username='admin',
            full_name='YuvaShakti Director',
            email='director@yuvashakti.org',
            role='Super Administrator',
            created_at=datetime.utcnow() - timedelta(days=90),
            last_login=datetime.utcnow()
        )
        admin.set_password('admin123')
        db.session.add(admin)

    # 2. Seed Camps & Events
    if not CampEvent.query.first():
        events = [
            CampEvent(
                title="Slum Youth Education & Book Drive",
                event_type="Education Drive",
                description="Distributing curriculum textbooks, stationery kits, and school uniforms to 200+ underprivileged children.",
                venue="YuvaShakti Community Center, Sector 4",
                event_date=date.today() + timedelta(days=12),
                target_budget=60000.0,
                raised_budget=48500.0,
                volunteer_capacity=25,
                status="Upcoming"
            ),
            CampEvent(
                title="Free Community Eye & Dental Health Camp",
                event_type="Health Camp",
                description="Comprehensive medical screening, basic vision tests, and free spectacles distribution in collaboration with City Hospital.",
                venue="Govt Primary School Hall, East Ward",
                event_date=date.today() + timedelta(days=3),
                target_budget=45000.0,
                raised_budget=45000.0,
                volunteer_capacity=30,
                status="Ongoing"
            ),
            CampEvent(
                title="Mega Blood Donation & Health Awareness Drive",
                event_type="Blood Donation",
                description="Collaborative blood donation drive with Red Cross Society to support thalassemia patients and local blood banks.",
                venue="YuvaShakti Foundation Main Grounds",
                event_date=date.today() - timedelta(days=15),
                target_budget=30000.0,
                raised_budget=32500.0,
                volunteer_capacity=40,
                status="Completed"
            ),
            CampEvent(
                title="Warmth for All: Winter Relief & Food Kit Camp",
                event_type="Food Distribution",
                description="Provision of high-nutrition grain kits, warm blankets, and hygienic care packs to elderly citizens and street vendors.",
                venue="Railway Colony Shelter Grounds",
                event_date=date.today() + timedelta(days=25),
                target_budget=75000.0,
                raised_budget=38000.0,
                volunteer_capacity=35,
                status="Upcoming"
            )
        ]
        db.session.add_all(events)
        db.session.commit()

    # 3. Seed Volunteers
    if not Volunteer.query.first():
        volunteers = [
            Volunteer(
                full_name="Aarav Sharma",
                email="aarav.sharma@example.com",
                phone="+91 98231 45678",
                date_of_birth=date(1999, 4, 15),
                address="B-402, Green Valley Apartments, Mumbai",
                skills="Teaching, Mathematics, Youth Mentorship",
                preferred_activity="Education Support",
                status="Active",
                joined_date=date.today() - timedelta(days=120)
            ),
            Volunteer(
                full_name="Pooja Deshmukh",
                email="pooja.d@example.com",
                phone="+91 97654 32190",
                date_of_birth=date(2001, 8, 22),
                address="Flat 12, Sunrise Residency, Pune",
                skills="Nursing, First Aid, Medical Camp Logistics",
                preferred_activity="Health Camps",
                status="Active",
                joined_date=date.today() - timedelta(days=85)
            ),
            Volunteer(
                full_name="Rohan Verma",
                email="rohan.verma@example.com",
                phone="+91 99112 87654",
                date_of_birth=date(1998, 11, 5),
                address="Plot 55, Lakeview Enclave, Nagpur",
                skills="Social Media, Photography, Campaign Management",
                preferred_activity="Community Awareness",
                status="Active",
                joined_date=date.today() - timedelta(days=40)
            ),
            Volunteer(
                full_name="Sneha Iyer",
                email="sneha.iyer@example.com",
                phone="+91 98450 11234",
                date_of_birth=date(2002, 2, 18),
                address="24/7 Rose Garden Lane, Bengaluru",
                skills="Graphic Design, Art Workshops for Kids",
                preferred_activity="Youth Skill Development",
                status="Pending",
                joined_date=date.today() - timedelta(days=4)
            ),
            Volunteer(
                full_name="Karan Malhotra",
                email="karan.m@example.com",
                phone="+91 98991 76543",
                date_of_birth=date(1996, 6, 30),
                address="Tower C, Orchid Woods, Delhi NCR",
                skills="Logistics, Food Distribution, Fleet Coordination",
                preferred_activity="Relief & Food Drives",
                status="Active",
                joined_date=date.today() - timedelta(days=210)
            ),
            Volunteer(
                full_name="Meera Joshi",
                email="meera.joshi@example.com",
                phone="+91 97123 99881",
                date_of_birth=date(1997, 9, 14),
                address="7/A Heritage Heights, Ahmedabad",
                skills="English Tutoring, Soft Skills Training",
                preferred_activity="Education Support",
                status="Inactive",
                joined_date=date.today() - timedelta(days=320)
            )
        ]
        db.session.add_all(volunteers)

    # 4. Seed Students / Beneficiaries
    if not Student.query.first():
        students = [
            Student(
                student_name="Ananya Patil",
                dob=date(2013, 5, 14),
                age=13,
                gender="Female",
                guardian_name="Ramesh Patil (Daily wage earner)",
                guardian_phone="+91 98211 44556",
                school_grade="Class 8 - Municipal Vidya Mandir",
                assistance_type="Free Tuition & Books",
                status="Active",
                enrolled_date=date.today() - timedelta(days=250)
            ),
            Student(
                student_name="Kunal Waghmare",
                dob=date(2015, 9, 3),
                age=11,
                gender="Male",
                guardian_name="Sunita Waghmare (Domestic helper)",
                guardian_phone="+91 97660 12345",
                school_grade="Class 6 - Zilla Parishad Primary School",
                assistance_type="Nutrition & School Uniform",
                status="Active",
                enrolled_date=date.today() - timedelta(days=180)
            ),
            Student(
                student_name="Priyanka Kumari",
                dob=date(2011, 1, 20),
                age=15,
                gender="Female",
                guardian_name="Mohan Lal (Auto-rickshaw driver)",
                guardian_phone="+91 99345 67890",
                school_grade="Class 10 - St. Teresa Girls High School",
                assistance_type="Secondary Education Scholarship",
                status="Active",
                enrolled_date=date.today() - timedelta(days=400)
            ),
            Student(
                student_name="Aditya Shinde",
                dob=date(2016, 12, 10),
                age=9,
                gender="Male",
                guardian_name="Ganesh Shinde (Carpenter)",
                guardian_phone="+91 98812 33445",
                school_grade="Class 4 - Modern English School",
                assistance_type="Free Tuition",
                status="Active",
                enrolled_date=date.today() - timedelta(days=90)
            ),
            Student(
                student_name="Tanvi Pawar",
                dob=date(2014, 7, 8),
                age=12,
                gender="Female",
                guardian_name="Jyoti Pawar (Single mother)",
                guardian_phone="+91 98700 88991",
                school_grade="Class 7 - Vidya Vikas Mandir",
                assistance_type="School Supplies Kit",
                status="Active",
                enrolled_date=date.today() - timedelta(days=60)
            )
        ]
        db.session.add_all(students)

    # 5. Seed Donations
    if not Donation.query.first():
        ev1 = CampEvent.query.filter_by(title="Slum Youth Education & Book Drive").first()
        ev2 = CampEvent.query.filter_by(title="Free Community Eye & Dental Health Camp").first()
        
        donations = [
            Donation(
                donor_name="Dr. Vikram Sen",
                donor_email="dr.vikram.sen@gmail.com",
                donor_phone="+91 98110 55443",
                amount=15000.0,
                event_id=ev1.id if ev1 else None,
                cause_name="Slum Youth Education & Book Drive",
                payment_mode="NetBanking",
                transaction_ref="TXN_NB_99812401",
                receipt_number="YSF-2026-1001",
                donation_date=date.today() - timedelta(days=22)
            ),
            Donation(
                donor_name="Kavita Rao",
                donor_email="kavita.rao@outlook.com",
                donor_phone="+91 98450 77665",
                amount=5000.0,
                event_id=ev2.id if ev2 else None,
                cause_name="Free Community Eye & Dental Health Camp",
                payment_mode="UPI",
                transaction_ref="UPI_RAO_88321045",
                receipt_number="YSF-2026-1002",
                donation_date=date.today() - timedelta(days=14)
            ),
            Donation(
                donor_name="Rajesh Khanna & Associates",
                donor_email="info@khanna-associates.in",
                donor_phone="+91 98200 11998",
                amount=25000.0,
                event_id=None,
                cause_name="General Foundation Fund",
                payment_mode="Credit/Debit Card",
                transaction_ref="CARD_PAY_77301928",
                receipt_number="YSF-2026-1003",
                donation_date=date.today() - timedelta(days=10)
            ),
            Donation(
                donor_name="Anita Saxena",
                donor_email="anita.saxena@gmail.com",
                donor_phone="+91 97110 33445",
                amount=7500.0,
                event_id=ev1.id if ev1 else None,
                cause_name="Slum Youth Education & Book Drive",
                payment_mode="UPI",
                transaction_ref="UPI_SAX_44901237",
                receipt_number="YSF-2026-1004",
                donation_date=date.today() - timedelta(days=5)
            ),
            Donation(
                donor_name="Alok Singhania",
                donor_email="alok.singhania@yahoo.com",
                donor_phone="+91 98300 44556",
                amount=10000.0,
                event_id=None,
                cause_name="General Foundation Fund",
                payment_mode="Cash",
                transaction_ref="CASH_REC_0029",
                receipt_number="YSF-2026-1005",
                donation_date=date.today() - timedelta(days=2)
            )
        ]
        db.session.add_all(donations)

    # 6. Seed Contact Inquiries
    if not ContactMessage.query.first():
        messages = [
            ContactMessage(
                name="Deepak Trivedi",
                email="deepak.trivedi@corptech.com",
                phone="+91 98201 99223",
                subject="Corporate Social Responsibility (CSR) Partnership",
                message="Greetings from CorpTech. We are looking to sponsor educational kits for 500 children under our CSR mandate. Kindly share the partnership brochure.",
                status="In Review",
                created_at=datetime.utcnow() - timedelta(days=3)
            ),
            ContactMessage(
                name="Siddharth Menon",
                email="sid.menon@college.edu",
                phone="+91 97455 12098",
                subject="College Student Volunteer Group Enrollment",
                message="Our college NSS club has 30 students eager to assist in your upcoming Health and Eye Screening camp. How can we coordinate group logistics?",
                status="New",
                created_at=datetime.utcnow() - timedelta(days=1)
            ),
            ContactMessage(
                name="Leela Krishnan",
                email="leela.k@hotmail.com",
                phone="+91 98400 33221",
                subject="Donation Receipt Acknowledgement Query",
                message="I contributed online yesterday for the book drive. Could you confirm if tax exemption receipt was generated? Thank you for your noble work.",
                status="Resolved",
                created_at=datetime.utcnow() - timedelta(days=6)
            )
        ]
        db.session.add_all(messages)

    db.session.commit()
    print("Database successfully seeded!")
