import unittest
from datetime import date
from app import create_app
from database.db import db
from database.models import Admin, Volunteer, Student, CampEvent, Donation, ContactMessage

class YuvaShaktiPlatformTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    def test_01_public_pages_load(self):
        """Verify that all public pages return HTTP 200"""
        for route in ['/', '/about', '/programs', '/events', '/volunteer-register', '/donate', '/student-register', '/contact']:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with status {response.status_code}")
            self.assertIn(b'YuvaShakti', response.data)

    def test_02_volunteer_registration(self):
        """Test submitting the volunteer registration form"""
        payload = {
            'full_name': 'Aanya Sengupta',
            'email': 'aanya.sen@example.com',
            'phone': '+91 98301 23456',
            'date_of_birth': '2000-03-25',
            'address': 'Flat 301, Lake City, Kolkata',
            'skills': 'Child counseling, Public speaking, High-school science',
            'preferred_activity': 'Education Support'
        }
        response = self.client.post('/volunteer-register', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'registration has been successfully recorded', response.data)

        with self.app.app_context():
            vol = Volunteer.query.filter_by(email='aanya.sen@example.com').first()
            self.assertIsNotNone(vol)
            self.assertEqual(vol.full_name, 'Aanya Sengupta')
            self.assertEqual(vol.status, 'Active')

    def test_03_donation_and_receipt(self):
        """Test donation form submission and automatic 80G receipt generation"""
        payload = {
            'donor_name': 'Rakesh Jhunjhunwala Trust',
            'donor_email': 'trust@example.org',
            'donor_phone': '+91 98200 99887',
            'amount': '15000',
            'payment_mode': 'UPI',
            'transaction_ref': 'UPI_TEST_991823'
        }
        response = self.client.post('/donate', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Official Receipt', response.data)
        self.assertIn(b'80G CERTIFIED', response.data)
        self.assertIn(b'Rakesh Jhunjhunwala Trust', response.data)

    def test_04_student_enrollment(self):
        """Test student beneficiary registration with DOB, age, and assistance type"""
        payload = {
            'student_name': 'Siddharth Waghmare',
            'dob': '2015-08-14',
            'age': '11',
            'gender': 'Male',
            'guardian_name': 'Sunita Waghmare',
            'guardian_phone': '+91 98210 33221',
            'school_grade': 'Class 6 - Municipal School No. 4',
            'assistance_type': 'Free Tuition & Books'
        }
        response = self.client.post('/student-register', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'successfully enrolled', response.data)

        with self.app.app_context():
            stu = Student.query.filter_by(student_name='Siddharth Waghmare').first()
            self.assertIsNotNone(stu)
            self.assertEqual(stu.age, 11)

    def test_05_contact_inquiry(self):
        """Test contact inquiry form submission"""
        payload = {
            'name': 'Gaurav Singhal',
            'email': 'gaurav.singhal@company.com',
            'phone': '+91 98100 11223',
            'subject': 'Volunteer Team Building Drive',
            'message': 'We want our tech engineering team of 20 people to volunteer at your upcoming eye camp.'
        }
        response = self.client.post('/contact', data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your inquiry has been logged in our system', response.data)

    def test_06_admin_auth_and_dashboard(self):
        """Test secure admin login and dashboard analytics view"""
        # Unauthenticated access should redirect to login
        res = self.client.get('/admin/dashboard')
        self.assertEqual(res.status_code, 302)

        # Login with correct credentials
        login_res = self.client.post('/admin/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn(b'Activity &amp; Impact Dashboard', login_res.data)
        self.assertIn(b'Total Volunteers', login_res.data)
        self.assertIn(b'Total Funds Mobilized', login_res.data)

        # Access volunteers management table
        vol_res = self.client.get('/admin/volunteers')
        self.assertEqual(vol_res.status_code, 200)
        self.assertIn(b'Volunteers Directory', vol_res.data)

        # Access students management table
        stu_res = self.client.get('/admin/students')
        self.assertEqual(stu_res.status_code, 200)
        self.assertIn(b'Student &amp; Child Beneficiaries Registry', stu_res.data)

        # Access donations audit trail
        don_res = self.client.get('/admin/donations')
        self.assertEqual(don_res.status_code, 200)
        self.assertIn(b'Donation Management &amp; Audit Trail', don_res.data)

        # Access events / camps manager
        ev_res = self.client.get('/admin/events')
        self.assertEqual(ev_res.status_code, 200)
        self.assertIn(b'Camps, Drives &amp; Welfare Events Manager', ev_res.data)

        # Access inquiries messages
        msg_res = self.client.get('/admin/messages')
        self.assertEqual(msg_res.status_code, 200)
        self.assertIn(b'Public Inquiries &amp; Community Messages', msg_res.data)

if __name__ == '__main__':
    unittest.main()
