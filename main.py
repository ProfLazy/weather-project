import sys
import pandas as pd
import requests 

fake_args_for_api_key = ["--api-key", "your_api_key_here"]
fake_args_for_help1 = ["--help"]
fake_args_for_help2 = ["-h"]

def main():
    # sys.argv is a list: [program_name, arg1, arg2, ...]
    # This takes the first element as the program name and takes it out of the buffer
    program_name = sys.argv[0]
    
    # All arguments after the program name
    # Needs a max of 2 args for either ZipCode or --api-key KEY
    args = sys.argv[1:]

    # Debug: Using fake args for API key testing
    # args = fake_args_for_api_key

    # Debug: Using fake args for help testing
    # args = fake_args_for_help1
    # args = fake_args_for_help2

    # debug: Using fake args for ZipCode testing
    # args = ["28277"]

    # debug: Using fake args for ZipCode testing
    # args = ["27606"]

    # Debug: using an incorrect zipcode
    # args = ["99999"]


    # Handle help flag
    if not args or args[0] in ("-h", "--help"):
        help()
        return

    # If args is larger than 2, truncate it and ask the user if they meant to say the first two only
    if len(args) > 2:
        print("Warning: More than 2 arguments provided. Using only the first two.")
        args = args[:2]

    # Example: handle no args
    if not args:
        print("No arguments provided!")
        return
    
    # Handle API key input
    currKey = handle_api_key_input(args)

    if currKey is None:
        return

    # Handle ZipCode input
    if args[0] == "--api-key":
        return
    
    lat_long_id_state = handle_zipcode_input(args)

    print_weather_info(lat_long_id_state[0], lat_long_id_state[1], lat_long_id_state[2], lat_long_id_state[3], currKey)

def print_weather_info(lat, lng, state, state_id, api_key):
    # This method will fetch and print the weather information for the given latitude and longitude
    # using the provided API key

    # Example API endpoint (replace with actual weather API endpoint)
    api_endpoint = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}"

    # Make a GET request to the weather API
    response = requests.get(api_endpoint)

    # Check if the request was successful
    if response.status_code == 200:
        weather_data = response.json()

        temp_to_fahrenheit = (weather_data['main']['temp'] - 273.15) * 9/5 + 32

        print("----- Weather Information -----")
        print(f"Current weather at ({lat}, {lng}):")
        print(f"Temperature: {temp_to_fahrenheit:.2f} °F")
        print(f"Condition: {weather_data['weather'][0]['description']}")
        print(f"State: {state} (ID: {state_id})")
    else:
        print(f"Error fetching weather data: {response.status_code} - {response.text}")
        print("Please check your API key. An invalid API key can lead to authentication errors.")



def handle_api_key_input(args):
    # This method will check if the user provided an API key via command line arguments
    # If so, it will save it to a .env file for future use
    # If not, it will tell the user to provide one

    # Initialize api_key variable
    api_key = None

    # Check if the first argument is --api-key
    # if so, validate and save the key
    if args[0] == "--api-key":
        
        # Check for too few arguments
        if len(args) < 2:
            print("Error: --api-key flag provided but no key found.")
            return
        
        # Check for too many arguments
        if len(args) > 2:
            print("Error: Too many arguments provided with --api-key flag.")
            return
        
        # Extract the API key from the arguments
        api_key = args[1]
        print(f"API Key provided: {api_key}")
        save_api_key_to_env(api_key)
    
    if api_key is None:
        try :
            from dotenv import load_dotenv
            import os

            load_dotenv()
            api_key = os.getenv("WEATHER_API_KEY")

            if api_key is None:
                print("Error: No API key provided and none found in .env file.")
                print("Please provide an API key using --api-key flag.")
                return
            else:
                print("API key loaded from .env file.")
        except ImportError:
            print("Error: python-dotenv package not installed. Please provide an API key using --api-key flag.")

    return api_key

def save_api_key_to_env(api_key: str):
    # Save the API key to a .env file
    # Overwrite any existing .env file

    # Open .env file in write mode
    with open(".env", "w") as f:

        # Write the API key in the format expected by the application
        f.write(f"WEATHER_API_KEY={api_key}\n")

    # Inform the user that the API key has been saved
    print("API key saved to .env, you can use it in future runs without providing it again.")

def help():
    # Print help information

    print("Usage:")
    print("  python main.py [ZipCode]")
    print("  python main.py --api-key YOUR_API_KEY")

def handle_zipcode_input(args):
    # This method will handle the case when a ZipCode is provided
    # It will convert the ZipCode to latitude and longitude
    # and then fetch the weather information for that location

    zip_code = args[0]
    print(f"Fetching weather for ZipCode: {zip_code}")
    # Here you would add the logic to convert ZipCode to lat/long
    # and then fetch the weather data using the API

    df = pd.read_csv("Zip-Code.csv")

    zip_code = int(zip_code)

    if zip_code not in df['zip'].values:
        print(f"Error: ZipCode {zip_code} not found in database.")
        sys.exit(1)
    else: 
        df_zip = df[df['zip'] == int(zip_code)]
    
    lat = df_zip['lat'].values[0]
    lng = df_zip['lng'].values[0]

    city = df_zip['city'].values[0]
    state_id = df_zip['state_id'].values[0]
    state_name = df_zip['state_name'].values[0]

    print(f"ZipCode {zip_code} corresponds to {city}, {state_id} ({state_name}) at coordinates ({lat}, {lng})")

    return [lat, lng, state_id, state_name]

    

if __name__ == "__main__":
    main()