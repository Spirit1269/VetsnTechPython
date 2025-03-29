import requests

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env into environment

url2 = "https://api.yelp.com/v3/businesses/search?location=dfw&term=Starbucks&sort_by=best_match&limit=20"
yelp_api_key = os.getenv("YELP_API_KEY")

headers = {
    "accept": "application/json",
    "authorization": yelp_api_key
}

response = requests.get(url2, headers=headers)

print(response.text)
