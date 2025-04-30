Waynest - Vacation Rental Platform
Waynest is a vacation rental platform inspired by Airbnb that suggests activities and destinations based on weather conditions. Built with Flask, MySQL, and Bootstrap 5, it helps users plan better trips.
Tech Stack

Frontend: HTML, CSS, Bootstrap 5
Backend: Python (Flask)
Database: MySQL

Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/Waynest.git
cd Waynest

2. Set Up a Virtual Environment
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install flask flask-wtf mysql-connector-python werkzeug

4. Set Up the Database

Ensure MySQL is running (mysql.server start).
Apply the schema:mysql -u root -p < init_db.sql

Enter password: your MySQL password

5. Run the Application
python app.py

Access Waynest at http://127.0.0.1:5000.
Usage

Homepage: See weather-based suggestions.
Login: Use alice.jones@example.com / password123.
Properties: Browse at /properties.
Bookings: View at /bookings.

