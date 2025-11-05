"""
Convert car prices from USD to AED (Emirati Dirhams)
Conversion rate: 1 USD = 3.67 AED
"""
import sqlite3

DB_NAME = 'car_rental.db'
USD_TO_AED = 3.67

def convert_prices_to_aed():
    """Convert all car prices from USD to AED"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Get all cars with current USD prices
    cursor.execute('SELECT id, make, model, daily_price FROM cars')
    cars = cursor.fetchall()

    print(f"Converting {len(cars)} car prices from USD to AED...")
    print(f"Conversion rate: 1 USD = {USD_TO_AED} AED\n")

    for car_id, make, model, usd_price in cars:
        aed_price = round(usd_price * USD_TO_AED, 2)
        cursor.execute('UPDATE cars SET daily_price = ? WHERE id = ?', (aed_price, car_id))
        print(f"{make} {model}: ${usd_price:.2f} -> AED {aed_price:.2f}")

    conn.commit()
    conn.close()

    print(f"\nSuccessfully converted all prices to AED!")

if __name__ == '__main__':
    convert_prices_to_aed()
