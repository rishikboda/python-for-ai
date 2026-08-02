import requests
import pandas as pd

response = requests.get("https://jsonplaceholder.typicode.com/users")
api_data = response.json()
print(api_data[0])  # see the shape of the data