import requests
import json

BASE_URL = "http://localhost:5555"

# Create multiple test users
users = [
    {
        "phone_number": "0711111111",
        "password": "password123",
        "name": "John Doe",
        "location": "Westlands, Nairobi"
    },
    {
        "phone_number": "0722222222", 
        "password": "password123",
        "name": "Jane Smith",
        "location": "Kilimani, Nairobi"
    },
    {
        "phone_number": "0733333333",
        "password": "password123",
        "name": "Bob Johnson",
        "location": "Karen, Nairobi"
    }
]

print("Seeding users...")
for user in users:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user)
    if response.status_code == 201:
        print(f"Created user: {user['name']}")
    else:
        print(f"Failed to create {user['name']}: {response.text}")