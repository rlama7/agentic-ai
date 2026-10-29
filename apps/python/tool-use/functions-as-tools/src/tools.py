from datetime import datetime
from pathlib import Path

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


def write_txt_file(file_path: str, content: str) -> str:
    """
    Write text content to a .txt file in the output directory.

    Args:
        file_path: Filename for the text file.
        content: Text to write into the file.

    Returns:
        Path to the saved text file.
    """

    # Define the allowed output directory
    output_dir = Path(__file__).resolve().parent.parent / "output"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Accept filenames only, not arbitrary paths
    if not file_path or Path(file_path).name != file_path:
        raise ValueError("Only filenames are allowed.")

    # Require a .txt extension
    if not file_path.endswith(".txt"):
        raise ValueError("Filename must end with .txt")

    # Construct the destination path
    destination = output_dir / file_path

    # Write content using UTF-8 encoding
    destination.write_text(content, encoding="utf-8")

    # Return the saved path
    return str(destination)
