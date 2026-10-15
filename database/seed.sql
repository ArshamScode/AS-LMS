USE as_lms_db;

-- Demo users
-- Demo password for all accounts: password
INSERT INTO users (username, password_hash, role, full_name)
VALUES
('admin', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'admin', 'System Admin'),
('teacher1', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'teacher', 'Mr. Smith'),
('student1', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'student', 'Alice Johnson'),
('student2', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 'student', 'Bob Brown');

-- Demo course
INSERT INTO courses (title, description, teacher_id)
VALUES ('Python Tkinter Mastery', 'Advanced GUI concepts.', 2);

-- Enroll demo students
INSERT INTO enrollments (student_id, course_id)
VALUES (3, 1), (4, 1);

-- Demo assignment
INSERT INTO assignments
(course_id, title, description, max_score, deadline, attachment_path)
VALUES
(1, 'Build a Calculator', 'Create a basic calculator app.', 50, '2027-12-31 23:59:00', NULL);

-- Assign the task to demo students
INSERT INTO assignment_distribution (assignment_id, student_id)
VALUES (1, 3), (1, 4);
