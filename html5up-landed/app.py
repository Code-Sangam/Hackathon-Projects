from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymongo
import sqlite3
import os
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Database configurations
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/alumni_platform')
SQLITE_DB = 'alumni_platform.db'

# MongoDB connection
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client.alumni_platform
    students_collection = db.students
    alumni_collection = db.alumni
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    db = None
    students_collection = None
    alumni_collection = None

# SQLite connection and setup
def init_sqlite():
    try:
        conn = sqlite3.connect(SQLITE_DB)
        cursor = conn.cursor()
        
        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                roll_no TEXT NOT NULL,
                college_name TEXT NOT NULL,
                department TEXT NOT NULL,
                address TEXT NOT NULL,
                email_or_mobile TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create alumni table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alumni (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                roll_no TEXT NOT NULL,
                college_name TEXT NOT NULL,
                currently_working_as TEXT NOT NULL,
                address TEXT NOT NULL,
                email_or_mobile TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ SQLite database initialized successfully")
    except Exception as e:
        print(f"❌ SQLite initialization failed: {e}")

# Initialize SQLite on startup
init_sqlite()

# Serve static files
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# API Routes

# Student Signup
@app.route('/api/signup/student', methods=['POST'])
def signup_student():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['fullName', 'rollNo', 'collegeName', 'department', 'address', 'emailOrMobile', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare student data
        student_data = {
            'fullName': data['fullName'],
            'rollNo': data['rollNo'],
            'collegeName': data['collegeName'],
            'department': data['department'],
            'address': data['address'],
            'emailOrMobile': data['emailOrMobile'],
            'password': data['password'],  # Note: In production, hash this password
            'userType': 'student',
            'createdAt': datetime.now()
        }
        
        # Save to MongoDB
        mongo_result = None
        if students_collection:
            try:
                mongo_result = students_collection.insert_one(student_data)
                print(f"✅ Student saved to MongoDB: {mongo_result.inserted_id}")
            except Exception as e:
                print(f"❌ MongoDB save failed: {e}")
        
        # Save to SQLite
        sqlite_result = None
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO students (full_name, roll_no, college_name, department, address, email_or_mobile, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['fullName'],
                data['rollNo'],
                data['collegeName'],
                data['department'],
                data['address'],
                data['emailOrMobile'],
                data['password']
            ))
            sqlite_result = cursor.lastrowid
            conn.commit()
            conn.close()
            print(f"✅ Student saved to SQLite: ID {sqlite_result}")
        except Exception as e:
            print(f"❌ SQLite save failed: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Student registered successfully',
            'mongoId': str(mongo_result.inserted_id) if mongo_result else None,
            'sqliteId': sqlite_result
        })
        
    except Exception as e:
        print(f"❌ Student signup error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Alumni Signup
@app.route('/api/signup/alumni', methods=['POST'])
def signup_alumni():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['fullName', 'rollNo', 'collegeName', 'currentlyWorkingAs', 'address', 'emailOrMobile', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare alumni data
        alumni_data = {
            'fullName': data['fullName'],
            'rollNo': data['rollNo'],
            'collegeName': data['collegeName'],
            'currentlyWorkingAs': data['currentlyWorkingAs'],
            'address': data['address'],
            'emailOrMobile': data['emailOrMobile'],
            'password': data['password'],  # Note: In production, hash this password
            'userType': 'alumni',
            'createdAt': datetime.now()
        }
        
        # Save to MongoDB
        mongo_result = None
        if alumni_collection:
            try:
                mongo_result = alumni_collection.insert_one(alumni_data)
                print(f"✅ Alumni saved to MongoDB: {mongo_result.inserted_id}")
            except Exception as e:
                print(f"❌ MongoDB save failed: {e}")
        
        # Save to SQLite
        sqlite_result = None
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO alumni (full_name, roll_no, college_name, currently_working_as, address, email_or_mobile, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['fullName'],
                data['rollNo'],
                data['collegeName'],
                data['currentlyWorkingAs'],
                data['address'],
                data['emailOrMobile'],
                data['password']
            ))
            sqlite_result = cursor.lastrowid
            conn.commit()
            conn.close()
            print(f"✅ Alumni saved to SQLite: ID {sqlite_result}")
        except Exception as e:
            print(f"❌ SQLite save failed: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Alumni registered successfully',
            'mongoId': str(mongo_result.inserted_id) if mongo_result else None,
            'sqliteId': sqlite_result
        })
        
    except Exception as e:
        print(f"❌ Alumni signup error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Login
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'emailOrMobile' not in data or 'password' not in data:
            return jsonify({'error': 'Email/Mobile and password are required'}), 400
        
        email_or_mobile = data['emailOrMobile']
        password = data['password']
        
        # Search in both students and alumni tables (SQLite)
        user = None
        user_type = None
        
        try:
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            
            # Check students table
            cursor.execute('''
                SELECT id, full_name, roll_no, college_name, department, address, email_or_mobile
                FROM students WHERE email_or_mobile = ? AND password = ?
            ''', (email_or_mobile, password))
            student_result = cursor.fetchone()
            
            if student_result:
                user_type = 'student'
                user = {
                    'id': student_result[0],
                    'fullName': student_result[1],
                    'rollNo': student_result[2],
                    'collegeName': student_result[3],
                    'department': student_result[4],
                    'address': student_result[5],
                    'emailOrMobile': student_result[6],
                    'userType': 'student'
                }
            else:
                # Check alumni table
                cursor.execute('''
                    SELECT id, full_name, roll_no, college_name, currently_working_as, address, email_or_mobile
                    FROM alumni WHERE email_or_mobile = ? AND password = ?
                ''', (email_or_mobile, password))
                alumni_result = cursor.fetchone()
                
                if alumni_result:
                    user_type = 'alumni'
                    user = {
                        'id': alumni_result[0],
                        'fullName': alumni_result[1],
                        'rollNo': alumni_result[2],
                        'collegeName': alumni_result[3],
                        'currentlyWorkingAs': alumni_result[4],
                        'address': alumni_result[5],
                        'emailOrMobile': alumni_result[6],
                        'userType': 'alumni'
                    }
            
            conn.close()
            
        except Exception as e:
            print(f"❌ SQLite login query failed: {e}")
            return jsonify({'error': 'Database error'}), 500
        
        if user:
            print(f"✅ Login successful: {user_type} - {user['fullName']}")
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user
            })
        else:
            print(f"❌ Login failed: Invalid credentials")
            return jsonify({'error': 'Invalid email/mobile or password'}), 401
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'mongodb': 'connected' if db else 'disconnected',
        'sqlite': 'connected',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    print(f"🚀 Starting Flask server on port {port}")
    print(f"📊 MongoDB URI: {MONGO_URI}")
    print(f"🗄️ SQLite DB: {SQLITE_DB}")
    app.run(host='0.0.0.0', port=port, debug=True)
