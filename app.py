from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, FileField
from wtforms.validators import DataRequired, Optional
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Custom Jinja filters
def date_format(value):
    if isinstance(value, str):
        value = datetime.strptime(value, '%Y-%m-%d')
    return value.strftime('%B %d, %Y')

def format_price(value):
    return f"{float(value):.2f}"

app.jinja_env.filters['date_format'] = date_format
app.jinja_env.filters['format_price'] = format_price

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Flask-WTF form for listing properties
class ListPropertyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price_per_night = FloatField('Price per Night ($)', validators=[DataRequired()])
    image = FileField('Property Image', validators=[Optional()])
    experience_title = StringField('Experience Title', validators=[Optional()])
    experience_description = TextAreaField('Experience Description', validators=[Optional()])

# Weather Vibes for all 34 locations
WEATHER_VIBES = {
    'Miami, FL': {
        'sunny': 'Soak up the sun with a beachside picnic—join our Sunset Beach Walk!',
        'rainy': 'Savor a cozy café vibe—try a local Cuban eatery!',
        'snowy': 'Dream of snow with an indoor spa day—book a Miami wellness retreat!'
    },
    'New York, NY': {
        'sunny': 'Stroll Central Park’s sunny paths—join our City Food Tour!',
        'rainy': 'Dive into a museum adventure—explore our curated art walk!',
        'snowy': 'Embrace the snow with ice skating—visit Rockefeller Center!'
    },
    'Aspen, CO': {
        'sunny': 'Hike scenic trails under blue skies—try our Hiking Adventure!',
        'rainy': 'Cozy up by a fireplace—enjoy a local café’s hot cocoa!',
        'snowy': 'Hit the slopes for epic skiing—book our Ski Adventure!'
    },
    'Paris, France': {
        'sunny': 'Picnic by the Seine—join our Eiffel Tower Picnic!',
        'rainy': 'Sip coffee in a cozy café—explore our local café tour!',
        'snowy': 'Imagine a snowy Paris—visit a patisserie for warm pastries!'
    },
    'Tokyo, Japan': {
        'sunny': 'Wander temple gardens—experience our Tea Ceremony!',
        'rainy': 'Enjoy sushi indoors—join a cooking class!',
        'snowy': 'Cozy up with ramen—try a local noodle shop!'
    },
    'Santorini, Greece': {
        'sunny': 'Sail the caldera’s sparkling waters—book our Sunset Cruise!',
        'rainy': 'Taste wines indoors—visit a local winery!',
        'snowy': 'Dream of snow with a cozy taverna meal—enjoy Greek comfort food!'
    },
    'Sydney, Australia': {
        'sunny': 'Climb the Harbour Bridge—join our guided tour!',
        'rainy': 'Explore the aquarium—dive into marine wonders!',
        'snowy': 'Imagine snow with a cozy pub night—try Aussie craft beers!'
    },
    'Tuscany, Italy': {
        'sunny': 'Tour sunny vineyards—join our Wine Tasting Tour!',
        'rainy': 'Cook Italian indoors—try a pasta-making class!',
        'snowy': 'Cozy up with Chianti—visit a rustic trattoria!'
    },
    'Cape Town, South Africa': {
        'sunny': 'Hike Table Mountain’s trails—book our guided tour!',
        'rainy': 'Shop vibrant markets indoors—explore local crafts!',
        'snowy': 'Dream of snow with a cozy wine tasting—visit a Stellenbosch cellar!'
    },
    'Rio de Janeiro, Brazil': {
        'sunny': 'Dance on Copacabana Beach—learn Samba with our lesson!',
        'rainy': 'Join a carnival workshop—master dance moves indoors!',
        'snowy': 'Imagine snow with a caipirinha—hit a lively bar!'
    },
    'Barcelona, Spain': {
        'sunny': 'Marvel at Gaudí’s works—join our Architecture Tour!',
        'rainy': 'Savor tapas indoors—try our food crawl!',
        'snowy': 'Cozy up with churros—visit a historic chocolatier!'
    },
    'Kyoto, Japan': {
        'sunny': 'Meet a geisha under cherry blossoms—join our Cultural Evening!',
        'rainy': 'Meditate indoors—try a temple Zen session!',
        'snowy': 'Warm up with matcha—visit a traditional tea house!'
    },
    'Amsterdam, Netherlands': {
        'sunny': 'Cruise sunny canals—book our Boat Tour!',
        'rainy': 'Explore museums indoors—visit the Rijksmuseum!',
        'snowy': 'Imagine snow with stroopwafels—cozy up in a café!'
    },
    'Banff, Canada': {
        'sunny': 'Ride the gondola for epic views—book our Scenic Tour!',
        'rainy': 'Relax in a hot spring—try a spa day!',
        'snowy': 'Ski the Rockies—join our Ski Adventure!'
    },
    'Dubai, UAE': {
        'sunny': 'Venture on a desert safari—book our Adventure Tour!',
        'rainy': 'Shop in luxury—explore Dubai Mall!',
        'snowy': 'Dream of snow at Ski Dubai—try indoor skiing!'
    },
    'Havana, Cuba': {
        'sunny': 'Dance salsa in the streets—join our Cuban Salsa Workshop!',
        'rainy': 'Taste cigars indoors—visit a local lounge!',
        'snowy': 'Cozy up with mojitos—hit a vibrant bar!'
    },
    'Reykjavik, Iceland': {
        'sunny': 'Soak in hot springs—visit the Blue Lagoon!',
        'rainy': 'Explore Viking history—tour a museum!',
        'snowy': 'Chase the Northern Lights—book our guided tour!'
    },
    'Marrakech, Morocco': {
        'sunny': 'Wander colorful souks—join our Medina Tour!',
        'rainy': 'Relax in a hammam—book a spa day!',
        'snowy': 'Imagine snow with mint tea—cozy up in a riad!'
    },
    'Seoul, South Korea': {
        'sunny': 'Learn K-pop moves—join our Dance Workshop!',
        'rainy': 'Savor Korean BBQ—try a local eatery!',
        'snowy': 'Warm up with tteokbokki—visit a street food stall!'
    },
    'Venice, Italy': {
        'sunny': 'Ride a gondola—book our Serenade Tour!',
        'rainy': 'Tour art galleries—visit a historic palazzo!',
        'snowy': 'Cozy up with tiramisu—try a Venetian café!'
    },
    'Queenstown, New Zealand': {
        'sunny': 'Cruise Milford Sound—book our Scenic Tour!',
        'rainy': 'Taste local wines—visit a vineyard!',
        'snowy': 'Ski the Remarkables—join our Ski Adventure!'
    },
    'Lisbon, Portugal': {
        'sunny': 'Enjoy fado music outdoors—join our Tavern Tour!',
        'rainy': 'Craft azulejo tiles—try a workshop!',
        'snowy': 'Warm up with pastéis de nata—visit a bakery!'
    },
    'Ubud, Bali': {
        'sunny': 'Learn Balinese cooking—join our Cooking Class!',
        'rainy': 'Practice yoga indoors—book a retreat session!',
        'snowy': 'Dream of snow with a spa day—try a Balinese massage!'
    },
    'Edinburgh, Scotland': {
        'sunny': 'Explore haunted castles—join our Ghost Tour!',
        'rainy': 'Sip whisky indoors—visit a historic pub!',
        'snowy': 'Cozy up with a ceilidh—try a Scottish dance night!'
    },
    'Vancouver, Canada': {
        'sunny': 'Kayak the harbor—book our Coastal Adventure!',
        'rainy': 'Tour art galleries—explore Granville Island!',
        'snowy': 'Imagine snow with a hot toddy—hit a cozy café!'
    },
    'Chiang Mai, Thailand': {
        'sunny': 'Taste street food—join our Night Market Tour!',
        'rainy': 'Craft Thai lanterns—try a workshop!',
        'snowy': 'Cozy up with khao soi—visit a local eatery!'
    },
    'Buenos Aires, Argentina': {
        'sunny': 'Dance tango outdoors—join our Tango Night!',
        'rainy': 'Savor steak indoors—try a parrilla!',
        'snowy': 'Warm up with mate—visit a traditional café!'
    },
    'Dubrovnik, Croatia': {
        'sunny': 'Tour Game of Thrones sites—book our Walking Tour!',
        'rainy': 'Explore maritime history—visit a museum!',
        'snowy': 'Dream of snow with rakija—cozy up in a tavern!'
    },
    'Nairobi, Kenya': {
        'sunny': 'Go on safari—book our Day Trip Adventure!',
        'rainy': 'Discover local crafts—tour a market indoors!',
        'snowy': 'Imagine snow with nyama choma—try a Kenyan BBQ!'
    },
    'San Francisco, CA': {
        'sunny': 'Bike the Golden Gate—join our Cycling Tour!',
        'rainy': 'Explore tech history—visit a museum!',
        'snowy': 'Cozy up with clam chowder—try a pier eatery!'
    },
    'Prague, Czech Republic': {
        'sunny': 'Stroll Charles Bridge—join our Sunset Tour!',
        'rainy': 'Tour historic pubs—try Czech beers!',
        'snowy': 'Warm up with goulash—visit a cozy restaurant!'
    },
    'Auckland, New Zealand': {
        'sunny': 'Discover Maori culture—join our Cultural Evening!',
        'rainy': 'Explore art indoors—visit a gallery!',
        'snowy': 'Imagine snow with pavlova—cozy up in a café!'
    },
    'Cairo, Egypt': {
        'sunny': 'Explore the pyramids—book our Egyptologist Tour!',
        'rainy': 'Discover artifacts—tour the Egyptian Museum!',
        'snowy': 'Dream of snow with koshari—try a street food stall!'
    },
    'Dehradun, India': {
        'sunny': 'Practice yoga outdoors—join our Mountain Retreat!',
        'rainy': 'Savor chai indoors—visit a local tea house!',
        'snowy': 'Cozy up with momos—try a Himalayan eatery!'
    }
}

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_host = 'is_host' in request.form

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password, is_host) VALUES (%s, %s, %s, %s)',
                (username, email, hashed_password, is_host)
            )
            conn.commit()
            cursor.close()
            conn.close()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            flash(f'Error: {e}', 'danger')
    
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_host'] = user['is_host']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# List property route
@app.route('/list_property', methods=['GET', 'POST'])
def list_property():
    if 'user_id' not in session or not session.get('is_host'):
        flash('You must be a host to list a property.', 'danger')
        return redirect(url_for('login'))
    
    form = ListPropertyForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        location = form.location.data
        price_per_night = form.price_per_night.data
        experience_title = form.experience_title.data
        experience_description = form.experience_description.data
        image_path = None

        if form.image.data:
            file = form.image.data
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = os.path.join('images', filename).replace('\\', '/')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO properties (host_id, title, description, location, price_per_night, image_path) VALUES (%s, %s, %s, %s, %s, %s)',
                (session['user_id'], title, description, location, price_per_night, image_path)
            )
            property_id = cursor.lastrowid
            
            if experience_title and experience_description:
                cursor.execute(
                    'INSERT INTO experiences (property_id, title, description) VALUES (%s, %s, %s)',
                    (property_id, experience_title, experience_description)
                )
            
            conn.commit()
            cursor.close()
            conn.close()
            flash('Property listed successfully!', 'success')
            return redirect(url_for('properties'))
        except mysql.connector.Error as e:
            flash(f'Error: {e}', 'danger')
    
    return render_template('list_property.html', form=form)

# Properties route
@app.route('/properties')
def properties():
    location = request.args.get('location', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = 'SELECT * FROM properties WHERE location LIKE %s'
    cursor.execute(query, ('%' + location + '%',))
    properties = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('properties.html', properties=properties, location=location)

# Property detail route
@app.route('/property/<int:property_id>', methods=['GET', 'POST'])
def property_detail(property_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT * FROM properties WHERE id = %s', (property_id,))
    property = cursor.fetchone()
    
    cursor.execute('SELECT * FROM experiences WHERE property_id = %s', (property_id,))
    experiences = cursor.fetchall()
    
    cursor.execute('SELECT r.*, u.username FROM reviews r JOIN users u ON r.user_id = u.id WHERE r.property_id = %s', (property_id,))
    reviews = cursor.fetchall()
    
    vibe_tip = None
    if request.method == 'POST':
        if 'check_in' in request.form and 'weather_vibe' in request.form:
            check_in = request.form['check_in']
            weather_vibe = request.form['weather_vibe']
            location = property['location']
            vibe_tip = WEATHER_VIBES.get(location, {}).get(weather_vibe, 'Enjoy your stay!')
        elif 'check_in' in request.form:  # Booking form
            check_in = request.form['check_in']
            check_out = request.form['check_out']
            total_price = float(request.form['total_price'])
            
            try:
                cursor.execute(
                    'INSERT INTO bookings (user_id, property_id, check_in, check_out, total_price) VALUES (%s, %s, %s, %s, %s)',
                    (session['user_id'], property_id, check_in, check_out, total_price)
                )
                conn.commit()
                flash('Booking successful!', 'success')
                return redirect(url_for('bookings'))
            except mysql.connector.Error as e:
                flash(f'Error: {e}', 'danger')
        elif 'rating' in request.form:  # Review form
            rating = request.form['rating']
            comment = request.form['comment']
            
            try:
                cursor.execute(
                    'INSERT INTO reviews (user_id, property_id, rating, comment) VALUES (%s, %s, %s, %s)',
                    (session['user_id'], property_id, rating, comment)
                )
                conn.commit()
                flash('Review submitted!', 'success')
                return redirect(url_for('property_detail', property_id=property_id))
            except mysql.connector.Error as e:
                flash(f'Error: {e}', 'danger')
    
    cursor.close()
    conn.close()
    return render_template('property_detail.html', property=property, experiences=experiences, reviews=reviews, vibe_tip=vibe_tip)

# Bookings route
@app.route('/bookings')
def bookings():
    if 'user_id' not in session:
        flash('Please log in to view bookings.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        'SELECT b.*, p.title FROM bookings b JOIN properties p ON b.property_id = p.id WHERE b.user_id = %s',
        (session['user_id'],)
    )
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)