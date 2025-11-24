#!/usr/bin/env python3
"""
Weather CLI - A simple command-line tool to fetch weather data using OpenWeatherMap API.
"""

import argparse
import sys
import os
import requests


class WeatherClient:
    """Client for interacting with OpenWeatherMap API."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    
    def __init__(self, api_key):
        """Initialize the weather client with an API key."""
        self.api_key = api_key
    
    def get_weather(self, city, units="metric"):
        """
        Fetch current weather data for a given city.
        
        Args:
            city (str): Name of the city
            units (str): Units of measurement (metric, imperial, standard)
        
        Returns:
            dict: Weather data from the API
        
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise ValueError("Invalid API key. Please check your OpenWeatherMap API key.")
            elif response.status_code == 404:
                raise ValueError(f"City '{city}' not found. Please check the city name.")
            else:
                raise ValueError(f"HTTP error occurred: {e}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error connecting to OpenWeatherMap API: {e}")


def format_weather_data(data, units="metric"):
    """
    Format weather data for display.
    
    Args:
        data (dict): Weather data from the API
        units (str): Units of measurement
    
    Returns:
        str: Formatted weather information
    """
    # Determine temperature unit symbol
    temp_unit = "°C" if units == "metric" else "°F" if units == "imperial" else "K"
    
    # Extract relevant data
    city_name = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "")
    
    weather_main = data.get("weather", [{}])[0].get("main", "Unknown")
    weather_desc = data.get("weather", [{}])[0].get("description", "Unknown")
    
    main_data = data.get("main", {})
    temp = main_data.get("temp", "N/A")
    feels_like = main_data.get("feels_like", "N/A")
    temp_min = main_data.get("temp_min", "N/A")
    temp_max = main_data.get("temp_max", "N/A")
    humidity = main_data.get("humidity", "N/A")
    pressure = main_data.get("pressure", "N/A")
    
    wind = data.get("wind", {})
    wind_speed = wind.get("speed", "N/A")
    
    # Build formatted output
    output = []
    output.append("=" * 50)
    output.append(f"Weather in {city_name}, {country}")
    output.append("=" * 50)
    output.append(f"Condition: {weather_main} ({weather_desc})")
    output.append(f"Temperature: {temp}{temp_unit}")
    output.append(f"Feels like: {feels_like}{temp_unit}")
    output.append(f"Min/Max: {temp_min}{temp_unit} / {temp_max}{temp_unit}")
    output.append(f"Humidity: {humidity}%")
    output.append(f"Pressure: {pressure} hPa")
    output.append(f"Wind Speed: {wind_speed} m/s" if units == "metric" else f"Wind Speed: {wind_speed} mph")
    output.append("=" * 50)
    
    return "\n".join(output)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Fetch and display weather data from OpenWeatherMap API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s London
  %(prog)s "New York" --units imperial
  %(prog)s Tokyo --api-key YOUR_API_KEY
  
API Key:
  You can provide the API key via:
  - Command line: --api-key YOUR_KEY
  - Environment variable: OPENWEATHER_API_KEY
  
Get your free API key at: https://openweathermap.org/api
        """
    )
    
    parser.add_argument(
        "city",
        help="Name of the city to get weather for"
    )
    
    parser.add_argument(
        "--api-key",
        dest="api_key",
        help="OpenWeatherMap API key (can also use OPENWEATHER_API_KEY env variable)"
    )
    
    parser.add_argument(
        "--units",
        choices=["metric", "imperial", "standard"],
        default="metric",
        help="Units of measurement (default: metric - Celsius, m/s)"
    )
    
    args = parser.parse_args()
    
    # Get API key from command line or environment variable
    api_key = args.api_key or os.environ.get("OPENWEATHER_API_KEY")
    
    if not api_key:
        print("Error: API key is required.", file=sys.stderr)
        print("Provide it via --api-key option or OPENWEATHER_API_KEY environment variable.", file=sys.stderr)
        print("Get your free API key at: https://openweathermap.org/api", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Create weather client and fetch data
        client = WeatherClient(api_key)
        weather_data = client.get_weather(args.city, args.units)
        
        # Format and display weather data
        formatted_output = format_weather_data(weather_data, args.units)
        print(formatted_output)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
