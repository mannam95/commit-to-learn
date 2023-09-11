import random
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import base64


# Provided data
WeatherConditions = ['sunny', 'rainy', 'fog', 'windy']
MaintenanceAlerts = [1042, 1056, 1078, 1094, 1300, 2465, 3570]
air_levels = ['normal', 'low', 'high', 'flat-tyre']

# Generate synthetic data
num_records = 1000
records = []

background_color = '#F1F1F1'


for _ in range(num_records):
    weather = random.choice(WeatherConditions)
    maintenance_alert = random.choice(MaintenanceAlerts)
    fuel_level = random.randint(0, 100)
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
        # Generate x and y data for the line curve
        x_intervals = list(range(0, 101, 10))
        fuel_levels = [10, 25, 40, 60, 80, 70, 90, 95, 85, 100]

        # Create the line curve
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_intervals, y=fuel_levels, mode='lines+markers', name='Fuel Levels'))

        # Customize the layout
        fig.update_layout(
            xaxis_title='Interval',
            yaxis_title='Fuel Level',
            xaxis=dict(tickvals=x_intervals, title='Fuel Intervals (in %)'),
            yaxis=dict(title='Fuel Level'),
            showlegend=True,
            paper_bgcolor=background_color,  # Set the background color
            plot_bgcolor=background_color  # Set the plot area background color
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
