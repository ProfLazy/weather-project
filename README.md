# Weather CLI Project

A Python command-line interface (CLI) tool that fetches and displays current weather data using the OpenWeatherMap API.

## Features

- Fetch current weather data for any city worldwide
- Display temperature, weather conditions, humidity, pressure, and wind speed
- Support for multiple unit systems (Metric, Imperial, Standard)
- Clean, formatted output
- Error handling for invalid cities and API issues

## Prerequisites

- Python 3.6 or higher
- OpenWeatherMap API key (free tier available)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ProfLazy/weather-project.git
cd weather-project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)

## Usage

### Basic Usage

```bash
python weather_cli.py "City Name" --api-key YOUR_API_KEY
```

### Using Environment Variable

Set the API key as an environment variable:
```bash
export OPENWEATHER_API_KEY=your_api_key_here
python weather_cli.py London
```

### Examples

Get weather in metric units (Celsius, m/s):
```bash
python weather_cli.py London --api-key YOUR_API_KEY
```

Get weather in imperial units (Fahrenheit, mph):
```bash
python weather_cli.py "New York" --units imperial --api-key YOUR_API_KEY
```

Get weather using environment variable for API key:
```bash
export OPENWEATHER_API_KEY=your_api_key_here
python weather_cli.py Tokyo
python weather_cli.py Paris --units metric
```

### Command-Line Options

```
positional arguments:
  city                  Name of the city to get weather for

optional arguments:
  -h, --help           Show help message and exit
  --api-key API_KEY    OpenWeatherMap API key
  --units {metric,imperial,standard}
                       Units of measurement (default: metric)
                       - metric: Celsius, m/s
                       - imperial: Fahrenheit, mph
                       - standard: Kelvin, m/s
```

## Example Output

```
==================================================
Weather in London, GB
==================================================
Condition: Clouds (overcast clouds)
Temperature: 12.5°C
Feels like: 11.8°C
Min/Max: 11.2°C / 13.7°C
Humidity: 82%
Pressure: 1012 hPa
Wind Speed: 3.5 m/s
==================================================
```

## API Key

You can provide your OpenWeatherMap API key in two ways:

1. **Command-line argument**: `--api-key YOUR_KEY`
2. **Environment variable**: `OPENWEATHER_API_KEY`

To get a free API key:
1. Visit [OpenWeatherMap API](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key from your account dashboard

## Error Handling

The application handles various error scenarios:
- Missing or invalid API key
- City not found
- Network connection issues
- API rate limits
- Invalid input

## License

This project is open source and available for educational purposes.
