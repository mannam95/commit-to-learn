import random
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import base64
import numpy as np


# Provided data
WeatherConditions = ['sunny', 'rainy', 'fog', 'windy']
MaintenanceAlerts = [1042, 1056, 1078, 1094, 1300, 2465, 3570]
air_levels = ['normal', 'low', 'high', 'flat-tyre']

# Generate synthetic data
num_records = 1000
records = []

background_color = '#F1F1F1'

fuel_data = np.random.normal(50, 15, 1000)  # Mean=50, Standard Deviation=15, 1000 data points


for _ in range(num_records):
    weather = random.choice(WeatherConditions)
    maintenance_alert = random.choice(MaintenanceAlerts)
    fuel_level = random.randint(10, 100)
    air_level = random.choice(air_levels)
    
    records.append([weather, maintenance_alert, fuel_level, air_level])


# Get the weather conditions
def get_weather_conditions():
    try:
        weather_counts = {weather: 0 for weather in WeatherConditions}
        for record in records:
            weather_counts[record[0]] += 1

        # Create a bar chart with Plotly
        fig = px.bar(x=weather_counts.keys(), y=list(weather_counts.values()))
        fig.update_layout(
            xaxis_title='Weather Conditions',
            yaxis_title='Count',
            paper_bgcolor=background_color,  # Set the background color
            plot_bgcolor=background_color  # Set the plot area background color
        )

        # Export the plot as an image in base64 format
        img_bytes = pio.to_image(fig, format="png")
        base64_image = base64.b64encode(img_bytes).decode()

        return base64_image
    except:
        return ['empty_list']


# Get the maintenance alerts
def get_maintenance_alerts():
    try:
        maintenance_alert_counts = {str(alert): 0 for alert in MaintenanceAlerts}
        for record in records:
            maintenance_alert_counts[str(record[1])] += 1

        # Create a bar chart with Plotly
        fig = px.bar(x=maintenance_alert_counts.keys(), y=list(maintenance_alert_counts.values()))
        fig.update_layout(
            xaxis_title='Maintenance Alerts',
            yaxis_title='Count',
            paper_bgcolor=background_color,  # Set the background color
            plot_bgcolor=background_color  # Set the plot area background color
        )

        # Export the plot as an image in base64 format
        img_bytes = pio.to_image(fig, format="png")
        base64_image = base64.b64encode(img_bytes).decode()

        return base64_image
    except:
        return ['empty_list']


# Get the Air Levels stats
def get_air_levels():
    try:
        air_level_counts = {air_level: 0 for air_level in air_levels}
        for record in records:
            air_level_counts[record[3]] += 1

        # Create a pie chart with Plotly
        fig = px.pie(values=list(air_level_counts.values()), names=list(air_level_counts.keys()))
        fig.update_layout(
            paper_bgcolor=background_color,  # Set the background color
            plot_bgcolor=background_color  # Set the plot area background color
        )

        # Export the plot as an image in base64 format
        img_bytes = pio.to_image(fig, format="png")
        base64_image = base64.b64encode(img_bytes).decode()

        return base64_image
    except:
        return ['empty_list']
    

# Get fuel level stats
def get_fuel_levels():
    try:
        # Create a histogram
        fig = px.histogram(fuel_data, nbins=30, histnorm='probability density')

        # Overlay a normal distribution curve
        x = np.linspace(min(fuel_data), max(fuel_data), 100)
        y = (1 / (15 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - 50) / 15) ** 2)
        fig.add_scatter(x=x, y=y, mode='lines', name='Distribution Line')

        # Update axis labels and title
        fig.update_layout(
            xaxis_title="Fuel Range",
            yaxis_title="Probability Density",
            showlegend=False,
            paper_bgcolor=background_color,  # Set the background color
            plot_bgcolor=background_color 
        )

        # Export the plot as an image in base64 format
        img_bytes = pio.to_image(fig, format="png")
        base64_image = base64.b64encode(img_bytes).decode()

        return base64_image

    except:
        return ['empty_list']



def get_dashboard_stats():
    try:
        return {
            'weather_stats': get_weather_conditions(),
            'maintenance_alert_stats': get_maintenance_alerts(),
            'air_level_stats': get_air_levels(),
            'fuel_level_stats': get_fuel_levels()
        }
    except:
        return ['empty_list']
