import mysql.connector
from mysql.connector import Error
import hashlib
import logging

logging.basicConfig(filename='as_lms_model.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',         
    'password': 'YOUR-PASSWORD', 
    'database': 'as_lms_db'
}

class DatabaseModel:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**DB_CONFIG)
            return True
        except Error as e:
            logging.error(f"Connection Error: {e}")
            print(f"DB Error: {e}")
            return False

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, username, password):
        if not self.connect(): return None
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
        pwd_hash = self._hash_password(password)
        cursor.execute(query, (username, pwd_hash))
        user = cursor.fetchone()
        cursor.close()
        return user

    def create_user(self, username, password, full_name, role):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            pwd_hash = self._hash_password(password)
            cursor.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (%s, %s, %s, %s)", (username, pwd_hash, full_name, role))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def update_user(self, user_id, full_name, role, username):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE users SET full_name = %s, role = %s, username = %s WHERE id = %s", (full_name, role, username, user_id))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def delete_user(self, user_id):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def get_all_users(self, search_query=""):
        if not self.connect(): return []
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT id, username, full_name, role FROM users"
        params = []
        if search_query:
            query += " WHERE full_name LIKE %s OR username LIKE %s OR role LIKE %s"
            term = f"%{search_query}%"
            params = [term, term, term]
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        return cursor.fetchall()

    def update_user_advisors(self, student_id, teacher_ids):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM advisors WHERE student_id = %s", (student_id,))
            for tid in teacher_ids:
                cursor.execute("INSERT INTO advisors (student_id, teacher_id) VALUES (%s, %s)", (student_id, tid))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def get_user_advisors(self, student_id):
        if not self.connect(): return []
        cursor = self.connection.cursor()
        cursor.execute("SELECT teacher_id FROM advisors WHERE student_id = %s", (student_id,))
        return [row[0] for row in cursor.fetchall()]

    def create_course(self, title, description, teacher_id):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO courses (title, description, teacher_id) VALUES (%s, %s, %s)", (title, description, teacher_id))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def delete_course(self, course_id):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def get_all_courses(self, search_query=""):
        if not self.connect(): return []
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT c.id, c.title, u.full_name as teacher_name FROM courses c LEFT JOIN users u ON c.teacher_id = u.id"
        params = []
        if search_query:
            query += " WHERE c.title LIKE %s OR u.full_name LIKE %s"
            term = f"%{search_query}%"
            params = [term, term]
        cursor.execute(query, params)
        return cursor.fetchall()

    def get_teacher_courses(self, teacher_id):
        if not self.connect(): return []
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM courses WHERE teacher_id = %s", (teacher_id,))
        return cursor.fetchall()

    def enroll_student(self, student_id, course_id):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT IGNORE INTO enrollments (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def unenroll_student(self, student_id, course_id):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM enrollments WHERE student_id = %s AND course_id = %s", (student_id, course_id))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def get_course_students(self, course_id, teacher_id=None):
        if not self.connect(): return []
        cursor = self.connection.cursor(dictionary=True)
        query = """
            SELECT DISTINCT u.id, u.full_name 
            FROM users u 
            JOIN enrollments e ON u.id = e.student_id
        """
        params = [course_id]
        
        if teacher_id:
            query += " JOIN advisors a ON u.id = a.student_id WHERE e.course_id = %s AND a.teacher_id = %s"
            params = [course_id, teacher_id]
        else:
            query += " WHERE e.course_id = %s AND u.role = 'student'"
            
        cursor.execute(query, params)
        return cursor.fetchall()

    def create_assignment(self, course_id, title, description, max_score, deadline, attachment_path=None):
        if not self.connect(): return None
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO assignments (course_id, title, description, max_score, deadline, attachment_path) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (course_id, title, description, max_score, deadline, attachment_path))
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            return None
        finally:
            cursor.close()
            
    def distribute_assignment(self, assignment_id, student_ids):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            for sid in student_ids:
                cursor.execute("INSERT INTO assignment_distribution (assignment_id, student_id) VALUES (%s, %s)", (assignment_id, sid))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()
            
    def delete_assignment(self, assignment_id):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM assignments WHERE id = %s", (assignment_id,))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def get_course_assignments(self, course_id, search=""):
        if not self.connect(): return []
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM assignments WHERE course_id = %s"
        params = [course_id]
        if search:
            query += " AND title LIKE %s"
            params.append(f"%{search}%")
        query += " ORDER BY created_at DESC"
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def get_assignment_details(self, assignment_id):
        if not self.connect(): return None
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM assignments WHERE id = %s", (assignment_id,))
        return cursor.fetchone()

    def submit_assignment(self, student_id, assignment_id, content_text, file_path):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO submissions (student_id, assignment_id, content_text, file_path) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE content_text = %s, file_path = %s, submitted_at = CURRENT_TIMESTAMP", (student_id, assignment_id, content_text, file_path, content_text, file_path))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def get_student_submission(self, student_id, assignment_id):
        if not self.connect(): return None
        cursor = self.connection.cursor(dictionary=True)
        query = """
            SELECT s.*, g.score, g.feedback 
            FROM submissions s 
            LEFT JOIN grades g ON s.assignment_id = g.assignment_id AND s.student_id = g.student_id 
            WHERE s.student_id = %s AND s.assignment_id = %s
        """
        cursor.execute(query, (student_id, assignment_id))
        return cursor.fetchone()

    def get_assignment_submissions(self, assignment_id, search=""):
        if not self.connect(): return []
        cursor = self.connection.cursor(dictionary=True)
        # Only students in assignment_distribution
        query = """
            SELECT u.id, u.full_name, s.content_text, s.file_path, s.submitted_at, g.score, g.feedback
            FROM users u
            JOIN enrollments e ON u.id = e.student_id
            JOIN assignments a ON e.course_id = a.course_id
            JOIN assignment_distribution ad ON a.id = ad.assignment_id AND u.id = ad.student_id
            LEFT JOIN submissions s ON u.id = s.student_id AND a.id = s.assignment_id
            LEFT JOIN grades g ON u.id = g.student_id AND a.id = g.assignment_id
            WHERE a.id = %s
        """
        params = [assignment_id]
        if search:
            query += " AND u.full_name LIKE %s"
            params.append(f"%{search}%")
        cursor.execute(query, params)
        return cursor.fetchall()

    def save_grade_and_feedback(self, student_id, assignment_id, score, feedback):
        if not self.connect(): return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO grades (student_id, assignment_id, score, feedback) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE score = %s, feedback = %s, graded_at = CURRENT_TIMESTAMP", (student_id, assignment_id, score, feedback, score, feedback))
            self.connection.commit()
            return True
        except Error as e:
            return False
        finally:
            cursor.close()

    def get_student_grades(self, student_id, search=""):
        if not self.connect(): return []
        cursor = self.connection.cursor()
        # FIX: Added JOIN with assignment_distribution to ensure only assigned tasks appear
        query = """
            SELECT c.title, a.id, a.title, a.max_score, g.score, a.deadline 
            FROM enrollments e 
            JOIN courses c ON e.course_id = c.id 
            JOIN assignments a ON c.id = a.course_id
            JOIN assignment_distribution ad ON a.id = ad.assignment_id AND e.student_id = ad.student_id
            LEFT JOIN grades g ON a.id = g.assignment_id AND g.student_id = %s 
            WHERE e.student_id = %s
        """
        params = [student_id, student_id]
        if search:
            query += " AND (a.title LIKE %s OR c.title LIKE %s)"
            term = f"%{search}%"
            params.extend([term, term])
        cursor.execute(query, params)
        return cursor.fetchall()
