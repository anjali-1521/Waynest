Waynest - Weather-Vibe-Based Vacation Rental Platform

Waynest is a vacation rental platform inspired by Airbnb, designed to enhance travel planning by suggesting activities and destinations based on current weather conditions. Built using Flask, MySQL, and Bootstrap 5, Waynest offers a seamless user experience with a fully functional backend, a well-normalized database structure, and a clean, responsive frontend. The platform integrates the OpenWeatherMap API to fetch real-time weather data, enabling dynamic weather-based recommendations.

Problem Statement

Current vacation rental platforms often fail to suggest activities based on weather or user vibe, leading to less satisfying travel experiences. Waynest addresses this by providing weather-aware recommendations, ensuring users can plan activities that match the local conditions.

Motivation

The goal of Waynest is to create a smart and intuitive rental platform that enhances travel planning by integrating weather-based suggestions, helping users make the most of their trips regardless of the forecast.

Tech Stack





Frontend: HTML5, CSS3, Bootstrap 5, JavaScript, Google Fonts (Montserrat), Font Awesome



Backend: Python (Flask)



Database: MySQL (3NF normalized with PL/SQL triggers and procedures)



API Integration: OpenWeatherMap API

Features





Weather-Based Activity Suggestions: Suggests activities (e.g., skiing, beach trips) based on the current weather at each property’s location.



User Registration and Login: Secure user authentication with session management.



Property Listings by Hosts: Hosts can list properties with details like title, location, price per night, and availability.



Search and Booking Functionality: Users can search for properties and book stays with specified check-in and check-out dates.



Dynamic Weather Suggestions on Homepage: The homepage displays weather-based suggestions for popular destinations.

Project Structure

Waynest/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings (e.g., MySQL credentials)
├── init_db.sql            # SQL script to initialize the database
├── test_db.py             # Script to test database connection
├── static/
│   ├── css/
│   │   └── style.css      # Custom CSS for styling
│   └── images/            # Images for properties (optional)
└── templates/
    ├── base.html          # Base template with navbar and layout
    ├── index.html         # Homepage with weather-based suggestions
    ├── properties.html    # Property listings page
    ├── bookings.html      # User bookings page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── list_property.html # Form for hosts to list properties
    ├── mood_boards.html   # Mood board creation and listing (if applicable)
    └── view_mood_board.html # View a specific mood board (if applicable)

Setup Instructions

Follow these steps to set up and run Waynest on your local machine.

Prerequisites





Python 3.x: Ensure Python 3 is installed (python3 --version).



MySQL: Install and run MySQL (mysql.server start).



Git: Install Git to clone the repository (git --version).



ChromeDriver (optional): If using the OpenWeatherMap API with scraping, you may need ChromeDriver for Selenium.

1. Clone the Repository

Clone the Waynest repository from GitHub to your local machine.

git clone https://github.com/your-username/Waynest.git
cd Waynest

Replace your-username with your actual GitHub username.

2. Set Up a Virtual Environment

Create and activate a virtual environment to manage dependencies.

python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# For Windows: venv\Scripts\activate

3. Install Dependencies

Install the required Python packages listed in requirements.txt.

pip install flask flask-wtf mysql-connector-python werkzeug

If you have a requirements.txt file, you can install all dependencies at once:

pip install -r requirements.txt

4. Set Up the Database

Waynest uses a MySQL database named waynest. Apply the database schema using the init_db.sql script.

mysql -u root -p < init_db.sql





Enter your MySQL password when prompted (default: ShopSphere2025! in our setup; adjust if different).



This script creates the waynest database, sets up tables (users, properties, bookings, weather, activities), and populates them with sample data.

Verify the database:

mysql -u root -p -e "USE waynest; SHOW TABLES;"

5. Configure OpenWeatherMap API (Optional)

Waynest integrates the OpenWeatherMap API for weather data. To use this feature:





Sign up at https://openweathermap.org/ and get an API key.



Add the API key to your environment or configuration:





Create a .env file (optional):

echo "OPENWEATHERMAP_API_KEY=your-api-key" > .env



Or modify config.py to include the API key:

class Config:
    OPENWEATHERMAP_API_KEY = 'your-api-key'
    # Other settings...

6. Run the Application

Start the Flask server to run Waynest.

python app.py

You should see:

 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!

7. Access Waynest

Open your browser and go to:

http://127.0.0.1:5000





Homepage: Displays weather-based suggestions for destinations.



Login: Use credentials like alice.jones@example.com / password123 (from sample data).



Properties: View listings at /properties (e.g., "Lakeside Cabin" in Finger Lakes, "Beachfront Bungalow" in Bali).



Bookings: Check your bookings at /bookings.

Database Design

The waynest database is designed in Third Normal Form (3NF) for data integrity and scalability:





Tables:





users: Stores user information (id, username, email, password, is_host).



properties: Stores property listings (id, host_id, title, location, price_per_night, availability).



bookings: Stores booking details (id, user_id, property_id, check_in, check_out, total_price).



weather: Stores weather data for locations (id, location, temperature, condition).



activities: Stores activity suggestions (id, location, weather_condition, activity).



PL/SQL Features:





Triggers: Handle booking validation and update property availability.



Stored Procedures: Generate booking reports and manage activity suggestions.

Sample Data





Locations: Includes diverse places like Miami, FL; Honolulu, HI; Banff, Canada; Santorini, Greece; and Sydney, Australia.



Properties: Over 30 properties, such as "Tropical Beach Villa" (Honolulu), "Clifftop Villa" (Big Sur), and "Island Getaway" (Phuket).



Weather: Conditions like Sunny, Snowy, Rainy, and Cloudy for each location.



Activities: Suggestions like "Surfing at Waikiki Beach" (Sunny in Honolulu) and "Skiing at Lake Louise" (Snowy in Banff).

Troubleshooting





Virtual Environment Activation Fails:

python3 -m venv venv
source venv/bin/activate



Database Connection Errors:





Ensure MySQL is running:

mysql.server start



Verify the database:

mysql -u root -p -e "SHOW DATABASES;"



Reapply if needed:

mysql -u root -p < init_db.sql



Flask Server Fails to Start:





Check for missing dependencies:

pip install flask flask-wtf mysql-connector-python werkzeug



Ensure app.py is configured correctly with MySQL credentials in config.py.



Properties or Bookings Not Showing:





Clear browser cache (Cmd + Shift + R in Chrome).



Verify the database has data:

mysql -u root -p -e "SELECT * FROM properties LIMIT 5;"
