import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Initialize SQLite database
conn = sqlite3.connect('flight_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS flights
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              airline TEXT,
              departure_time TEXT,
              arrival_time TEXT,
              price INTEGER)''')
conn.commit()

# Web scraping function
def scrape_flight_data():
    url = 'https://www.makemytrip.com/flight/search?itinerary=DXB-BOM-24/10/2023&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=AE&lang=eng&cmp=SEM|D|DF|G|Brand|Brand-BrandExact_DT|B_M_Makemytrip_Search_Exact|RSA|673383350836'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for flight in soup.find_all('div', {'class': 'flight'}):
        airline = flight.find('span', {'class': 'airline'}).text
        departure_time = flight.find('span', {'class': 'departure-time'}).text
        arrival_time = flight.find('span', {'class': 'arrival-time'}).text
        price = int(flight.find('span', {'class': 'price'}).text[1:])
        
        c.execute("INSERT INTO flights (airline, departure_time, arrival_time, price) VALUES (?, ?, ?, ?)",
                  (airline, departure_time, arrival_time, price))
        conn.commit()

# Scheduler
while True:
    scrape_flight_data()
    time.sleep(3600)  # Sleep for 1 hour