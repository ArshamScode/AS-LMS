from model import DatabaseModel
import tkinter.messagebox as messagebox

class LMSController:
    def __init__(self):
        self.model = DatabaseModel()
        self.current_user = None

    def login(self, username, password):
        user = self.model.authenticate_user(username, password)
        if user:
            self.current_user = user
            return True
        return False

    def logout(self):
        self.current_user = None

    def get_all_users_data(self, search=""):
        return self.model.get_all_users(search)

    def add_user(self, data):
        return self.model.create_user(*data)

    def update_user(self, uid, name, role, username):
        return self.model.update_user(uid, name, role, username)

    def delete_user(self, uid):
        return self.model.delete_user(uid)

    def update_advisors(self, student_id, teacher_ids):
        return self.model.update_user_advisors(student_id, teacher_ids)
    
    def get_user_advisors(self, student_id):
        return self.model.get_user_advisors(student_id)

    def get_all_courses_data(self, search=""):
        return self.model.get_all_courses(search)

    def add_course(self, data):
        return self.model.create_course(*data)

    def delete_course(self, cid):
        return self.model.delete_course(cid)

    def enroll_student(self, student_id, course_id):
        return self.model.enroll_student(student_id, course_id)

    def unenroll_student(self, student_id, course_id):
        return self.model.unenroll_student(student_id, course_id)

    def get_teacher_courses_data(self):
        return self.model.get_teacher_courses(self.current_user['id'])

    def get_course_assignments_data(self, course_id, search=""):
        return self.model.get_course_assignments(course_id, search)

    def get_course_students(self, course_id):
        return self.model.get_course_students(course_id, self.current_user['id'])

    def add_assignment(self, data, student_ids=[], attachment_path=None):
        assignment_id = self.model.create_assignment(*data, attachment_path)
        if assignment_id:
            if student_ids:
                self.model.distribute_assignment(assignment_id, student_ids)
            return True
        return False
    
    def delete_assignment(self, aid):
        return self.model.delete_assignment(aid)

    def get_assignment_submissions(self, assignment_id, search=""):
        return self.model.get_assignment_submissions(assignment_id, search)

    def save_grade_and_feedback(self, student_id, assignment_id, score, feedback):
        return self.model.save_grade_and_feedback(student_id, assignment_id, score, feedback)

    def submit_assignment(self, assignment_id, text, file_path):
        return self.model.submit_assignment(self.current_user['id'], assignment_id, text, file_path)

    def get_student_report_card(self, search=""):
        return self.model.get_student_grades(self.current_user['id'], search)
