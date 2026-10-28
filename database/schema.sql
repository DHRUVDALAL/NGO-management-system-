-- ====================================================================
-- Database Schema for YuvaShakti Foundation: NGO Management System
-- Database: ngo_management
-- ====================================================================

CREATE DATABASE IF NOT EXISTS ngo_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ngo_management;

-- 1. Administrators Table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    role VARCHAR(50) DEFAULT 'Administrator',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Volunteers Table
CREATE TABLE IF NOT EXISTS volunteers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    date_of_birth DATE NULL,
    address VARCHAR(255) NULL,
    skills TEXT NULL,
    preferred_activity VARCHAR(120) NOT NULL,
    status VARCHAR(30) DEFAULT 'Active', -- 'Active', 'Pending', 'Inactive'
    joined_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Students / Beneficiaries Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(120) NOT NULL,
    dob DATE NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    guardian_name VARCHAR(120) NOT NULL,
    guardian_phone VARCHAR(30) NOT NULL,
    school_grade VARCHAR(80) NOT NULL,
    assistance_type VARCHAR(120) NOT NULL, -- 'Free Tuition', 'Scholarship', 'Nutrition Program', 'School Supplies Kit'
    status VARCHAR(30) DEFAULT 'Active',   -- 'Active', 'Graduated', 'Suspended'
    enrolled_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Camps & Events Table
CREATE TABLE IF NOT EXISTS camps_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    event_type VARCHAR(80) NOT NULL, -- 'Health Camp', 'Blood Donation', 'Education Drive', 'Food Distribution'
    description TEXT NOT NULL,
    venue VARCHAR(200) NOT NULL,
    event_date DATE NOT NULL,
    target_budget DECIMAL(12, 2) DEFAULT 0.00,
    raised_budget DECIMAL(12, 2) DEFAULT 0.00,
    volunteer_capacity INT DEFAULT 30,
    status VARCHAR(30) DEFAULT 'Upcoming', -- 'Upcoming', 'Ongoing', 'Completed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Donations Table
CREATE TABLE IF NOT EXISTS donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donor_name VARCHAR(120) NOT NULL,
    donor_email VARCHAR(120) NOT NULL,
    donor_phone VARCHAR(30) NULL,
    amount DECIMAL(12, 2) NOT NULL,
    event_id INT NULL,
    cause_name VARCHAR(150) DEFAULT 'General Foundation Fund',
    payment_mode VARCHAR(50) NOT NULL, -- 'UPI', 'NetBanking', 'Credit/Debit Card', 'Cash'
    transaction_ref VARCHAR(100) NULL,
    receipt_number VARCHAR(50) NOT NULL UNIQUE,
    donation_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES camps_events(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Contact Messages Table
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(30) NULL,
    subject VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'New', -- 'New', 'In Review', 'Resolved'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
