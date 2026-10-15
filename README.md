[🇬🇧 English](README.md) | [🇮🇷 فارسی](README.fa.md) | [🇸🇦 العربية](README.ar.md) | [🇨🇳 简体中文](README.zh-CN.md)

---

# AS-LMS — Learning Management System

AS-LMS is a desktop-based Learning Management System built with Python, Tkinter, and MySQL. It provides separate interfaces for administrators, teachers, and students to manage courses, assignments, submissions, grades, and academic feedback.

## Features

### Administrator
- Manage user accounts and roles.
- Manage courses and course enrollments.
- Assign teachers and students to appropriate academic relationships.
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
- **Password Hashing:** SHA-256 in the current implementation

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or a compatible version
- MySQL Server
- pip

## Project Structure

The following is an example of the project structure. The actual files in the repository may differ.

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

## Installation and Setup

### 1. Download the project

Clone the repository:

```bash
git clone https://github.com/ArshamScode/AS-LMS.git
cd AS-LMS
```

Alternatively, select **Code → Download ZIP** on GitHub and extract the downloaded archive.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bat
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Make sure MySQL Server is installed and running.

Configure the database host, port, username, password, and database name according to your local MySQL installation. Review the database connection settings used by the application, typically in `model.py`.

Do not commit real database passwords or other private credentials to the repository.

### 5. Create the database tables

If your repository contains `database/schema.sql`, open MySQL Workbench or another MySQL client and execute that script to create the database structure.

Review the SQL script before running it. Confirm that it will not delete or overwrite a database containing data you need to keep.

### 6. Insert demonstration data

If your repository contains `database/seed.sql`, execute it after creating the schema to insert the demonstration data.

Run the seed script only when appropriate. Unless it is explicitly designed to be repeatable, running it multiple times may cause duplicate records or other database issues.

### 7. Run the application

From the project directory, run:

```bash
python main.py
```

## Demo Login Credentials

The following demonstration accounts are documented for local testing. They will work only if the database has been initialized with matching account records and password hashes.

**Demonstration password:** `password123`

| Role | Username | Password |
|---|---|---|
| Administrator | `admin` | `password123` |
| Teacher | `teacher1` | `password123` |
| Student | `student1` | `password123` |
| Student | `student2` | `password123` |

These accounts are for local testing and demonstration only. Do not use the sample password for real accounts or sensitive information.

## Database

The database is designed to support the application's learning-management workflows, including:

- Users and roles
- Teacher–student advisor relationships
- Courses and enrollments
- Assignments and assignment distribution
- Student submissions
- Grades and feedback

Refer to the SQL files included in the repository for the actual database schema and any available demonstration data.

## Security Notes

- The demonstration accounts use a shared sample password.
- The current implementation uses SHA-256 for password hashing. SHA-256 alone is not recommended for storing passwords in production applications. Use a password-hashing algorithm designed for passwords, such as Argon2id, scrypt, or bcrypt, with appropriate configuration.
- Configure your own MySQL credentials locally.
- Never commit real passwords, API keys, private configuration files, or sensitive user data to a public repository.
- Review SQL scripts before executing them, especially if they create, drop, or overwrite databases or tables.
- Review and test the project before using it with real users or production data.

## Troubleshooting

**MySQL connection error**
- Confirm that MySQL Server is running.
- Verify the host, port, username, and password in the application's database configuration.
- Confirm that the required database and tables exist.

**Missing Python module**
- Activate the virtual environment.
- Run `pip install -r requirements.txt` again.
- Confirm that `requirements.txt` lists the dependencies required by the application.

**Demo login does not work**
- Confirm that the demonstration account records exist in the database.
- Check that the application connects to the same database that contains those records.
- Verify that the password hashing logic matches the password hashes stored in the database.

## Project Purpose

AS-LMS is a desktop software project demonstrating Python GUI development, MySQL integration, role-based interfaces, and common learning-management workflows.

## Screenshots

### Login Screen

![AS-LMS Login Screen](docs/screenshots/login.png)

### Administrator Dashboard

![AS-LMS Administrator Dashboard](docs/screenshots/admin-dashboard.png)

### Teacher Dashboard

![AS-LMS Teacher Dashboard](docs/screenshots/teacher-dashboard.png)

### Student Dashboard

![AS-LMS Student Dashboard](docs/screenshots/student-dashboard.png)

If a screenshot does not appear, check that the image exists at the specified path and that its filename and capitalization match the Markdown link.

## Author

**Arsham Sarmast**

GitHub: [@ArshamScode](https://github.com/ArshamScode)

## License

AS-LMS is licensed under the MIT License. See the [LICENSE](LICENSE) file for the full license text.

The MIT License permits use, modification, distribution, and commercial use, subject to its terms, including preservation of the copyright and license notices. The software is provided without warranty. See the `LICENSE` file for details.

---

If you find this project useful, consider starring the repository on GitHub.
