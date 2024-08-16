# Expense Tracker Web Application

## Overview

This comprehensive expense tracker web application allows users to enter, manage, and analyze their expenses and income. Built with a robust tech stack including HTML, CSS, JavaScript, and Django, it offers a user-friendly interface coupled with powerful backend functionality.

## Features

- User authentication and account management
- Expense and income entry
- Data visualization with interactive graphs and pie charts
- Real-time username and email validation
- Admin interface for database management
- Responsive design for various devices

## Tech Stack

- Frontend:
  - HTML5
  - CSS3
  - JavaScript
  - Chart.js (for data visualization)
- Backend:
  - Django (Python web framework)
  - PostgreSQL (database)
- Other Technologies:
  - AJAX (for real-time validation)

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/expense-tracker.git
```
2. Navigate to the project directory:
```
cd expense-tracker
```
3. Create a virtual environment:
```
python -m venv venv
```
4. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

5. Install the required packages:
```
pip install -r requirements.txt
```
6. Set up the PostgreSQL database and update the `DATABASES` configuration in `settings.py`

7. Run migrations:
```
python manage.py migrate
```
8. Create a superuser for admin access:
```
python manage.py createsuperuser
```
9. Start the development server:
```
python manage.py runserver
```
10. Access the application at `http://localhost:8000`

## Usage

1. Register for a new account or log in with existing credentials
2. Add your expenses and income through the user-friendly interface
3. View and analyze your financial data using the interactive charts and graphs
4. Access the admin interface at `http://localhost:8000/admin` using superuser credentials

## Data Visualization

The application uses Chart.js to provide the following visualizations:

- Pie chart for expense categories
- Line graph for income vs. expenses over time
- Bar chart for monthly spending analysis

## Real-time Validation

AJAX is utilized for real-time username and email validation during the registration process, enhancing user experience and reducing errors.

## Admin Interface

The Django admin interface allows authorized users to:

- View and edit user accounts
- Manage expense and income entries
- Perform database operations

## Database

PostgreSQL is used as the primary database for its robustness and ability to handle complex queries efficiently.

## License

Distributed under the MIT License. See `LICENSE` for more information.
