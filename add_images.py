"""
Migration script to add image URLs to existing cars
"""
import sqlite3

DB_NAME = 'car_rental.db'

def add_image_column():
    """Add image_url column to cars table if it doesn't exist"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Try to add the column
        cursor.execute('ALTER TABLE cars ADD COLUMN image_url TEXT')
        print("Added image_url column to cars table")
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("image_url column already exists")
        else:
            raise

    # Generic car images from Unsplash (publicly accessible)
    car_images = {
        'Economy': 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800',
        'Compact SUV': 'https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?w=800',
        'Mid-Size SUV': 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800',
        'Full-Size SUV': 'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800',
        'Luxury': 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800',
        'Minivan': 'https://images.unsplash.com/photo-1464219789935-c2d9d9aba644?w=800',
        'Electric': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800',
        'Pickup Truck': 'https://images.unsplash.com/photo-1533661837699-e5e4a02b6e4e?w=800',
        'Sports': 'https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=800',
    }

    # Update cars with image URLs based on category
    cursor.execute('SELECT id, category FROM cars')
    cars = cursor.fetchall()

    for car_id, category in cars:
        image_url = car_images.get(category, 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800')
        cursor.execute('UPDATE cars SET image_url = ? WHERE id = ?', (image_url, car_id))

    conn.commit()
    print(f"Updated {len(cars)} cars with image URLs")
    conn.close()

if __name__ == '__main__':
    add_image_column()
    print("Migration complete!")
