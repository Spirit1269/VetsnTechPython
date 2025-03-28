import requests

url2 = "https://api.yelp.com/v3/businesses/search?location=dfw&term=Starbucks&sort_by=best_match&limit=20"

headers = {
    "accept": "application/json",
    "authorization": "Bearer lGhHfJ5rJl8nMrr0QLei61oKEm9yS--MZa9WUtadR1-X0qWjXtvBmGRUXKqbWGwEKq6SaBgS4D69fDbKswUSFuU7ZhkLEqnXICzv8zRvfYNi5ofrJ_FZc-hQwKHhZ3Yx"
}

response = requests.get(url2, headers=headers)

print(response.text)