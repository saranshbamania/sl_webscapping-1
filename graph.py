import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

def connecting_flight_graph():
    flight_connections = [{'from_place': 'DEL', 'to_place': 'BOM'}, {'from_place': 'DEL', 'to_place': 'BLR'},
                          {'from_place': 'DEL', 'to_place': 'HYD'}, {'from_place': 'DEL', 'to_place': 'CCU'},
                          {'from_place': 'BOM', 'to_place': 'DEL'}, {'from_place': 'BOM', 'to_place': 'BLR'},
                          {'from_place': 'BOM', 'to_place': 'HYD'}, {'from_place': 'BOM', 'to_place': 'CCU'},
                          {'from_place': 'BLR', 'to_place': 'DEL'}, {'from_place': 'BLR', 'to_place': 'BOM'},
                          {'from_place': 'BLR', 'to_place': 'HYD'}, {'from_place': 'BLR', 'to_place': 'CCU'},
                          {'from_place': 'HYD', 'to_place': 'DEL'}, {'from_place': 'HYD', 'to_place': 'BOM'},
                          {'from_place': 'HYD', 'to_place': 'BLR'}, {'from_place': 'HYD', 'to_place': 'CCU'},
                          {'from_place': 'CCU', 'to_place': 'DEL'}, {'from_place': 'CCU', 'to_place': 'BOM'},
                          {'from_place': 'CCU', 'to_place': 'BLR'}, {'from_place': 'CCU', 'to_place': 'HYD'},
                          {'from_place': 'ATL', 'to_place': 'DFW'}, {'from_place': 'ATL', 'to_place': 'DEN'},
                          {'from_place': 'ATL', 'to_place': 'ORD'}, {'from_place': 'ATL', 'to_place': 'DXB'},
                          {'from_place': 'ATL', 'to_place': 'LAX'}, {'from_place': 'ATL', 'to_place': 'IST'},
                          {'from_place': 'ATL', 'to_place': 'LHR'}, {'from_place': 'ATL', 'to_place': 'DEL'},
                          {'from_place': 'ATL', 'to_place': 'CDG'}, {'from_place': 'ATL', 'to_place': 'JFK'},
                          {'from_place': 'ATL', 'to_place': 'LAS'}, {'from_place': 'DFW', 'to_place': 'ATL'},
                          {'from_place': 'DFW', 'to_place': 'DEN'}, {'from_place': 'DFW', 'to_place': 'ORD'},
                          {'from_place': 'DFW', 'to_place': 'DXB'}, {'from_place': 'DFW', 'to_place': 'LAX'},
                          {'from_place': 'DFW', 'to_place': 'IST'}, {'from_place': 'DFW', 'to_place': 'LHR'},
                          {'from_place': 'DFW', 'to_place': 'DEL'}, {'from_place': 'DFW', 'to_place': 'CDG'},
                          {'from_place': 'DFW', 'to_place': 'JFK'}, {'from_place': 'DFW', 'to_place': 'LAS'},
                          {'from_place': 'DEN', 'to_place': 'ATL'}, {'from_place': 'DEN', 'to_place': 'DFW'},
                          {'from_place': 'DEN', 'to_place': 'ORD'}, {'from_place': 'DEN', 'to_place': 'DXB'},
                          {'from_place': 'DEN', 'to_place': 'LAX'}, {'from_place': 'DEN', 'to_place': 'IST'},
                          {'from_place': 'DEN', 'to_place': 'LHR'}, {'from_place': 'DEN', 'to_place': 'DEL'},
                          {'from_place': 'DEN', 'to_place': 'CDG'}, {'from_place': 'DEN', 'to_place': 'JFK'},
                          {'from_place': 'DEN', 'to_place': 'LAS'}, {'from_place': 'ORD', 'to_place': 'ATL'},
                          {'from_place': 'ORD', 'to_place': 'DFW'}, {'from_place': 'ORD', 'to_place': 'DEN'},
                          {'from_place': 'ORD', 'to_place': 'DXB'}, {'from_place': 'ORD', 'to_place': 'LAX'},
                          {'from_place': 'ORD', 'to_place': 'IST'}, {'from_place': 'ORD', 'to_place': 'LHR'},
                          {'from_place': 'ORD', 'to_place': 'DEL'}, {'from_place': 'ORD', 'to_place': 'CDG'},
                          {'from_place': 'ORD', 'to_place': 'JFK'}, {'from_place': 'ORD', 'to_place': 'LAS'},
                          {'from_place': 'DXB', 'to_place': 'ATL'}, {'from_place': 'DXB', 'to_place': 'DFW'},
                          {'from_place': 'DXB', 'to_place': 'DEN'}, {'from_place': 'DXB', 'to_place': 'ORD'},
                          {'from_place': 'DXB', 'to_place': 'LAX'}, {'from_place': 'DXB', 'to_place': 'IST'},
                          {'from_place': 'DXB', 'to_place': 'LHR'}, {'from_place': 'DXB', 'to_place': 'DEL'},
                          {'from_place': 'DXB', 'to_place': 'CDG'}, {'from_place': 'DXB', 'to_place': 'JFK'},
                          {'from_place': 'DXB', 'to_place': 'LAS'}, {'from_place': 'LAX', 'to_place': 'ATL'},
                          {'from_place': 'LAX', 'to_place': 'DFW'}, {'from_place': 'LAX', 'to_place': 'DEN'},
                          {'from_place': 'LAX', 'to_place': 'ORD'}, {'from_place': 'LAX', 'to_place': 'DXB'},
                          {'from_place': 'LAX', 'to_place': 'IST'}, {'from_place': 'LAX', 'to_place': 'LHR'},
                          {'from_place': 'LAX', 'to_place': 'DEL'}, {'from_place': 'LAX', 'to_place': 'CDG'},
                          {'from_place': 'LAX', 'to_place': 'JFK'}, {'from_place': 'LAX', 'to_place': 'LAS'},
                          {'from_place': 'IST', 'to_place': 'ATL'}, {'from_place': 'IST', 'to_place': 'DFW'},
                          {'from_place': 'IST', 'to_place': 'DEN'}, {'from_place': 'IST', 'to_place': 'ORD'},
                          {'from_place': 'IST', 'to_place': 'DXB'}, {'from_place': 'IST', 'to_place': 'LAX'},
                          {'from_place': 'IST', 'to_place': 'LHR'}, {'from_place': 'IST', 'to_place': 'DEL'},
                          {'from_place': 'IST', 'to_place': 'CDG'}, {'from_place': 'IST', 'to_place': 'JFK'},
                          {'from_place': 'IST', 'to_place': 'LAS'}, {'from_place': 'LHR', 'to_place': 'ATL'},
                          {'from_place': 'LHR', 'to_place': 'DFW'}, {'from_place': 'LHR', 'to_place': 'DEN'},
                          {'from_place': 'LHR', 'to_place': 'ORD'}, {'from_place': 'LHR', 'to_place': 'DXB'},
                          {'from_place': 'LHR', 'to_place': 'LAX'}, {'from_place': 'LHR', 'to_place': 'IST'},
                          {'from_place': 'LHR', 'to_place': 'DEL'}, {'from_place': 'LHR', 'to_place': 'CDG'},
                          {'from_place': 'LHR', 'to_place': 'JFK'}, {'from_place': 'LHR', 'to_place': 'LAS'},
                          {'from_place': 'DEL', 'to_place': 'ATL'}, {'from_place': 'DEL', 'to_place': 'DFW'},
                          {'from_place': 'DEL', 'to_place': 'DEN'}, {'from_place': 'DEL', 'to_place': 'ORD'},
                          {'from_place': 'DEL', 'to_place': 'DXB'}, {'from_place': 'DEL', 'to_place': 'LAX'},
                          {'from_place': 'DEL', 'to_place': 'IST'}, {'from_place': 'DEL', 'to_place': 'LHR'},
                          {'from_place': 'DEL', 'to_place': 'CDG'}, {'from_place': 'DEL', 'to_place': 'JFK'},
                          {'from_place': 'DEL', 'to_place': 'LAS'}, {'from_place': 'CDG', 'to_place': 'ATL'},
                          {'from_place': 'CDG', 'to_place': 'DFW'}, {'from_place': 'CDG', 'to_place': 'DEN'},
                          {'from_place': 'CDG', 'to_place': 'ORD'}, {'from_place': 'CDG', 'to_place': 'DXB'},
                          {'from_place': 'CDG', 'to_place': 'LAX'}, {'from_place': 'CDG', 'to_place': 'IST'},
                          {'from_place': 'CDG', 'to_place': 'LHR'}, {'from_place': 'CDG', 'to_place': 'DEL'},
                          {'from_place': 'CDG', 'to_place': 'JFK'}, {'from_place': 'CDG', 'to_place': 'LAS'},
                          {'from_place': 'JFK', 'to_place': 'ATL'}, {'from_place': 'JFK', 'to_place': 'DFW'},
                          {'from_place': 'JFK', 'to_place': 'DEN'}, {'from_place': 'JFK', 'to_place': 'ORD'},
                          {'from_place': 'JFK', 'to_place': 'DXB'}, {'from_place': 'JFK', 'to_place': 'LAX'},
                          {'from_place': 'JFK', 'to_place': 'IST'}, {'from_place': 'JFK', 'to_place': 'LHR'},
                          {'from_place': 'JFK', 'to_place': 'DEL'}, {'from_place': 'JFK', 'to_place': 'CDG'},
                          {'from_place': 'JFK', 'to_place': 'LAS'}, {'from_place': 'LAS', 'to_place': 'ATL'},
                          {'from_place': 'LAS', 'to_place': 'DFW'}, {'from_place': 'LAS', 'to_place': 'DEN'},
                          {'from_place': 'LAS', 'to_place': 'ORD'}, {'from_place': 'LAS', 'to_place': 'DXB'},
                          {'from_place': 'LAS', 'to_place': 'LAX'}, {'from_place': 'LAS', 'to_place': 'IST'},
                          {'from_place': 'LAS', 'to_place': 'LHR'}, {'from_place': 'LAS', 'to_place': 'DEL'},
                          {'from_place': 'LAS', 'to_place': 'CDG'}, {'from_place': 'LAS', 'to_place': 'JFK'}]

    # Create a DataFrame from the list of dictionaries
    df_connections = pd.DataFrame(flight_connections)

    # Create a directed graph using networkx
    G = nx.from_pandas_edgelist(df_connections, 'from_place', 'to_place', create_using=nx.DiGraph())

    # Draw the network graph
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_size=8, node_size=800, node_color='skyblue', font_color='black',
            font_weight='bold', arrowsize=10)
    plt.title('Flight Connections between Places')
    plt.show()

    # Save the network graph image
    graph_image_path = 'flight_connections_graph.png'
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_size=8, node_size=800, node_color='skyblue', font_color='black',
            font_weight='bold', arrowsize=10)
    plt.title('Flight Connections between Places')
    plt.savefig(graph_image_path, format='png')
    plt.close()


connecting_flight_graph()
def create_flight_connections_graph():
    flight_connections = [{'from_place': 'DEL', 'to_place': 'BOM'}, {'from_place': 'DEL', 'to_place': 'BLR'}, {'from_place': 'DEL', 'to_place': 'HYD'}, {'from_place': 'DEL', 'to_place': 'CCU'}, {'from_place': 'BOM', 'to_place': 'DEL'}, {'from_place': 'BOM', 'to_place': 'BLR'}, {'from_place': 'BOM', 'to_place': 'HYD'}, {'from_place': 'BOM', 'to_place': 'CCU'}, {'from_place': 'BLR', 'to_place': 'DEL'}, {'from_place': 'BLR', 'to_place': 'BOM'}, {'from_place': 'BLR', 'to_place': 'HYD'}, {'from_place': 'BLR', 'to_place': 'CCU'}, {'from_place': 'HYD', 'to_place': 'DEL'}, {'from_place': 'HYD', 'to_place': 'BOM'}, {'from_place': 'HYD', 'to_place': 'BLR'}, {'from_place': 'HYD', 'to_place': 'CCU'}, {'from_place': 'CCU', 'to_place': 'DEL'}, {'from_place': 'CCU', 'to_place': 'BOM'}, {'from_place': 'CCU', 'to_place': 'BLR'}, {'from_place': 'CCU', 'to_place': 'HYD'}, {'from_place': 'ATL', 'to_place': 'DFW'}, {'from_place': 'ATL', 'to_place': 'DEN'}, {'from_place': 'ATL', 'to_place': 'ORD'}, {'from_place': 'ATL', 'to_place': 'DXB'}, {'from_place': 'ATL', 'to_place': 'LAX'}, {'from_place': 'ATL', 'to_place': 'IST'}, {'from_place': 'ATL', 'to_place': 'LHR'}, {'from_place': 'ATL', 'to_place': 'DEL'}, {'from_place': 'ATL', 'to_place': 'CDG'}, {'from_place': 'ATL', 'to_place': 'JFK'}, {'from_place': 'ATL', 'to_place': 'LAS'}, {'from_place': 'DFW', 'to_place': 'ATL'}, {'from_place': 'DFW', 'to_place': 'DEN'}, {'from_place': 'DFW', 'to_place': 'ORD'}, {'from_place': 'DFW', 'to_place': 'DXB'}, {'from_place': 'DFW', 'to_place': 'LAX'}, {'from_place': 'DFW', 'to_place': 'IST'}, {'from_place': 'DFW', 'to_place': 'LHR'}, {'from_place': 'DFW', 'to_place': 'DEL'}, {'from_place': 'DFW', 'to_place': 'CDG'}, {'from_place': 'DFW', 'to_place': 'JFK'}, {'from_place': 'DFW', 'to_place': 'LAS'}, {'from_place': 'DEN', 'to_place': 'ATL'}, {'from_place': 'DEN', 'to_place': 'DFW'}, {'from_place': 'DEN', 'to_place': 'ORD'}, {'from_place': 'DEN', 'to_place': 'DXB'}, {'from_place': 'DEN', 'to_place': 'LAX'}, {'from_place': 'DEN', 'to_place': 'IST'}, {'from_place': 'DEN', 'to_place': 'LHR'}, {'from_place': 'DEN', 'to_place': 'DEL'}, {'from_place': 'DEN', 'to_place': 'CDG'}, 
    ]

    df_connections = pd.DataFrame(flight_connections)
    G = nx.from_pandas_edgelist(df_connections, 'from_place', 'to_place', create_using=nx.DiGraph())
    return G

def load_and_process_flight_data(file_path):
    xls = pd.ExcelFile(file_path)
    
    for sheet_name in xls.sheet_names:
        route_data = pd.read_excel(file_path, sheet_name=sheet_name)

        # Create a folder for each route
        route_folder_path = f'output/{sheet_name}'
        os.makedirs(route_folder_path, exist_ok=True)

        # Call your visualization function with the route data
        visualize_flight_data(route_data, route_folder_path)

        # Add HTML code
        html_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Image Showcase</title>
            <style>
                body {{
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #222; /* Add this line to set the background color to black */
                    color: white; /* Add this line to set the text color to white */
                }}

                img {{
                    max-width: 100%;
                    height: auto;
                    margin: 10px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }}
                p {{
                    text-align: center;
                    font-weight: bold;
            }}
            </style>
        </head>
        <body>
            <div>
                <img src="average_emissions_by_airline.png" alt="Average Emissions by Airline">
                <p style="text-align: center; font-weight: bold;">Average Emissions by Airline</p>
            </div>

            <div>
                <img src="average_prices_by_day.png" alt="Average Prices by Day">
                <p style="text-align: center; font-weight: bold;">Average Prices by Day</p>
            </div>

            <div>
                <img src="bubble_chart.png" alt="Bubble Chart">
                <p style="text-align: center; font-weight: bold;">Bubble Chart</p>
            </div>

            <div>
                <img src="flight_durations_distribution.png" alt="Flight Durations Distribution">
                <p style="text-align: center; font-weight: bold;">Flight Durations Distribution</p>
            </div>

            <div>
                <img src="stops_vs_emissions.png" alt="Stops vs Emissions">
                <p style="text-align: center; font-weight: bold;">Stops vs Emissions</p>
            </div>
        </body>
        </html>
        """

        # Save the HTML file inside the route folder
        html_file_path = f'{route_folder_path}/{sheet_name}_image_showcase.html'
        with open(html_file_path, 'w') as html_file:
            html_file.write(html_code)

def visualize_flight_data(google_flights_df, route_folder_path):
    # Data cleaning and conversion
    google_flights_df['arrival_date'] = google_flights_df['arrival_date'].str.replace('AM\+1', 'AM+1')
    google_flights_df['departure_datetime'] = pd.to_datetime(google_flights_df['departure_date'] + ' ' + google_flights_df['arrival_date'], format='%m-%d-%Y %I:%M %p', errors='coerce')
    google_flights_df['duration_minutes'] = google_flights_df['duration'].apply(lambda x: sum(int(i) * 60 ** j for j, i in enumerate(reversed(x.replace('hr', '').replace('min', '').strip().split()))))
    google_flights_df['emissions_numeric'] = google_flights_df['emissions'].str.extract('(\d+)').astype(float)
    google_flights_df['price'] = google_flights_df['price'].replace('[\₹,]', '', regex=True).astype(float)
    google_flights_df['day_of_week'] = google_flights_df['departure_datetime'].dt.day_name()

    # Visualization 1: Bubble Chart
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(
        google_flights_df['emissions_numeric'],
        google_flights_df['price'],
        s=google_flights_df['duration_minutes'] * 5,
        c=google_flights_df['emissions_numeric'],
        cmap='viridis',
        alpha=0.7
    )
    plt.colorbar(scatter, label='Emissions (kg CO2)')
    plt.title('Bubble Chart: Duration, Emissions, and Price')
    plt.xlabel('Emissions (kg CO2)')
    plt.ylabel('Price (₹)')
    plt.tight_layout()
    plt.grid(True)

    # Save the Bubble Chart
    bubble_chart_path = f'{route_folder_path}/bubble_chart.png'
    plt.savefig(bubble_chart_path, format='png')
    plt.close()

    # Visualization 2: Flight Durations Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(google_flights_df['duration_minutes'], bins=20, kde=True, color='skyblue')
    plt.title('Distribution of Flight Durations')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.grid(True)

    # Save the Flight Durations Distribution
    flight_durations_distribution_path = f'{route_folder_path}/flight_durations_distribution.png'
    plt.savefig(flight_durations_distribution_path, format='png')
    plt.close()

    # Visualization 3: Average Emissions by Airline
    plt.figure(figsize=(12, 8))
    
    ax=sns.barplot(x='company', y='emissions_numeric', data=google_flights_df, ci=None, palette='viridis')
    plt.title('Average Emissions for Different Airlines')
    plt.xlabel('Airline')
    plt.ylabel('Average Emissions (kg CO2)')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
    plt.tight_layout()
    plt.grid(True)

    # Save the Average Emissions by Airline
    average_emissions_by_airline_path = f'{route_folder_path}/average_emissions_by_airline.png'
    plt.savefig(average_emissions_by_airline_path, format='png')
    plt.close()

    # Visualization 4: Relationship between Stops and Emissions
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='stops', y='emissions_numeric', data=google_flights_df, palette='viridis')
    plt.title('Relationship between Stops and Emissions')
    plt.xlabel('Number of Stops')
    plt.ylabel('Emissions (kg CO2)')
    plt.tight_layout()
    plt.grid(True)

    # Save the Relationship between Stops and Emissions
    stops_vs_emissions_path = f'{route_folder_path}/stops_vs_emissions.png'
    plt.savefig(stops_vs_emissions_path, format='png')
    plt.close()

    # Visualization 5: Average Prices by Day of the Week
    average_prices_by_day = google_flights_df.groupby('day_of_week')['price'].mean().sort_values()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=average_prices_by_day.index, y=average_prices_by_day.values, palette='viridis')
    plt.title('Average Prices for Each Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Average Price (₹)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)

    # Save the Average Prices by Day of the Week
    average_prices_by_day_path = f'{route_folder_path}/average_prices_by_day.png'
    plt.savefig(average_prices_by_day_path, format='png')
    plt.close()

# Main script
flight_connections_graph = create_flight_connections_graph()
load_and_process_flight_data('C:\\Users\\saran\\OneDrive\\Desktop\\flight\\google_flights_data.xlsx')


