from playwright.sync_api import sync_playwright
from selectolax.lexbor import LexborHTMLParser
import json, time
import pandas as pd

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




def run(playwright):
    from_place = 'BOM'
    to_place = 'DEL'
    departure_date = '11-30-2023'
    
    parser = get_page(playwright, from_place, to_place, departure_date)
    google_flights_results = extract_flight_data(parser)

    # Convert the data to a DataFrame
    df = pd.DataFrame(google_flights_results)

    # Save the DataFrame to an Excel file
    excel_file_path = 'C:\\Users\\saran\\OneDrive\\Desktop\\mmtscraper\\google_flights_data.xlsx'
    df.to_excel(excel_file_path, index=False)



with sync_playwright() as playwright:
    run(playwright)