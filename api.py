import requests

# GET Method
api_url = "https://jsonplaceholder.typicode.com/todos/1"
response = requests.get(api_url)
print(response.json())
print(response.status_code)
print(response.headers["Content-Type"])

# POST Method
api_url = "https://jsonplaceholder.typicode.com/todos"
data = {"userId": 1, "title": "Buy milk", "completed": False}
response = requests.post(api_url, json=data)
print(response.json())
print(response.status_code)
print(response.headers["Content-Type"])

# PUT Method
api_url = "https://jsonplaceholder.typicode.com/todos/10"
data = {"userId": 1, "title": "Wash car", "completed": True}
response = requests.put(api_url, json=data)
print(response.json())
print(response.status_code)
print(response.headers["Content-Type"])

# PATCH Method
api_url = "https://jsonplaceholder.typicode.com/todos/10"
data = {"title": "Mow lawn"}
response = requests.put(api_url, json=data)
print(response.json())
print(response.status_code)
print(response.headers["Content-Type"])

# PATCH Method
api_url = "https://jsonplaceholder.typicode.com/todos/10"
response = requests.delete(api_url)
print(response.json())
print(response.status_code)
print(response.headers["Content-Type"])
