from playwright.sync_api import sync_playwright
from selectolax.lexbor import LexborHTMLParser
import json, time
import pandas as pd
import os
def get_page(playwright, from_place, to_place, departure_date):
    page = playwright.chromium.launch(headless=False).new_page()
    page.goto('https://www.google.com/travel/flights')

    # This clicks on the div that is acting as a dropdown.
    page.click('div[role="combobox"][aria-haspopup="listbox"]')
    time.sleep(1)  # Wait for the dropdown to open

    # Click the "One way" option from the dropdown list
    one_way_option = page.query_selector('text="One way"')
    box = one_way_option.bounding_box()
    page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
    time.sleep(1) 


    # type "From"
    from_place_field = page.query_selector_all('.e5F5td')[0]
    from_place_field.click()
    time.sleep(1)
    from_place_field.type(from_place)
    time.sleep(1)
    page.keyboard.press('Enter')

    # type "To"
    to_place_field = page.query_selector_all('.e5F5td')[1]
    to_place_field.click()
    time.sleep(1)
    to_place_field.type(to_place)
    time.sleep(1)
    page.keyboard.press('Enter')

    departure_date_field = page.query_selector('input[aria-label="Departure"]')
    departure_date_field.click()
    time.sleep(1)  # Use wait_for_function or wait_for_timeout instead
    page.keyboard.type(departure_date)
    time.sleep(1)
    # Click the div with the specified classes
    page.click('div.UGrfjc.hY4LCf')
    time.sleep(1)
    page.query_selector('.WXaAwc .VfPpkd-LgbsSe').click()
    time.sleep(1)

    # press "Explore"
    page.query_selector('.MXvFbd .VfPpkd-LgbsSe').click()
    time.sleep(2)

    # press "More flights"
    page.query_selector('.zISZ5c button').click()
    time.sleep(2)

    #file_path = "C:\\Users\\saran\\OneDrive\\Desktop\\mmtscraper\\scrapper_webpage.html" 
    #html_content=page.content()
    # Writing HTML content to the file
    #with open(file_path, 'w', encoding='utf-8') as file:
    #    file.write(html_content)

    parser = LexborHTMLParser(page.content())
    
    page.close()

    return parser


def extract_flight_data(parser):
    data = []

    categories = parser.css('.zBTtmb')
    category_results = parser.css('.Rk10dc')

    for category, category_result in zip(categories, category_results):
        category_name = category.text().lower().replace(' ', '_')

        for result in category_result.css('.yR1fYc'):
            flight_info = {}

            date = result.css('[jscontroller="cNtv4b"] span')
            flight_info['departure_date'] = date[0].text() if date else None
            flight_info['arrival_date'] = date[1].text() if len(date) > 1 else None

            company = result.css_first('.Ir0Voe .sSHqwe')
            flight_info['company'] = company.text() if company else None

            duration = result.css_first('.AdWm1c.gvkrdb')
            flight_info['duration'] = duration.text() if duration else None

            stops = result.css_first('.EfT7Ae .ogfYpf')
            flight_info['stops'] = stops.text() if stops else None

            emissions = result.css_first('.V1iAHe .AdWm1c')
            flight_info['emissions'] = emissions.text() if emissions else None

            emission_comparison = result.css_first('.N6PNV')
            flight_info['emission_comparison'] = emission_comparison.text() if emission_comparison else None

            price = result.css_first('.U3gSDe .FpEdX span')
            flight_info['price'] = price.text() if price else None

            price_type = result.css_first('.U3gSDe .N872Rd')
            flight_info['price_type'] = price_type.text() if price_type else None

            airports = result.css_first('.Ak5kof .sSHqwe')
            if airports:
                departure_airport = airports.css('span:nth-child(1) .eoY5cb')
                arrival_airport = airports.css('span:nth-child(2) .eoY5cb')
                flight_info['departure_airport'] = departure_airport[0].text() if departure_airport else None
                flight_info['arrival_airport'] = arrival_airport[0].text() if arrival_airport else None

            service = result.css_first('.hRBhge')
            flight_info['service'] = service.text() if service else None

            data.append(flight_info)

    return data


def run(playwright, from_place, to_place, start_date, end_date):
    date_range = pd.date_range(start_date, end_date).strftime('%m-%d-%Y')
    all_data_df = pd.DataFrame()

    for departure_date in date_range:
        print(f"Processing {from_place} to {to_place} for {departure_date}...")

        parser = get_page(playwright, from_place, to_place, departure_date)
        google_flights_results = extract_flight_data(parser)

        # Convert the data to a DataFrame
        df = pd.DataFrame(google_flights_results)

        # Add route information and departure date to the DataFrame
        df['from_place'] = from_place
        df['to_place'] = to_place
        df['departure_date'] = departure_date

        # Concatenate the DataFrame to the overall DataFrame
        all_data_df = pd.concat([all_data_df, df], ignore_index=True)

    return all_data_df

def main():
    routes = [
    {'from_place': 'DEL', 'to_place': 'BOM'},
    {'from_place': 'DEL', 'to_place': 'BLR'},
    {'from_place': 'DEL', 'to_place': 'HYD'},
    {'from_place': 'DEL', 'to_place': 'CCU'},
    {'from_place': 'BOM', 'to_place': 'DEL'},
    {'from_place': 'BOM', 'to_place': 'BLR'},
    {'from_place': 'BOM', 'to_place': 'HYD'},
    {'from_place': 'BOM', 'to_place': 'CCU'},
    {'from_place': 'BLR', 'to_place': 'DEL'},
    {'from_place': 'BLR', 'to_place': 'BOM'},
    {'from_place': 'BLR', 'to_place': 'HYD'},
    {'from_place': 'BLR', 'to_place': 'CCU'},
    {'from_place': 'HYD', 'to_place': 'DEL'},
    {'from_place': 'HYD', 'to_place': 'BOM'},
    {'from_place': 'HYD', 'to_place': 'BLR'},
    {'from_place': 'HYD', 'to_place': 'CCU'},
    {'from_place': 'CCU', 'to_place': 'DEL'},
    {'from_place': 'CCU', 'to_place': 'BOM'},
    {'from_place': 'CCU', 'to_place': 'BLR'},
    {'from_place': 'CCU', 'to_place': 'HYD'},
    {'from_place': 'ATL', 'to_place': 'DFW'},
    {'from_place': 'ATL', 'to_place': 'DEN'},
    {'from_place': 'ATL', 'to_place': 'ORD'},
    {'from_place': 'ATL', 'to_place': 'DXB'},
    {'from_place': 'ATL', 'to_place': 'LAX'},
    {'from_place': 'ATL', 'to_place': 'IST'},
    {'from_place': 'ATL', 'to_place': 'LHR'},
    {'from_place': 'ATL', 'to_place': 'DEL'},
    {'from_place': 'ATL', 'to_place': 'CDG'},
    {'from_place': 'ATL', 'to_place': 'JFK'},
    {'from_place': 'ATL', 'to_place': 'LAS'},
    {'from_place': 'DFW', 'to_place': 'ATL'},
    {'from_place': 'DFW', 'to_place': 'DEN'},
    {'from_place': 'DFW', 'to_place': 'ORD'},
    {'from_place': 'DFW', 'to_place': 'DXB'},
    {'from_place': 'DFW', 'to_place': 'LAX'},
    {'from_place': 'DFW', 'to_place': 'IST'},
    {'from_place': 'DFW', 'to_place': 'LHR'},
    {'from_place': 'DFW', 'to_place': 'DEL'},
    {'from_place': 'DFW', 'to_place': 'CDG'},
    {'from_place': 'DFW', 'to_place': 'JFK'},
    {'from_place': 'DFW', 'to_place': 'LAS'},
    {'from_place': 'DEN', 'to_place': 'ATL'},
    {'from_place': 'DEN', 'to_place': 'DFW'},
    {'from_place': 'DEN', 'to_place': 'ORD'},
    {'from_place': 'DEN', 'to_place': 'DXB'},
    {'from_place': 'DEN', 'to_place': 'LAX'},
    {'from_place': 'DEN', 'to_place': 'IST'},
    {'from_place': 'DEN', 'to_place': 'LHR'},
    {'from_place': 'DEN', 'to_place': 'DEL'},
    {'from_place': 'DEN', 'to_place': 'CDG'},
    {'from_place': 'DEN', 'to_place': 'JFK'},
    {'from_place': 'DEN', 'to_place': 'LAS'},
    {'from_place': 'ORD', 'to_place': 'ATL'},
    {'from_place': 'ORD', 'to_place': 'DFW'},
    {'from_place': 'ORD', 'to_place': 'DEN'},
    {'from_place': 'ORD', 'to_place': 'DXB'},
    {'from_place': 'ORD', 'to_place': 'LAX'},
    {'from_place': 'ORD', 'to_place': 'IST'},
    {'from_place': 'ORD', 'to_place': 'LHR'},
    {'from_place': 'ORD', 'to_place': 'DEL'},
    {'from_place': 'ORD', 'to_place': 'CDG'},
    {'from_place': 'ORD', 'to_place': 'JFK'},
    {'from_place': 'ORD', 'to_place': 'LAS'},
    {'from_place': 'DXB', 'to_place': 'ATL'},
    {'from_place': 'DXB', 'to_place': 'DFW'},
    {'from_place': 'DXB', 'to_place': 'DEN'},
    {'from_place': 'DXB', 'to_place': 'ORD'},
    {'from_place': 'DXB', 'to_place': 'LAX'},
    {'from_place': 'DXB', 'to_place': 'IST'},
    {'from_place': 'DXB', 'to_place': 'LHR'},
    {'from_place': 'DXB', 'to_place': 'DEL'},
    {'from_place': 'DXB', 'to_place': 'CDG'},
    {'from_place': 'DXB', 'to_place': 'JFK'},
    {'from_place': 'DXB', 'to_place': 'LAS'},
    {'from_place': 'LAX', 'to_place': 'ATL'},
    {'from_place': 'LAX', 'to_place': 'DFW'},
    {'from_place': 'LAX', 'to_place': 'DEN'},
    {'from_place': 'LAX', 'to_place': 'ORD'},
    {'from_place': 'LAX', 'to_place': 'DXB'},
    {'from_place': 'LAX', 'to_place': 'IST'},
    {'from_place': 'LAX', 'to_place': 'LHR'},
    {'from_place': 'LAX', 'to_place': 'DEL'},
    {'from_place': 'LAX', 'to_place': 'CDG'},
    {'from_place': 'LAX', 'to_place': 'JFK'},
    {'from_place': 'LAX', 'to_place': 'LAS'},
    {'from_place': 'IST', 'to_place': 'ATL'},
    {'from_place': 'IST', 'to_place': 'DFW'},
    {'from_place': 'IST', 'to_place': 'DEN'},
    {'from_place': 'IST', 'to_place': 'ORD'},
    {'from_place': 'IST', 'to_place': 'DXB'},
    {'from_place': 'IST', 'to_place': 'LAX'},
    {'from_place': 'IST', 'to_place': 'LHR'},
    {'from_place': 'IST', 'to_place': 'DEL'},
    {'from_place': 'IST', 'to_place': 'CDG'},
    {'from_place': 'IST', 'to_place': 'JFK'},
    {'from_place': 'IST', 'to_place': 'LAS'},
    {'from_place': 'LHR', 'to_place': 'ATL'},
    {'from_place': 'LHR', 'to_place': 'DFW'},
    {'from_place': 'LHR', 'to_place': 'DEN'},
    {'from_place': 'LHR', 'to_place': 'ORD'},
    {'from_place': 'LHR', 'to_place': 'DXB'},
    {'from_place': 'LHR', 'to_place': 'LAX'},
    {'from_place': 'LHR', 'to_place': 'IST'},
    {'from_place': 'LHR', 'to_place': 'DEL'},
    {'from_place': 'LHR', 'to_place': 'CDG'},
    {'from_place': 'LHR', 'to_place': 'JFK'},
    {'from_place': 'LHR', 'to_place': 'LAS'},
    {'from_place': 'DEL', 'to_place': 'ATL'},
    {'from_place': 'DEL', 'to_place': 'DFW'},
    {'from_place': 'DEL', 'to_place': 'DEN'},
    {'from_place': 'DEL', 'to_place': 'ORD'},
    {'from_place': 'DEL', 'to_place': 'DXB'},
    {'from_place': 'DEL', 'to_place': 'LAX'},
    {'from_place': 'DEL', 'to_place': 'IST'},
    {'from_place': 'DEL', 'to_place': 'LHR'},
    {'from_place': 'DEL', 'to_place': 'CDG'},
    {'from_place': 'DEL', 'to_place': 'JFK'},
    {'from_place': 'DEL', 'to_place': 'LAS'},
    {'from_place': 'CDG', 'to_place': 'ATL'},
    {'from_place': 'CDG', 'to_place': 'DFW'},
    {'from_place': 'CDG', 'to_place': 'DEN'},
    {'from_place': 'CDG', 'to_place': 'ORD'},
    {'from_place': 'CDG', 'to_place': 'DXB'},
    {'from_place': 'CDG', 'to_place': 'LAX'},
    {'from_place': 'CDG', 'to_place': 'IST'},
    {'from_place': 'CDG', 'to_place': 'LHR'},
    {'from_place': 'CDG', 'to_place': 'DEL'},
    {'from_place': 'CDG', 'to_place': 'JFK'},
    {'from_place': 'CDG', 'to_place': 'LAS'},
    {'from_place': 'JFK', 'to_place': 'ATL'},
    {'from_place': 'JFK', 'to_place': 'DFW'},
    {'from_place': 'JFK', 'to_place': 'DEN'},
    {'from_place': 'JFK', 'to_place': 'ORD'},
    {'from_place': 'JFK', 'to_place': 'DXB'},
    {'from_place': 'JFK', 'to_place': 'LAX'},
    {'from_place': 'JFK', 'to_place': 'IST'},
    {'from_place': 'JFK', 'to_place': 'LHR'},
    {'from_place': 'JFK', 'to_place': 'DEL'},
    {'from_place': 'JFK', 'to_place': 'CDG'},
    {'from_place': 'JFK', 'to_place': 'LAS'}
]

    start_date = '2023-11-30'
    end_date = '2023-12-1'

    excel_file_path = 'C:\\Users\\saran\\OneDrive\\Desktop\\mmtscraper\\google_flights_data.xlsx'

    # Check if the file exists
    if not os.path.exists(excel_file_path):
        # Create a new file with headers
        with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
            pd.DataFrame().to_excel(writer, index=False)

    for route in routes:
        from_place = route['from_place']
        to_place = route['to_place']

        # Run the script for each route
        with sync_playwright() as playwright:
            data_df = run(playwright, from_place, to_place, start_date, end_date)

        # Save the data to Excel with a sheet for each route
        with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a') as writer:
            data_df.to_excel(writer, index=False, sheet_name=f'{from_place}_{to_place}')

if __name__ == "__main__":
    main()