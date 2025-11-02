"""
Migration script to add image URLs to existing cars in the database.
Run this once to update the database with image URLs.
"""
import sqlite3

DB_NAME = 'car_rental.db'

# Map of car identities to their image URLs
car_images = {
    ('Toyota', 'Corolla', 2024): 'https://via.placeholder.com/400x250/4A90E2/FFFFFF?text=Toyota+Corolla+2024',
    ('Honda', 'Civic', 2024): 'https://via.placeholder.com/400x250/5C6BC0/FFFFFF?text=Honda+Civic+2024',
    ('Hyundai', 'Elantra', 2023): 'https://via.placeholder.com/400x250/42A5F5/FFFFFF?text=Hyundai+Elantra+2023',
    ('Mazda', 'CX-5', 2024): 'https://via.placeholder.com/400x250/7E57C2/FFFFFF?text=Mazda+CX-5+2024',
    ('Honda', 'CR-V', 2024): 'https://via.placeholder.com/400x250/AB47BC/FFFFFF?text=Honda+CR-V+2024',
    ('Toyota', 'RAV4', 2023): 'https://via.placeholder.com/400x250/8E24AA/FFFFFF?text=Toyota+RAV4+2023',
    ('Chevrolet', 'Tahoe', 2024): 'https://via.placeholder.com/400x250/EF5350/FFFFFF?text=Chevrolet+Tahoe+2024',
    ('Ford', 'Explorer', 2024): 'https://via.placeholder.com/400x250/E53935/FFFFFF?text=Ford+Explorer+2024',
    ('BMW', '3 Series', 2024): 'https://via.placeholder.com/400x250/212121/FFFFFF?text=BMW+3+Series+2024',
    ('Mercedes-Benz', 'C-Class', 2024): 'https://via.placeholder.com/400x250/424242/FFFFFF?text=Mercedes+C-Class+2024',
    ('Audi', 'A4', 2023): 'https://via.placeholder.com/400x250/616161/FFFFFF?text=Audi+A4+2023',
    ('Chrysler', 'Pacifica', 2024): 'https://via.placeholder.com/400x250/26A69A/FFFFFF?text=Chrysler+Pacifica+2024',
    ('Honda', 'Odyssey', 2024): 'https://via.placeholder.com/400x250/00897B/FFFFFF?text=Honda+Odyssey+2024',
    ('Tesla', 'Model 3', 2024): 'https://via.placeholder.com/400x250/FF5722/FFFFFF?text=Tesla+Model+3+2024',
    ('Nissan', 'Leaf', 2024): 'https://via.placeholder.com/400x250/FF6F00/FFFFFF?text=Nissan+Leaf+2024',
    ('Ford', 'F-150', 2024): 'https://via.placeholder.com/400x250/795548/FFFFFF?text=Ford+F-150+2024',
    ('Chevrolet', 'Silverado', 2024): 'https://via.placeholder.com/400x250/6D4C41/FFFFFF?text=Chevy+Silverado+2024',
    ('Ford', 'Mustang', 2024): 'https://via.placeholder.com/400x250/C62828/FFFFFF?text=Ford+Mustang+2024',
    ('Chevrolet', 'Camaro', 2024): 'https://via.placeholder.com/400x250/AD1457/FFFFFF?text=Chevy+Camaro+2024',
}

def migrate():
    """Add image URLs to existing cars"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    updated = 0
    for (make, model, year), image_url in car_images.items():
        cursor.execute('''
            UPDATE cars
            SET image_url = ?
            WHERE make = ? AND model = ? AND year = ?
        ''', (image_url, make, model, year))
        updated += cursor.rowcount

    conn.commit()
    conn.close()

    print(f"Migration complete! Updated {updated} cars with image URLs.")

if __name__ == '__main__':
    migrate()
