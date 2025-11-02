import sqlite3
import json
from datetime import datetime

DB_NAME = 'car_rental.db'

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with car inventory"""
    conn = get_connection()
    cursor = conn.cursor()

    # Create cars table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            category TEXT NOT NULL,
            daily_price REAL NOT NULL,
            passengers INTEGER NOT NULL,
            luggage INTEGER NOT NULL,
            transmission TEXT NOT NULL,
            fuel_type TEXT NOT NULL,
            features TEXT NOT NULL,
            image_url TEXT,
            available BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Check if we already have data
    cursor.execute('SELECT COUNT(*) FROM cars')
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert mock car inventory
        cars = [
            # Economy Cars
            {
                'make': 'Toyota', 'model': 'Corolla', 'year': 2024, 'category': 'Economy',
                'daily_price': 35.00, 'passengers': 5, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Backup Camera'])'image_url': 'https://via.placeholder.com/400x250/4A90E2/FFFFFF?text=Toyota+Corolla+2024',
                'available': 1
            },
            {
                'make': 'Honda', 'model': 'Civic', 'year': 2024, 'category': 'Economy',
                'daily_price': 38.00, 'passengers': 5, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Lane Assist'])'image_url': 'https://via.placeholder.com/400x250/5C6BC0/FFFFFF?text=Honda+Civic+2024',
                'available': 1
            },
            {
                'make': 'Hyundai', 'model': 'Elantra', 'year': 2023, 'category': 'Economy',
                'daily_price': 33.00, 'passengers': 5, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Air Conditioning', 'Bluetooth'])'image_url': 'https://via.placeholder.com/400x250/42A5F5/FFFFFF?text=Hyundai+Elantra+2023',
                'available': 1
            },

            # Compact SUVs
            {
                'make': 'Mazda', 'model': 'CX-5', 'year': 2024, 'category': 'Compact SUV',
                'daily_price': 55.00, 'passengers': 5, 'luggage': 3, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Apple CarPlay', 'All-Wheel Drive']),
                'image_url': 'https://via.placeholder.com/400x250/7E57C2/FFFFFF?text=Mazda+CX-5+2024',
                'available': 1
            },
            {
                'make': 'Honda', 'model': 'CR-V', 'year': 2024, 'category': 'Compact SUV',
                'daily_price': 58.00, 'passengers': 5, 'luggage': 4, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Sunroof', 'Backup Camera']),
                'image_url': 'https://via.placeholder.com/400x250/AB47BC/FFFFFF?text=Honda+CR-V+2024',
                'available': 1
            },
            {
                'make': 'Toyota', 'model': 'RAV4', 'year': 2023, 'category': 'Compact SUV',
                'daily_price': 57.00, 'passengers': 5, 'luggage': 3, 'transmission': 'Automatic',
                'fuel_type': 'Hybrid', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'All-Wheel Drive', 'Lane Assist']),
                'image_url': 'https://via.placeholder.com/400x250/8E24AA/FFFFFF?text=Toyota+RAV4+2023',
                'available': 1
            },

            # Mid-Size SUVs
            {
                'make': 'Chevrolet', 'model': 'Tahoe', 'year': 2024, 'category': 'Full-Size SUV',
                'daily_price': 85.00, 'passengers': 8, 'luggage': 5, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Third Row Seating', 'Leather Interior', '4WD']),
                'image_url': 'https://via.placeholder.com/400x250/EF5350/FFFFFF?text=Chevrolet+Tahoe+2024',
                'available': 1
            },
            {
                'make': 'Ford', 'model': 'Explorer', 'year': 2024, 'category': 'Mid-Size SUV',
                'daily_price': 75.00, 'passengers': 7, 'luggage': 4, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Third Row Seating', 'Apple CarPlay']),
                'image_url': 'https://via.placeholder.com/400x250/E53935/FFFFFF?text=Ford+Explorer+2024',
                'available': 1
            },

            # Luxury Cars
            {
                'make': 'BMW', 'model': '3 Series', 'year': 2024, 'category': 'Luxury',
                'daily_price': 95.00, 'passengers': 5, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Premium Sound System', 'Leather Interior', 'Sunroof', 'Navigation', 'Heated Seats']),
                'image_url': 'https://via.placeholder.com/400x250/212121/FFFFFF?text=BMW+3+Series+2024',
                'available': 1
            },
            {
                'make': 'Mercedes-Benz', 'model': 'C-Class', 'year': 2024, 'category': 'Luxury',
                'daily_price': 98.00, 'passengers': 5, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Premium Sound System', 'Leather Interior', 'Sunroof', 'Navigation', 'Massage Seats']),
                'image_url': 'https://via.placeholder.com/400x250/424242/FFFFFF?text=Mercedes+C-Class+2024',
                'available': 1
            },
            {
                'make': 'Audi', 'model': 'A4', 'year': 2023, 'category': 'Luxury',
                'daily_price': 92.00, 'passengers': 5, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Premium Sound System', 'Leather Interior', 'Virtual Cockpit', 'All-Wheel Drive']),
                'image_url': 'https://via.placeholder.com/400x250/616161/FFFFFF?text=Audi+A4+2023',
                'available': 1
            },

            # Vans/Large Groups
            {
                'make': 'Chrysler', 'model': 'Pacifica', 'year': 2024, 'category': 'Minivan',
                'daily_price': 70.00, 'passengers': 8, 'luggage': 4, 'transmission': 'Automatic',
                'fuel_type': 'Hybrid', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Stow-n-Go Seating', 'Rear Entertainment']),
                'image_url': 'https://via.placeholder.com/400x250/26A69A/FFFFFF?text=Chrysler+Pacifica+2024',
                'available': 1
            },
            {
                'make': 'Honda', 'model': 'Odyssey', 'year': 2024, 'category': 'Minivan',
                'daily_price': 68.00, 'passengers': 8, 'luggage': 4, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Power Sliding Doors', 'Backup Camera']),
                'image_url': 'https://via.placeholder.com/400x250/00897B/FFFFFF?text=Honda+Odyssey+2024',
                'available': 1
            },

            # Electric/Hybrid
            {
                'make': 'Tesla', 'model': 'Model 3', 'year': 2024, 'category': 'Electric',
                'daily_price': 88.00, 'passengers': 5, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Electric', 'features': json.dumps(['Autopilot', 'Premium Sound System', 'Glass Roof', 'Supercharging Included']),
                'image_url': 'https://via.placeholder.com/400x250/FF5722/FFFFFF?text=Tesla+Model+3+2024',
                'available': 1
            },
            {
                'make': 'Nissan', 'model': 'Leaf', 'year': 2024, 'category': 'Electric',
                'daily_price': 52.00, 'passengers': 5, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Electric', 'features': json.dumps(['Air Conditioning', 'Bluetooth', 'Quick Charging', 'ProPILOT Assist']),
                'image_url': 'https://via.placeholder.com/400x250/FF6F00/FFFFFF?text=Nissan+Leaf+2024',
                'available': 1
            },

            # Trucks
            {
                'make': 'Ford', 'model': 'F-150', 'year': 2024, 'category': 'Pickup Truck',
                'daily_price': 78.00, 'passengers': 6, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['4WD', 'Towing Package', 'Bed Liner', 'Bluetooth', 'Backup Camera']),
                'image_url': 'https://via.placeholder.com/400x250/795548/FFFFFF?text=Ford+F-150+2024',
                'available': 1
            },
            {
                'make': 'Chevrolet', 'model': 'Silverado', 'year': 2024, 'category': 'Pickup Truck',
                'daily_price': 76.00, 'passengers': 6, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['4WD', 'Towing Package', 'Apple CarPlay', 'Bluetooth']),
                'image_url': 'https://via.placeholder.com/400x250/6D4C41/FFFFFF?text=Chevy+Silverado+2024',
                'available': 1
            },

            # Sports/Performance
            {
                'make': 'Ford', 'model': 'Mustang', 'year': 2024, 'category': 'Sports',
                'daily_price': 110.00, 'passengers': 4, 'luggage': 2, 'transmission': 'Manual',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Performance Package', 'Premium Sound System', 'Sport Seats', 'Track Apps']),
                'image_url': 'https://via.placeholder.com/400x250/C62828/FFFFFF?text=Ford+Mustang+2024',
                'available': 1
            },
            {
                'make': 'Chevrolet', 'model': 'Camaro', 'year': 2024, 'category': 'Sports',
                'daily_price': 108.00, 'passengers': 4, 'luggage': 2, 'transmission': 'Automatic',
                'fuel_type': 'Gasoline', 'features': json.dumps(['Performance Exhaust', 'Sport Suspension', 'Premium Interior', 'Brembo Brakes']),
                'image_url': 'https://via.placeholder.com/400x250/AD1457/FFFFFF?text=Chevy+Camaro+2024',
                'available': 1
            }
        ]

        for car in cars:
            cursor.execute('''
                INSERT INTO cars (make, model, year, category, daily_price, passengers,
                                luggage, transmission, fuel_type, features, image_url, available)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                car['make'], car['model'], car['year'], car['category'], car['daily_price'],
                car['passengers'], car['luggage'], car['transmission'], car['fuel_type'],
                car['features'], car.get('image_url'), car['available']
            ))

        conn.commit()
        print(f"Database initialized with {len(cars)} cars")

    conn.close()

def get_all_cars():
    """Get all cars from database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cars WHERE available = 1')
    rows = cursor.fetchall()
    conn.close()

    cars = []
    for row in rows:
        car = dict(row)
        car['features'] = json.loads(car['features'])
        cars.append(car)

    return cars

def search_cars(criteria):
    """Search cars based on criteria"""
    conn = get_connection()
    cursor = conn.cursor()

    query = 'SELECT * FROM cars WHERE available = 1'
    params = []

    if criteria.get('max_price'):
        query += ' AND daily_price <= ?'
        params.append(criteria['max_price'])

    if criteria.get('min_passengers'):
        query += ' AND passengers >= ?'
        params.append(criteria['min_passengers'])

    if criteria.get('category'):
        query += ' AND category = ?'
        params.append(criteria['category'])

    if criteria.get('fuel_type'):
        query += ' AND fuel_type = ?'
        params.append(criteria['fuel_type'])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    cars = []
    for row in rows:
        car = dict(row)
        car['features'] = json.loads(car['features'])
        cars.append(car)

    return cars

if __name__ == '__main__':
    # Initialize database when run directly
    init_db()
    print("Database initialized successfully!")
