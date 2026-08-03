import requests
latitude = 22.3082
longitude= 70.8007
#here we have added the location the requests library do all and gives us the weather
#report in the form of the dict datatype
url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"

# we should take url from the google and mention the given things using f strings 
# like latitude and longitude and it will give the information of the weather 
response = requests.get(url)
data = response.json()

print(data)
# as we know that the all requests library are in
#dict datatype so if we want the specific one like temperature
# if we want the data type we are confused weither it is dict or not
type(data)
data["current"]
print("this is weather api")