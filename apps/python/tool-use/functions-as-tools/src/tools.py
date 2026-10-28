from datetime import datetime

import requests


def get_current_time() -> str:
    """
    Returns the current local time as a string.
    """

    return datetime.now().strftime("%H:%M:%S")


def get_weather_from_ip() -> str:
    """
    Gets current, high, and low temperatures in Fahrenheit
    based on the user's approximate IP location.
    """

    # Step 1: Get approximate coordinates from public IP
    location_response = requests.get(
        "https://ipinfo.io/json",
        timeout=10,
    )
    location_response.raise_for_status()

    lat, lon = location_response.json()["loc"].split(",")

    # Step 2: Define Open-Meteo weather parameters
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "timezone": "auto",
    }

    # Step 3: Retrieve weather information
    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params=params,
        timeout=10,
    )
    weather_response.raise_for_status()

    weather_data = weather_response.json()

    # Step 4: Format the result for the LLM
    return (
        f"Current: {weather_data['current']['temperature_2m']}°F, "
        f"High: {weather_data['daily']['temperature_2m_max'][0]}°F, "
        f"Low: {weather_data['daily']['temperature_2m_min'][0]}°F"
    )
