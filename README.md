# YuvaShakti Foundation: NGO Management System
### With Real-Time Activity & Impact Dashboard

A modern, responsive, and data-driven web application developed for the **YuvaShakti Foundation** to streamline volunteer onboarding, track donor contributions, manage student beneficiaries, organize community welfare camps, and provide administrators with actionable organizational intelligence.

Built strictly according to project specifications using **HTML5, CSS3, Vanilla JavaScript, Python Flask, and Relational Database (MySQL / SQLite dual-mode)**.

---

## 🌟 Key System Capabilities

1. **Public Information Portal**:
   - **Home**: Dynamic landing page featuring mission highlights, live database impact counters, and active camp cards.
   - **About Us**: Comprehensive overview of foundation history, core principles, mission, vision, and 3-tier operational lifecycle.
   - **Programs Showcase**: Deep dive into Gyan Setu (Tutoring), Arogya Sparsh (Mobile Health/Eye Camps), Yuva Disha (Youth Skills), and Poshak Aahar (Nutrition & Relief).
   - **Camps & Events Directory**: Calendar of scheduled social drives with real-time target vs. raised budget progress meters and volunteer sign-ups.

2. **Action & Registration Modules**:
   - **Volunteer Registration**: Captures demographic info, contact numbers, date of birth, skills, and preferred social activity with immediate database logging.
   - **Donation Gateway & 80G Tax Exemption Receipts**: Supports contribution amount presets (₹1,000, ₹2,500, ₹5,000, custom), cause/camp selection, multi-mode payment options (UPI/QR, Net Banking, Card, Cash), and produces an instant printable 80G tax receipt with a unique serial number (`YSF-2026-XXXX`).
   - **Student / Beneficiary Welfare Enrollment**: Dedicated form capturing student full name, date of birth, calculated age, gender, parent/guardian phone, school & grade, and assistance type (free tuition, scholarship, uniform/kit).
   - **Contact & Inquiries Desk**: Public inquiries and partnership proposals saved directly with timestamps for administrative follow-up.

3. **Executive Admin Control Center**:
   - **Secure Authentication**: Password hashing using `werkzeug.security` with session guards.
   - **Activity & Impact Dashboard**: Live metrics for Total Volunteers, Active Field Force, Total Funds Mobilized (₹), Unique Donors, Enrolled Students, and Scheduled Camps.
   - **Data Visualizations**: Integrated [Chart.js](https://www.chartjs.org/) charts showing volunteer distribution by preferred activity (Doughnut) and donation inflows by cause (Bar chart).
   - **Management Tables & Audit Trails**:
     - Volunteers directory with live search and 1-click status toggling (`Active` / `Inactive`).
     - Donations audit log with link to inspect/re-print any donor's official 80G receipt.
     - Student beneficiary registry with age, DOB, schooling level, and status updates.
     - Camps and drives manager with a modal to schedule new welfare drives and monitor collection progress.
     - Public inquiries inbox with resolution status tracking.
   - **CSV / Audit Exporter**: One-click download of audit-ready CSV spreadsheets for board meetings or compliance reporting.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- (Optional) MySQL Server 8.0+ if you wish to connect to a live MySQL instance. The system runs seamlessly on SQLite by default with zero configuration required.

### 2. Environment Setup
```bash
# Navigate to the project directory
cd /Users/dhruv/Desktop/Projects/satya_project

# Activate the virtual environment
source venv/bin/activate

# Install required dependencies (if not already installed)
pip install -r requirements.txt
```

### 3. Running the Server
```bash
python app.py
```
Open your browser and visit: **`http://127.0.0.1:5050`** (or `http://127.0.0.1:5001` depending on configured port).

---

## 🔑 Administrative Credentials (Default)

| Role | Username | Password | Access URL |
| :--- | :--- | :--- | :--- |
| **Super Administrator** | `admin` | `admin123` | `http://127.0.0.1:5050/admin/login` |

---

## 🗄️ Database Architecture & Switching to MySQL

The system uses a flexible, dual-mode database adapter in `config.py`.

### Default Mode: SQLite
On initial run, a self-contained database `database/ngo_management.db` is initialized and pre-seeded with realistic records for demonstration and viva testing.

### Switching to MySQL:
To connect to a live MySQL database named `ngo_management`:
1. Ensure your local MySQL server is running:
   ```bash
   mysql -u root -p < database/schema.sql
   ```
2. Set the environment variable:
   ```bash
   export USE_MYSQL=true
   export MYSQL_HOST=localhost
   export MYSQL_USER=root
   export MYSQL_PASSWORD=your_password
   export MYSQL_DB=ngo_management
   python app.py
   ```

---

## 🧪 Automated Testing

A full regression test suite is included in `tests/test_flow.py`:
```bash
python -m unittest tests/test_flow.py
```
All 6 core functional workflows are verified automatically.

---

## 📁 Repository Structure

```text
satya_project/
├── app.py                      # Core Flask application and routing logic
├── config.py                   # Environment-driven database & session configuration
├── requirements.txt            # Python dependencies
├── database/
│   ├── db.py                   # SQLAlchemy instance setup
│   ├── models.py               # ORM definitions (Admin, Volunteer, Student, Camp, Donation, Message)
│   ├── schema.sql              # MySQL DDL script
│   └── seed_data.py            # Initial seed data for demo accounts and records
├── static/
│   ├── css/
│   │   ├── main.css            # Core design system tokens, typography, navbar, footer
│   │   ├── portal.css          # Public hero, about, programs, and camp cards
│   │   ├── forms.css           # Modern inputs, donation chips, and printable receipts
│   │   └── admin.css           # Admin KPI cards, data tables, and modal styles
│   └── js/
│       ├── main.js             # Mobile drawer and alert dismissals
│       ├── forms.js            # Preset selectors and input validation
│       └── dashboard.js        # Live table search, status toggles, and Chart.js integration
├── templates/
│   ├── base.html               # Public layout template
│   ├── index.html              # Home landing page with live counters
│   ├── about.html              # Foundation background, mission, and vision
│   ├── programs.html           # Social initiatives overview
│   ├── events.html             # Camps and community drives
│   ├── volunteer_register.html # Volunteer application form
│   ├── donate.html             # Donation portal with cause selection
│   ├── receipt.html            # Printable 80G tax donation receipt
│   ├── student_register.html   # Student beneficiary enrollment form
│   ├── contact.html            # Public inquiry form
│   └── admin/
│       ├── base_admin.html     # Admin layout with tabbed navigation
│       ├── login.html          # Secure admin sign-in
│       ├── dashboard.html      # KPI analytics & visualization center
│       ├── volunteers.html     # Volunteer directory & status editor
│       ├── students.html       # Student beneficiary management
│       ├── donations.html      # Donation log & receipt inspection
│       ├── events.html         # Camps and welfare drives scheduler
│       └── messages.html       # Public inquiries inbox
└── tests/
    └── test_flow.py            # Unit and integration test suite
```
