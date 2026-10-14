# AS LMS — Learning Management System

A Python desktop application for managing educational activities, courses, assignments, and student progress.

## Overview

**AS LMS** is a desktop-based Learning Management System built with Python, Tkinter, and MySQL. It provides separate interfaces for administrators, teachers, and students.

## Features

* **Admin dashboard:** Manage users, courses, enrollments, and teacher–student assignments.
* **Teacher dashboard:** Manage assignments, set deadlines and grades, review submissions, and provide feedback.
* **Student dashboard:** View assigned work, submit responses or files, and review grades and feedback.
* **MySQL database:** Store application data in a relational database.
* **Desktop interface:** A graphical interface built with Tkinter and ttk.

## Technology Stack

* Python
* Tkinter / ttk
* MySQL
* MySQL Connector/Python

## Project Structure

```text
AS-LMS/
├── main.py
├── model.py
├── view.py
├── controller.py
├── style.py
└── README.md
```

## Requirements

* Python 3
* MySQL Server
* Python packages listed in `requirements.txt` (when provided)

## Setup

1. Install Python and MySQL Server.
2. Create and configure the application's MySQL database.
3. Install the required Python dependencies.
4. Configure the database connection using your local settings.
5. Run the application with:

```bash
python main.py
```

Database setup and configuration instructions will be documented as the project is prepared for release.

## Security Notice

This project is intended for learning and development. Before using it with real users or sensitive data, review database permissions, credential management, password storage, and role-based access controls.

Never commit real passwords, API keys, private user data, or local `.env` files.

## Author

**Arsham Sarmast**

GitHub: [@ArshamScode](https://github.com/ArshamScode)

---

*AS LMS — Supporting educational workflows through desktop software.*
