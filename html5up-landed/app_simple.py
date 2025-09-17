#!/usr/bin/env python3
"""
Simple Python HTTP server for the Alumni Platform
This version uses only built-in Python modules (no external dependencies)
"""

import http.server
import socketserver
import json
import sqlite3
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# Configuration
PORT = 3000
SQLITE_DB = 'alumni_platform.db'

# Initialize SQLite database
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

# Custom HTTP request handler
class AlumniPlatformHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_POST(self):
        """Handle POST requests for API endpoints"""
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_error(404, "Not Found")
    
    def handle_api_request(self):
        """Handle API requests"""
        try:
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/api/signup/student':
                response = self.handle_student_signup(data)
            elif self.path == '/api/signup/alumni':
                response = self.handle_alumni_signup(data)
            elif self.path == '/api/login':
                response = self.handle_login(data)
            else:
                response = {'error': 'Unknown API endpoint'}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ API request error: {e}")
            self.send_error(500, "Internal Server Error")
    
    def handle_student_signup(self, data):
        """Handle student signup"""
        try:
            # Validate required fields
            required_fields = ['fullName', 'rollNo', 'collegeName', 'department', 'address', 'emailOrMobile', 'password']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'Missing required field: {field}'}
            
            # Save to SQLite
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
            student_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Student registered: {data['fullName']} (ID: {student_id})")
            return {
                'success': True,
                'message': 'Student registered successfully',
                'studentId': student_id
            }
            
        except Exception as e:
            print(f"❌ Student signup error: {e}")
            return {'error': 'Internal server error'}
    
    def handle_alumni_signup(self, data):
        """Handle alumni signup"""
        try:
            # Validate required fields
            required_fields = ['fullName', 'rollNo', 'collegeName', 'currentlyWorkingAs', 'address', 'emailOrMobile', 'password']
            for field in required_fields:
                if field not in data or not data[field]:
                    return {'error': f'Missing required field: {field}'}
            
            # Save to SQLite
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
            alumni_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            print(f"✅ Alumni registered: {data['fullName']} (ID: {alumni_id})")
            return {
                'success': True,
                'message': 'Alumni registered successfully',
                'alumniId': alumni_id
            }
            
        except Exception as e:
            print(f"❌ Alumni signup error: {e}")
            return {'error': 'Internal server error'}
    
    def handle_login(self, data):
        """Handle user login"""
        try:
            if 'emailOrMobile' not in data or 'password' not in data:
                return {'error': 'Email/Mobile and password are required'}
            
            email_or_mobile = data['emailOrMobile']
            password = data['password']
            
            # Search in both students and alumni tables
            conn = sqlite3.connect(SQLITE_DB)
            cursor = conn.cursor()
            
            # Check students table
            cursor.execute('''
                SELECT id, full_name, roll_no, college_name, department, address, email_or_mobile
                FROM students WHERE email_or_mobile = ? AND password = ?
            ''', (email_or_mobile, password))
            student_result = cursor.fetchone()
            
            if student_result:
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
                conn.close()
                print(f"✅ Student login successful: {user['fullName']}")
                return {'success': True, 'message': 'Login successful', 'user': user}
            
            # Check alumni table
            cursor.execute('''
                SELECT id, full_name, roll_no, college_name, currently_working_as, address, email_or_mobile
                FROM alumni WHERE email_or_mobile = ? AND password = ?
            ''', (email_or_mobile, password))
            alumni_result = cursor.fetchone()
            
            if alumni_result:
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
                print(f"✅ Alumni login successful: {user['fullName']}")
                return {'success': True, 'message': 'Login successful', 'user': user}
            
            conn.close()
            print(f"❌ Login failed: Invalid credentials")
            return {'error': 'Invalid email/mobile or password'}
            
        except Exception as e:
            print(f"❌ Login error: {e}")
            return {'error': 'Internal server error'}
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    # Initialize database
    init_sqlite()
    
    # Start server
    with socketserver.TCPServer(("", PORT), AlumniPlatformHandler) as httpd:
        print(f"🚀 Starting Python HTTP server on port {PORT}")
        print(f"📊 SQLite DB: {SQLITE_DB}")
        print(f"🌐 Server running at: http://localhost:{PORT}/")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
