-- init_db.sql
-- Use the waynest database
USE waynest;

-- Drop tables if they exist to start fresh
DROP TABLE IF EXISTS booking_logs;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS experiences;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS users;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_host BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create properties table
CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    host_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(100) NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    image_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create bookings table
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

-- Create experiences table (unique feature)
CREATE TABLE experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

-- Create reviews table
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

-- Create booking_logs table (for trigger)
CREATE TABLE booking_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    user_id INT NOT NULL,
    property_id INT NOT NULL,
    log_message VARCHAR(255) NOT NULL,
    log_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users
INSERT INTO users (username, email, password, is_host) VALUES
('host1', 'host1@example.com', '$pbkdf2-sha256$29000$6t1r7R1jrDXGnLO2NsaYUw$z3y6Qz6y6Qz6y6Qz6y6Qz6y6Qz6y6Qz6y6Qz6y6Qz6', TRUE),
('guest1', 'guest1@example.com', '$pbkdf2-sha256$29000$6t1r7R1jrDXGnLO2NsaYUw$z3y6Qz6y6Qz6y6Qz6y6Qz6y6Qz6y6Qz6y6Qz6y6Qz6', FALSE);

-- Insert properties (23 original + 10 new + Dehradun)
INSERT INTO properties (host_id, title, description, location, price_per_night, image_path) VALUES
(1, 'Cozy Beach Cottage', 'A charming cottage by the sea with stunning views.', 'Miami, FL', 120.00, 'images/cottage.jpg'),
(1, 'Downtown Loft', 'Modern loft in the heart of the city.', 'New York, NY', 150.00, 'images/loft.jpg'),
(1, 'Mountain Cabin', 'Rustic cabin surrounded by nature.', 'Aspen, CO', 100.00, 'images/cabin.jpg'),
(1, 'Parisian Chic Apartment', 'Elegant apartment near the Eiffel Tower.', 'Paris, France', 180.00, 'images/paris.jpg'),
(1, 'Tokyo Zen Retreat', 'Tranquil house with a traditional Japanese garden.', 'Tokyo, Japan', 200.00, 'images/tokyo.jpg'),
(1, 'Santorini Cliff Villa', 'Whitewashed villa with panoramic sea views.', 'Santorini, Greece', 250.00, 'images/santorini.jpg'),
(1, 'Sydney Harbour Suite', 'Luxurious suite overlooking the Opera House.', 'Sydney, Australia', 220.00, 'images/sydney.jpg'),
(1, 'Tuscan Vineyard Cottage', 'Cozy cottage in the heart of wine country.', 'Tuscany, Italy', 140.00, 'images/tuscany.jpg'),
(1, 'Cape Town Coastal Bungalow', 'Beachfront bungalow with mountain views.', 'Cape Town, South Africa', 160.00, 'images/capetown.jpg'),
(1, 'Rio Beachfront Condo', 'Vibrant condo steps from Copacabana Beach.', 'Rio de Janeiro, Brazil', 130.00, 'images/rio.jpg'),
(1, 'Barcelona Gothic Quarter Flat', 'Historic flat in the city’s cultural heart.', 'Barcelona, Spain', 170.00, 'images/barcelona.jpg'),
(1, 'Kyoto Traditional Machiya', 'Authentic townhouse with tatami rooms.', 'Kyoto, Japan', 190.00, 'images/kyoto.jpg'),
(1, 'Amsterdam Canal House', 'Charming house along the iconic canals.', 'Amsterdam, Netherlands', 200.00, 'images/amsterdam.jpg'),
(1, 'Banff Lakeside Chalet', 'Cozy chalet by Lake Louise.', 'Banff, Canada', 180.00, 'images/banff.jpg'),
(1, 'Dubai Skyline Penthouse', 'Luxury penthouse with Burj Khalifa views.', 'Dubai, UAE', 300.00, 'images/dubai.jpg'),
(1, 'Havana Colonial Casa', 'Colorful casa in Old Havana’s historic district.', 'Havana, Cuba', 110.00, 'images/havana.jpg'),
(1, 'Reykjavik Northern Lights Cabin', 'Remote cabin perfect for aurora viewing.', 'Reykjavik, Iceland', 210.00, 'images/reykjavik.jpg'),
(1, 'Marrakech Riad Oasis', 'Traditional riad with a courtyard pool.', 'Marrakech, Morocco', 150.00, 'images/marrakech.jpg'),
(1, 'Seoul Modern Hanok', 'Contemporary take on a traditional Korean house.', 'Seoul, South Korea', 160.00, 'images/seoul.jpg'),
(1, 'Venice Palazzo Suite', 'Opulent suite in a historic Venetian palace.', 'Venice, Italy', 230.00, 'images/venice.jpg'),
(1, 'Queenstown Lakeview Lodge', 'Scenic lodge with views of Lake Wakatipu.', 'Queenstown, New Zealand', 190.00, 'images/queenstown.jpg'),
(1, 'Lisbon Alfama Apartment', 'Quaint apartment in the historic Alfama district.', 'Lisbon, Portugal', 140.00, 'images/lisbon.jpg'),
(1, 'Bali Rice Field Villa', 'Serene villa surrounded by lush rice paddies.', 'Ubud, Bali', 170.00, 'images/bali.jpg'),
(1, 'Historic Old Town Flat', 'Cozy flat in the heart of Edinburgh’s Old Town.', 'Edinburgh, Scotland', 130.00, 'images/edinburgh.jpg'),
(1, 'Waterfront Urban Loft', 'Modern loft with views of Vancouver’s harbor.', 'Vancouver, Canada', 160.00, 'images/vancouver.jpg'),
(1, 'Lantern-Lit Temple Retreat', 'Serene villa near Chiang Mai’s ancient temples.', 'Chiang Mai, Thailand', 110.00, 'images/chiangmai.jpg'),
(1, 'Tango Studio Apartment', 'Vibrant apartment in Buenos Aires’ tango district.', 'Buenos Aires, Argentina', 120.00, 'images/buenosaires.jpg'),
(1, 'Medieval Coastal Villa', 'Charming villa overlooking Dubrovnik’s Adriatic coast.', 'Dubrovnik, Croatia', 200.00, 'images/dubrovnik.jpg'),
(1, 'Safari Gateway Lodge', 'Eco-lodge near Nairobi’s wildlife reserves.', 'Nairobi, Kenya', 140.00, 'images/nairobi.jpg'),
(1, 'Tech City Condo', 'Sleek condo in San Francisco’s vibrant downtown.', 'San Francisco, CA', 180.00, 'images/sanfrancisco.jpg'),
(1, 'Bohemian Castle Apartment', 'Quaint apartment near Prague’s historic castle.', 'Prague, Czech Republic', 150.00, 'images/prague.jpg'),
(1, 'Harborview Bungalow', 'Cozy bungalow with Auckland’s skyline views.', 'Auckland, New Zealand', 170.00, 'images/auckland.jpg'),
(1, 'Nile River Suite', 'Elegant suite steps from Cairo’s ancient pyramids.', 'Cairo, Egypt', 190.00, 'images/cairo.jpg'),
(1, 'Himalayan Serenity Villa', 'Peaceful villa with mountain views in Dehradun.', 'Dehradun, India', 125.00, 'images/dehradun.jpg');

-- Insert experiences (for 23 original + 10 new + Dehradun)
INSERT INTO experiences (property_id, title, description) VALUES
(1, 'Sunset Beach Walk', 'Enjoy a guided walk along the beach at sunset.'),
(2, 'City Food Tour', 'Explore local restaurants with a guided tour.'),
(3, 'Hiking Adventure', 'Discover nearby trails with a local guide.'),
(4, 'Eiffel Tower Picnic', 'Savor a gourmet picnic with views of the Eiffel Tower.'),
(5, 'Tea Ceremony Experience', 'Participate in a traditional Japanese tea ceremony.'),
(6, 'Sunset Caldera Cruise', 'Sail around Santorini’s caldera at sunset.'),
(7, 'Harbour Bridge Climb', 'Climb the Sydney Harbour Bridge for stunning views.'),
(8, 'Wine Tasting Tour', 'Visit local vineyards for a day of wine tasting.'),
(9, 'Table Mountain Hike', 'Hike Table Mountain with a local guide.'),
(10, 'Samba Dance Lesson', 'Learn to dance samba with a professional instructor.'),
(11, 'Gaudi Architecture Tour', 'Explore Gaudí’s masterpieces like Sagrada Família.'),
(12, 'Geisha Cultural Evening', 'Meet a geisha and learn about Kyoto’s traditions.'),
(13, 'Canal Boat Tour', 'Cruise Amsterdam’s canals with a private guide.'),
(14, 'Banff Gondola Ride', 'Ride the gondola for panoramic mountain views.'),
(15, 'Desert Safari Adventure', 'Experience a thrilling desert safari with dinner.'),
(16, 'Cuban Salsa Workshop', 'Learn Cuban salsa in a vibrant dance studio.'),
(17, 'Northern Lights Chase', 'Hunt for the aurora borealis with expert guides.'),
(18, 'Medina Souk Exploration', 'Discover Marrakech’s souks with a local shopper.'),
(19, 'K-Pop Dance Class', 'Master K-pop choreography with a pro dancer.'),
(20, 'Gondola Serenade Ride', 'Enjoy a romantic gondola ride with live music.'),
(21, 'Milford Sound Cruise', 'Cruise through stunning fjords in Milford Sound.'),
(22, 'Fado Music Night', 'Experience soulful fado music in a local tavern.'),
(23, 'Balinese Cooking Class', 'Learn to cook authentic Balinese dishes.'),
(24, 'Castle Ghost Tour', 'Explore Edinburgh’s haunted castles with a guide.'),
(25, 'Kayak Coastal Adventure', 'Paddle Vancouver’s harbor with a local expert.'),
(26, 'Night Market Food Tour', 'Taste Chiang Mai’s street food under lantern lights.'),
(27, 'Tango Dance Night', 'Learn tango with Buenos Aires’ best dancers.'),
(28, 'Game of Thrones Walk', 'Tour Dubrovnik’s iconic filming locations.'),
(29, 'Safari Day Trip', 'Discover Nairobi’s wildlife on a guided safari.'),
(30, 'Golden Gate Bike Tour', 'Cycle San Francisco’s iconic bridge and parks.'),
(31, 'Charles Bridge Sunset Stroll', 'Walk Prague’s historic bridge at dusk.'),
(32, 'Maori Cultural Evening', 'Experience Auckland’s indigenous culture with locals.'),
(33, 'Pyramid Exploration Tour', 'Visit Cairo’s Giza pyramids with an Egyptologist.'),
(34, 'Yoga Mountain Retreat', 'Join a yoga session with Himalayan views in Dehradun.');

-- Insert sample bookings
INSERT INTO bookings (user_id, property_id, check_in, check_out, total_price) VALUES
(2, 1, '2025-05-01', '2025-05-03', 240.00),
(2, 2, '2025-06-01', '2025-06-02', 150.00);

-- Insert sample reviews
INSERT INTO reviews (user_id, property_id, rating, comment) VALUES
(2, 1, 5, 'Amazing stay, loved the beach view!'),
(2, 2, 4, 'Great location, very convenient.');

-- Create trigger
DELIMITER //
CREATE TRIGGER after_insert_booking
AFTER INSERT ON bookings
FOR EACH ROW
BEGIN
    INSERT INTO booking_logs (booking_id, user_id, property_id, log_message)
    VALUES (
        NEW.id,
        NEW.user_id,
        NEW.property_id,
        CONCAT('User ', NEW.user_id, ' booked property ', NEW.property_id, ' on ', DATE_FORMAT(NEW.created_at, '%Y-%m-%d %H:%i:%s'))
    );
END//
DELIMITER ;

-- Create stored procedure
DELIMITER //
CREATE PROCEDURE get_user_bookings(IN p_user_id INT)
BEGIN
    SELECT 
        b.id AS booking_id,
        b.property_id,
        p.title AS property_title,
        b.check_in,
        b.check_out,
        b.total_price,
        b.created_at
    FROM bookings b
    JOIN properties p ON b.property_id = p.id
    WHERE b.user_id = p_user_id
    ORDER BY b.created_at DESC;
END//
DELIMITER ;
