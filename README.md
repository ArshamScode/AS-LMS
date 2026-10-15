
# AS-LMS — Learning Management System

A desktop-based Learning Management System built with Python, Tkinter, and MySQL. AS-LMS provides separate interfaces for administrators, teachers, and students to manage courses, assignments, submissions, grades, and academic feedback.

## Features

### Administrator
- Manage user accounts and roles.
- Manage courses and course enrollments.
- Assign teachers and students to the appropriate academic relationships.
- Manage student–teacher advisor relationships.

### Teacher
- Access the teacher interface.
- Manage course assignments.
- Set assignment descriptions, maximum scores, and deadlines.
- Review student submissions.
- Grade submitted work and provide feedback.

### Student
- Access enrolled courses and assigned work.
- View assignment details and deadlines.
- Submit assignment content.
- View grades and teacher feedback.

## Technology Stack

- **Language:** Python
- **GUI:** Tkinter and ttk
- **Database:** MySQL
- **Database Connector:** MySQL Connector/Python
- **Password Hashing:** SHA-256

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or a compatible version
- MySQL Server
- pip

## Project Structure

```text
AS-LMS/
├── main.py
├── view.py
├── controller.py
├── model.py
├── style.py
├── requirements.txt
├── .gitignore
├── .env.example
├── help.txt
├── database/
│   ├── schema.sql
│   └── seed.sql
└── README.md
```

The exact files in your repository may differ slightly from this example.

## Installation and Setup

### 1. Download the project

Clone the repository:

```bash
git clone https://github.com/ArshamScode/AS-LMS.git
cd AS-LMS
```

Alternatively, select **Code → Download ZIP** on GitHub and extract the archive.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Make sure MySQL Server is installed and running.

Review the database connection settings used by the application, typically in `model.py`. Configure the host, port, username, password, and database name for your local MySQL installation.

Do not publish real database passwords or other private credentials.

### 5. Create the database tables

Open MySQL Workbench or another MySQL client and execute:

```text
database/schema.sql
```

This script creates the database and the tables required by the application. It does not intentionally drop an existing database.

### 6. Insert demonstration data

After creating the schema, execute:

```text
database/seed.sql
```

This inserts demonstration users, a course, enrollments, and an assignment.

Run the seed script only once on a fresh demonstration database unless you have checked its effects. The sample inserts are not designed as a repeatable migration.

### 7. Run the application

From the project directory, run:

```bash
python main.py
```

## Demo Login Credentials

The demonstration accounts use the following credentials, provided that `database/seed.sql` has been executed successfully.

**Password for all demo accounts:** `password123`

| Role | Username | Password |
|---|---|---|
| Administrator | `admin` | `password123` |
| Teacher | `teacher1` | `password123` |
| Student | `student1` | `password123` |
| Student | `student2` | `password123` |

These accounts are for local testing and demonstration only. Do not use the sample password for real accounts or sensitive information.

## Database

The database schema includes tables for:

- Users and roles
- Teacher–student advisor relationships
- Courses and enrollments
- Assignments and assignment distribution
- Student submissions
- Grades and feedback

The SQL scripts are provided separately so users can create the database structure and optionally load demonstration data.

## Security Notes

- The included demo accounts use a shared demonstration password.
- SHA-256 is used by the current project for password hashing. For production systems, use a password-hashing algorithm designed for passwords, such as Argon2id, scrypt, or bcrypt, with appropriate configuration.
- Configure your own MySQL credentials locally.
- Never commit real passwords, API keys, private configuration files, or sensitive user data to a public repository.
- Review and test the project before using it with real users or production data.

## Troubleshooting

**MySQL connection error**
- Confirm that MySQL Server is running.
- Verify the host, port, username, and password in the application's database configuration.
- Confirm that the database has been created successfully.

**Missing Python module**
- Activate the virtual environment.
- Run `pip install -r requirements.txt` again.

**Demo login does not work**
- Confirm that `database/seed.sql` ran successfully.
- Check that the application and seed script use the same database.
- Verify that the password hashing logic matches the hashes stored in the database.

## Project Purpose

AS-LMS is a desktop software project demonstrating Python GUI development, MySQL integration, role-based interfaces, and common learning-management workflows.

## Author

**Arsham Sarmast**

GitHub: [@ArshamScode](https://github.com/ArshamScode)

## License

No license has been specified yet. Unless a license is added to this repository, users should not assume that they have permission to redistribute, modify, or commercially use the project.

---

If you find this project useful, consider starring the repository on GitHub.
