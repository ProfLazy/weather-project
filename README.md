# weather-project

Small CLI project to fetch current weather for US locations by ZIP code.

Features
- Convert ZIP codes to latitude/longitude using the included data file ([Zip-Code.csv](Zip-Code.csv)).
- Fetch current weather from OpenWeatherMap using an API key.
- Save API key to a local `.env` for future runs.

Requirements
- Python 3.10+ (or your environment's Python)
- Packages: `pandas`, `requests`, optionally `python-dotenv` to load saved API key
    - These can be installed by running `pip install -r requirements.txt`

Usage
- Save an API key:
```sh
python main.py --api-key YOUR_OPENWEATHERMAP_API_KEY
```
This writes `WEATHER_API_KEY` to `.env`.

- Get weather by ZIP code:
```sh
python main.py 27606
```

This is a small learning project created for fun and to learn small things about APIs. 

ZipCode to Lat and Long in uszips.csv :https://simplemaps.com/data/us-zips 