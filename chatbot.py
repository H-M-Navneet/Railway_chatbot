import openai
import requests

# Set up your OpenAI API key
openai.api_key = 'your_api_key_here'

# Define the user's query or message
user_message = "What are the train timings from Delhi to Mumbai tomorrow?"

# Use the ChatGPT API to generate a response
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=user_message,
    max_tokens=50  # Adjust the desired response length
)

# Extract the generated response
chatbot_response = response.choices[0].text.strip() 

# Define the IRCTC API endpoint provided by RapidAPI
irctc_api_url = 'https://irctc1.p.rapidapi.com/api/v3/trainBetweenStations'

# Define parameters for the IRCTC API request (modify as needed)
api_params = {
    #'from_station': 'Delhi',  # Change this to the desired source station
    #'to_station': 'Mumbai',   # Change this to the desired destination station
    #'date': 'tomorrow'
    "fromStationCode":"KJM",
    "toStationCode":"MAS",
    "dateOfJourney":"2023-09-15"
}

# Define your RapidAPI key
rapidapi_key = '4350e08837msh60baa4e99868ec4p157cadjsn64bd696ef316'

# Define headers with the RapidAPI key
headers = {
    'X-RapidAPI-Key': rapidapi_key,
    "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
}

# Make a request to the IRCTC API via RapidAPI
try:
    irctc_response = requests.get(irctc_api_url, params=api_params, headers=headers)
    irctc_data = irctc_response.json()  # Parse the JSON response
    #print(irctc_data)


    # Extract and format relevant station data from the IRCTC response
    stations_info = "Station Information:\n"
    for station in irctc_data['data']:
        train_number = station['train_number']
        station_name = station['train_name']
        from_station_dept = station['from_std']
        to_station_arrival = station['to_sta']
        stations_info += f"Train Name: {station_name},Train Number: {train_number}, From station departure: {from_station_dept}, To station arrival: {to_station_arrival}\n"

    # Combine the chatbot response with the station information
    final_response = f"{chatbot_response}\n\n{stations_info}"
except Exception as e:
    # Handle API request errors
    final_response = f"Error: {str(e)}"

# Print or return the final response to the user
print(final_response)
