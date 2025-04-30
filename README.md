# Waynest - Vacation Rental Platform

Waynest is a weather-vibe-based vacation rental platform inspired by Airbnb. It suggests activities and destinations based on current weather conditions to enhance the user's travel experience. Built using Flask, MySQL, and Bootstrap 5, Waynest offers a smooth user experience with a fully functional backend and a well-normalized database structure.

## Tech Stack
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript, Google Fonts, Font Awesome
- **Backend**: Python (Flask)
- **Database**: MySQL (3NF normalized with PL/SQL triggers and procedures)
- **API Integration**: OpenWeatherMap API

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/Waynest.git
   cd Waynest

   python3 -m venv venv
source venv/bin/activate
pip install flask flask-wtf mysql-connector-python werkzeug
mysql -u root -p < init_db.sql
python app.py

