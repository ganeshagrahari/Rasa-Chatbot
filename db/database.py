import sqlite3
import os
import json
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'scholarship_bot.db')

def create_tables():
    """Create necessary tables for the scholarship bot."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone TEXT,
        education_level TEXT,
        income_level TEXT,
        category TEXT,
        state TEXT,
        field TEXT,
        score TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create scholarships table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scholarships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        eligibility TEXT,
        documents TEXT,
        deadline TEXT,
        categories TEXT,
        education_levels TEXT,
        max_income INTEGER,
        min_score INTEGER,
        description TEXT,
        website_url TEXT
    )
    ''')
    
    # Create reminders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        scholarship_id INTEGER,
        reminder_date TEXT,
        sent BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (scholarship_id) REFERENCES scholarships (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def add_sample_scholarships():
    """Add sample scholarship data to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    sample_scholarships = [
        {
            "name": "National Scholarship Portal",
            "eligibility": "All students with family income below 6 lakhs",
            "documents": ["Income certificate", "Caste certificate", "Mark sheets", "Aadhaar card"],
            "deadline": "October 31, 2025",
            "categories": ["SC", "ST", "OBC", "General"],
            "education_levels": ["10th", "12th", "undergraduate", "graduate"],
            "max_income": 600000,
            "min_score": 0,
            "description": "The National Scholarship Portal is a one-stop solution for students to access information about various scholarships provided by the Government of India.",
            "website_url": "https://scholarships.gov.in/"
        },
        {
            "name": "INSPIRE Scholarship",
            "eligibility": "Top 1% in 12th standard or qualified in competitive exams",
            "documents": ["Mark sheets", "Competitive exam result", "Bank account details"],
            "deadline": "December 15, 2025",
            "categories": ["General", "OBC", "SC", "ST"],
            "education_levels": ["undergraduate"],
            "max_income": 0,
            "min_score": 90,
            "description": "Innovation in Science Pursuit for Inspired Research (INSPIRE) is a program implemented by the Department of Science & Technology to strengthen the research base.",
            "website_url": "https://www.online-inspire.gov.in/"
        },
        {
            "name": "Post-Matric Scholarship",
            "eligibility": "Students belonging to SC/ST/OBC with family income below 2.5 lakhs",
            "documents": ["Income certificate", "Caste certificate", "Mark sheets", "Institution verification"],
            "deadline": "September 30, 2025",
            "categories": ["SC", "ST", "OBC"],
            "education_levels": ["12th", "undergraduate", "graduate"],
            "max_income": 250000,
            "min_score": 0,
            "description": "Post-Matric Scholarships are provided to students belonging to scheduled castes and tribes pursuing post-matriculation courses.",
            "website_url": "https://scholarships.gov.in/"
        }
    ]
    
    for scholarship in sample_scholarships:
        cursor.execute('''
        INSERT OR REPLACE INTO scholarships 
        (name, eligibility, documents, deadline, categories, education_levels, max_income, min_score, description, website_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            scholarship["name"],
            scholarship["eligibility"],
            json.dumps(scholarship["documents"]),
            scholarship["deadline"],
            json.dumps(scholarship["categories"]),
            json.dumps(scholarship["education_levels"]),
            scholarship["max_income"],
            scholarship["min_score"],
            scholarship["description"],
            scholarship["website_url"]
        ))
    
    conn.commit()
    conn.close()

def save_user_profile(user_id, profile_data):
    """Save or update user profile information."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT OR REPLACE INTO users 
    (user_id, education_level, income_level, category, state, field, score)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        profile_data.get("education_level", ""),
        profile_data.get("income_level", ""),
        profile_data.get("category", ""),
        profile_data.get("state", ""),
        profile_data.get("field", ""),
        profile_data.get("score", "")
    ))
    
    conn.commit()
    conn.close()

def set_reminder(user_id, scholarship_name, days_before=7):
    """Set a reminder for a scholarship deadline."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Find the scholarship
    cursor.execute("SELECT id, deadline FROM scholarships WHERE name LIKE ?", ('%' + scholarship_name + '%',))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return False
    
    scholarship_id, deadline_str = result
    
    # Parse the deadline and calculate reminder date
    try:
        deadline = datetime.strptime(deadline_str, "%B %d, %Y")
        reminder_date = deadline - timedelta(days=days_before)
        reminder_date_str = reminder_date.strftime("%Y-%m-%d")
        
        # Save the reminder
        cursor.execute('''
        INSERT INTO reminders (user_id, scholarship_id, reminder_date)
        VALUES (?, ?, ?)
        ''', (user_id, scholarship_id, reminder_date_str))
        
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def initialize_database():
    """Initialize database with tables and sample data."""
    create_tables()
    add_sample_scholarships()

# Run this when the module is imported
if not os.path.exists(DB_PATH):
    initialize_database()