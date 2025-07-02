import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuration
API_KEY = "e0bae8ca40b02bce4c677be7ff675e87"  # Your OpenWeatherMap API key
CITY = "London"  # Change to any valid city name
UNITS = "metric"  # metric for Celsius, imperial for Fahrenheit

def get_weather_data():
    """Fetch current weather and 5-day forecast from OpenWeatherMap API"""
    base_url = "https://api.openweathermap.org/data/2.5/"
    
    # Current weather data
    current_url = f"{base_url}weather?q={CITY}&appid={API_KEY}&units={UNITS}"
    current_response = requests.get(current_url).json()
    
    # Forecast data
    forecast_url = f"{base_url}forecast?q={CITY}&appid={API_KEY}&units={UNITS}"
    forecast_response = requests.get(forecast_url).json()
    
    # Debugging output
    print("Current Weather Response:", current_response)
    print("Forecast Response:", forecast_response)
    
    return current_response, forecast_response

def process_forecast_data(forecast_data):
    """Process forecast data into a pandas DataFrame"""
    if 'list' not in forecast_data:
        raise ValueError("Forecast data does not contain 'list' key.")
    
    forecast_list = []
    
    for forecast in forecast_data['list']:
        timestamp = datetime.fromtimestamp(forecast['dt'])
        forecast_list.append({
            'datetime': timestamp,
            'date': timestamp.date(),
            'time': timestamp.time(),
            'temp': forecast['main']['temp'],
            'temp_min': forecast['main']['temp_min'],
            'temp_max': forecast['main']['temp_max'],
            'humidity': forecast['main']['humidity'],
            'wind_speed': forecast['wind']['speed'],
            'weather': forecast['weather'][0]['main'],
            'weather_desc': forecast['weather'][0]['description']
        })
    
    return pd.DataFrame(forecast_list)

def create_dashboard(current_data, forecast_df):
    """Create a weather visualization dashboard"""
    
    # Set Seaborn style
    sns.set_style("darkgrid")
    plt.figure(figsize=(16, 12))
    
    # Dashboard title
    plt.suptitle(f"Weather Dashboard for {CITY}", fontsize=16, y=1.02)
    
    # GridSpec for custom layouts
    gs = plt.GridSpec(3, 2, height_ratios=[1, 1, 1])
    
    # PLOT 1: Temperature Trend
    plt.subplot(gs[0, 0])
    sns.lineplot(data=forecast_df, x='datetime', y='temp', marker='o')
    plt.title("Temperature Trend (3-hour intervals)")
    plt.xlabel("Date & Time")
    plt.ylabel(f"Temperature (°{'C' if UNITS=='metric' else 'F'})")
    
    # PLOT 2: Daily Temperature Ranges
    plt.subplot(gs[0, 1])
    daily_stats = forecast_df.groupby('date').agg({'temp': ['min', 'max', 'mean']})
    daily_stats.columns = ['min_temp', 'max_temp', 'mean_temp']
    plt.bar(daily_stats.index.astype(str), 
            daily_stats['max_temp'] - daily_stats['min_temp'],
            bottom=daily_stats['min_temp'])
    plt.title("Daily Temperature Ranges")
    plt.xlabel("Date")
    plt.ylabel(f"Temperature (°{'C' if UNITS=='metric' else 'F'})")
    
    # PLOT 3: Humidity Trend
    plt.subplot(gs[1, 0])
    sns.lineplot(data=forecast_df, x='datetime', y='humidity', marker='o')
    plt.title("Humidity Trend")
    plt.xlabel("Date & Time")
    plt.ylabel("Humidity (%)")
    
    # PLOT 4: Weather Condition Distribution
    plt.subplot(gs[1, 1])
    weather_counts = forecast_df['weather'].value_counts()
    plt.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%')
    plt.title("Weather Conditions Distribution")
    
    # PLOT 5: Current Weather Summary (text)
    plt.subplot(gs[2, :])
    plt.axis('off')
    
    current_summary = [
        "CURRENT WEATHER SUMMARY",
        f"City: {CITY}",
        f"Temperature: {current_data['main']['temp']}°{'C' if UNITS=='metric' else 'F'}",
        f"Feels Like: {current_data['main']['feels_like']}°{'C' if UNITS=='metric' else 'F'}",
        f"Humidity: {current_data['main']['humidity']}%",
        f"Wind Speed: {current_data['wind']['speed']} m/s",
        f"Pressure: {current_data['main']['pressure']} hPa",
        f"Weather: {current_data['weather'][0]['main']} ({current_data['weather'][0]['description']})",
        f"Sunrise: {datetime.fromtimestamp(current_data['sys']['sunrise']).strftime('%H:%M:%S')}",
        f"Sunset: {datetime.fromtimestamp(current_data['sys']['sunset']).strftime('%H:%M:%S')}",
        f"Last Updated: {datetime.fromtimestamp(current_data['dt']).strftime('%Y-%m-%d %H:%M:%S')}"
    ]
    
    plt.text(0.1, 0.5, '\n'.join(current_summary), fontsize=11, 
             bbox=dict(facecolor='lightblue', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('weather_dashboard.png')
    plt.show()

def main():
    try:
        print("Fetching weather data...")
        current_data, forecast_data = get_weather_data()
        
        print("Processing forecast data...")
        forecast_df = process_forecast_data(forecast_data)
        
        print("Creating dashboard...")
        create_dashboard(current_data, forecast_df)
        
        print("Dashboard saved as weather_dashboard.png")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()


