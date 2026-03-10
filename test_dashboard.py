# test_dashboard.py
import requests
import json

BASE_URL = "http://localhost:5555"

def test_dashboard():
    """Test dashboard endpoints"""
    print("\n" + "="*60)
    print("📊 TESTING DASHBOARD ENDPOINTS")
    print("="*60)
    
    # First login to get token
    login_data = {
        "phone_number": "0712345678",  # Jane Mwangi
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code != 200:
        print("❌ Login failed")
        return
    
    token = response.json()['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test user stats
    print("\n1️⃣ Getting user stats...")
    response = requests.get(f"{BASE_URL}/api/dashboard/stats", headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print("✅ User stats retrieved:")
        print(f"   As Giver: {json.dumps(stats['as_giver'], indent=2)}")
        print(f"   As Seeker: {json.dumps(stats['as_seeker'], indent=2)}")
        print(f"   Impact: {json.dumps(stats['impact'], indent=2)}")
    else:
        print(f"❌ Failed: {response.text}")
    
    # Test recent activity
    print("\n2️⃣ Getting recent activity...")
    response = requests.get(f"{BASE_URL}/api/dashboard/activity", headers=headers)
    if response.status_code == 200:
        activity = response.json()
        print("✅ Recent activity retrieved:")
        print(f"   Incoming requests: {len(activity['incoming_requests'])}")
        print(f"   Outgoing requests: {len(activity['outgoing_requests'])}")
        print(f"   Recent items: {len(activity['recent_items'])}")
    else:
        print(f"❌ Failed: {response.text}")
    
    # Test community stats (public)
    print("\n3️⃣ Getting community stats...")
    response = requests.get(f"{BASE_URL}/api/dashboard/community-stats")
    if response.status_code == 200:
        stats = response.json()
        print("✅ Community stats retrieved:")
        print(f"   Total items given: {stats['total_items_given']}")
        print(f"   Active items: {stats['active_items']}")
        print(f"   Total users: {stats['total_users']}")
        print(f"   Waste prevented: {stats['estimated_waste_prevented_kg']}kg")
    else:
        print(f"❌ Failed: {response.text}")
    
    print("\n" + "="*60)
    print("✅ Dashboard tests complete")
    print("="*60)

if __name__ == "__main__":
    test_dashboard()