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

# Sample categories
categories = [
    {"name": "Electronics", "description": "Gadgets, phones, computers"},
    {"name": "Furniture", "description": "Tables, chairs, sofas"},
    {"name": "Clothing", "description": "Apparel, shoes, accessories"},
    {"name": "Books", "description": "Novels, textbooks, magazines"},
    {"name": "Home Appliances", "description": "Kitchen, laundry, cleaning"}
]

# Sample items
items = [
    {
        "title": "iPhone 12 Pro",
        "description": "Like new, 256GB, Pacific Blue",
        "condition": "Good",
        "category": "Electronics",
        "seller_phone": "0711111111",
        "pickup_location": "Westlands, Nairobi",
    },
    {
        "title": "Wooden Dining Table",
        "description": "6-seater, solid oak, excellent condition",
        "condition": "Good",
        "category": "Furniture",
        "seller_phone": "0722222222",
        "pickup_location": "Kilimani, Nairobi",
    },
    {
        "title": "Samsung 4K TV",
        "description": "55-inch, Smart TV, 1 year old",
        "condition": "Like New",
        "category": "Electronics",
        "seller_phone": "0733333333",
        "pickup_location": "Karen, Nairobi",
    }
]

def seed():
    print("🌱 SEEDING DATA...")
    print("="*50)

    # 1. Create users
    print("\n📝 CREATING USERS...")
    for user in users:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user)
        if response.status_code == 201:
            print(f"✅ Created user: {user['name']} ({user['phone_number']})")
        elif response.status_code == 409:
            print(f"ℹ️ User already exists: {user['name']}")
        else:
            print(f"❌ Failed to create {user['name']}: {response.status_code} - {response.text}")

    # 2. Login to get token (using John Doe)
    print("\n🔐 LOGGING IN...")
    login_data = {"phone_number": "0711111111", "password": "password123"}
    login_res = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if login_res.status_code != 200:
        print(f"❌ Login failed: {login_res.text}")
        return
    token = login_res.json().get('access_token') or login_res.json().get('token')
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Logged in successfully.")

    # 3. Create categories
    print("\n📑 CREATING CATEGORIES...")
    cat_map = {}
    for category in categories:
        response = requests.post(f"{BASE_URL}/api/categories/", json=category, headers=headers)
        if response.status_code == 201:
            cat_data = response.json()
            cat_map[category['name']] = cat_data['id']
            print(f"✅ Created category: {category['name']}")
        elif response.status_code == 409:
            # Fetch to get the ID
            get_res = requests.get(f"{BASE_URL}/api/categories/")
            for c in get_res.json():
                if c['name'] == category['name']:
                    cat_map[category['name']] = c['id']
            print(f"ℹ️ Category already exists: {category['name']}")
        else:
            print(f"❌ Failed to create category {category['name']}: {response.status_code} - {response.text}")

    # 4. Create items
    print("\n📦 CREATING ITEMS...")
    for item in items:
        # We need to use the token for the specific user to be accurate, 
        # but for seeding one user can post all if needed. 
        # Let's try to post as John Doe for simplicity unless we want to login as each.
        
        # Adjust item payload to match API expectation
        api_item = {
            "title": item["title"],
            "description": item["description"],
            "condition": item["condition"],
            "pickup_location": item["pickup_location"],
            "category_id": cat_map.get(item["category"])
        }
        
        response = requests.post(f"{BASE_URL}/api/items/", json=api_item, headers=headers)
        if response.status_code == 201:
            print(f"✅ Created item: {item['title']}")
        else:
            print(f"❌ Failed to create item {item['title']}: {response.status_code} - {response.text}")

    print("\n" + "="*50)
    print("✅ SEEDING COMPLETE!")

if __name__ == "__main__":
    seed()
