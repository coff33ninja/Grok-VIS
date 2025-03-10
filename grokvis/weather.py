"""
Weather service functionality for GrokVIS.
Handles fetching and reporting weather information.
"""
import logging
import requests

# Import from core module
from grokvis.core import executor
from grokvis.speech import speak

def fetch_weather(city):
    """Fetch weather data synchronously for threading."""
    api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    return response['main']['temp'], response['weather'][0]['description']

def get_weather(city):
    """Fetch and announce weather asynchronously."""
    try:
        future = executor.submit(fetch_weather, city)
        temp, desc = future.result()
        speak(f"{city}: {temp}°C, {desc}.")
        return {"temp": temp, "desc": desc}
    except Exception as e:
        logging.error(f"Weather API Error: {e}")
        speak("Sorry, I couldn't fetch the weather.")

def get_forecast(city, days=5):
    """Get a multi-day weather forecast."""
    try:
        api_key = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt={days*8}"
        response = requests.get(url).json()
        
        # Process the forecast data (every 3 hours for 5 days)
        daily_forecasts = {}
        
        for item in response['list']:
            date = item['dt_txt'].split(' ')[0]
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    'temps': [],
                    'descriptions': []
                }
            
            daily_forecasts[date]['temps'].append(item['main']['temp'])
            daily_forecasts[date]['descriptions'].append(item['weather'][0]['description'])
        
        # Summarize the forecast for each day
        speak(f"Weather forecast for {city}:")
        for date, data in daily_forecasts.items():
            avg_temp = sum(data['temps']) / len(data['temps'])
            # Get the most common description
            common_desc = max(set(data['descriptions']), key=data['descriptions'].count)
            speak(f"{date}: Average {avg_temp:.1f}°C, {common_desc}")
            
        return daily_forecasts
    except Exception as e:
        logging.error(f"Forecast API Error: {e}")
        speak("Sorry, I couldn't fetch the forecast.")
        return None