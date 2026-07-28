# Expense Tracker

A Django web application for tracking personal expenses, built as a project during vocational training.

## Features
- User signup, login, and logout (Django authentication)
- Add expenses with category, amount, description, and date
- Set a monthly budget
- Dashboard showing total spending, category-wise breakdown chart, and budget usage
- Each user can only view and manage their own expenses

## Tech Stack
- Python 3.14
- Django 6.0
- SQLite (database)
- Bootstrap-inspired custom CSS
- Chart.js (for the spending chart)

## Setup Instructions
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser (optional, for admin access): `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`
6. Visit `http://127.0.0.1:8000/`