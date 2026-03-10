# reset_db.py
from app import create_app
from extensions import db
from models import User, Category, Item, Request
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def reset_database():
    """Reset and seed the database with fresh data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        print("🗑️  Database dropped and recreated")
        
        # Create categories
        categories = [
            Category(name="Furniture", description="Sofas, tables, beds, chairs"),
            Category(name="Kitchen", description="Pots, sufuria, utensils, plates"),
            Category(name="Electronics", description="TVs, phones, radios, laptops"),
            Category(name="Clothes", description="Children's clothes, adult clothes, shoes"),
            Category(name="Books", description="School books, novels, textbooks"),
            Category(name="Baby Items", description="Baby clothes, toys, equipment"),
            Category(name="Home Decor", description="Curtains, rugs, decorations"),
            Category(name="Sports", description="Equipment, balls, gear")
        ]
        
        db.session.add_all(categories)
        db.session.commit()
        print(f"✅ Created {len(categories)} categories")
        
        # Create users
        users = [
            User(
                phone_number="0712345678",
                password_hash=generate_password_hash("password123"),
                name="Jane Mwangi",
                location="Roysambu, near Tuskys"
            ),
            User(
                phone_number="0723456789",
                password_hash=generate_password_hash("password123"),
                name="John Otieno",
                location="Donholm, near Shell"
            ),
            User(
                phone_number="0734567890",
                password_hash=generate_password_hash("password123"),
                name="Mary Wanjiku",
                location="Lang'ata, near Oilibya"
            ),
            User(
                phone_number="0745678901",
                password_hash=generate_password_hash("password123"),
                name="Peter Kimani",
                location="South B, near Nairobi West"
            ),
            User(
                phone_number="0756789012",
                password_hash=generate_password_hash("password123"),
                name="Sarah Akinyi",
                location="Kilimani, near Junction"
            )
        ]
        
        db.session.add_all(users)
        db.session.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create items
        items = [
            Item(
                title="3-Seater Sofa - Brown Leather",
                description="Comfortable leather sofa, been in storage for 6 months. Still in great condition.",
                photo_url="https://via.placeholder.com/300",
                condition="Good",
                pickup_location="Tuskys Roysambu",
                pickup_days="Saturdays and Sundays",
                pickup_times="10:00 - 14:00",
                special_instructions="Call when you arrive, I'll bring it to the parking lot",
                is_available=True,
                giver_id=users[0].id,
                category_id=categories[0].id
            ),
            Item(
                title="Complete Sufuria Set - 3 pieces",
                description="Three aluminum sufuria, barely used. Sizes: 20cm, 24cm, 28cm.",
                photo_url="https://via.placeholder.com/300",
                condition="Like New",
                pickup_location="Shell Donholm",
                pickup_days="Weekdays after 5pm",
                pickup_times="17:00 - 19:00",
                special_instructions="I'll be at the petrol station, call me",
                is_available=True,
                giver_id=users[1].id,
                category_id=categories[1].id
            ),
            Item(
                title="Children's Clothes Bundle - Age 3-4",
                description="Mix of boys and girls clothes, my twins have outgrown them. Includes shirts, pants, dresses.",
                photo_url="https://via.placeholder.com/300",
                condition="Good",
                pickup_location="Oilibya Lang'ata",
                pickup_days="Saturday only",
                pickup_times="09:00 - 12:00",
                special_instructions="Near the checkout counter",
                is_available=True,
                giver_id=users[2].id,
                category_id=categories[3].id
            ),
            Item(
                title="Form 1 Textbooks - 2024 Edition",
                description="Complete set of Form 1 books: Mathematics, English, Kiswahili, Biology, Chemistry, Physics",
                photo_url="https://via.placeholder.com/300",
                condition="Fair",
                pickup_location="Nairobi West Shopping Center",
                pickup_days="Sunday",
                pickup_times="14:00 - 16:00",
                special_instructions="Text me when you arrive",
                is_available=True,
                giver_id=users[3].id,
                category_id=categories[4].id
            ),
            Item(
                title="Electric Kettle - Russell Hobbs",
                description="1.7L kettle, works perfectly. Upgraded to a thermos so giving away.",
                photo_url="https://via.placeholder.com/300",
                condition="Good",
                pickup_location="Tuskys Roysambu",
                pickup_days="Saturdays",
                pickup_times="10:00 - 12:00",
                special_instructions="I'll be near the vegetables section",
                is_available=True,
                giver_id=users[0].id,
                category_id=categories[2].id
            ),
            Item(
                title="Baby Clothes - Newborn to 6 months",
                description="Bundle of baby clothes, onesies, sleepers. My baby outgrew them quickly.",
                photo_url="https://via.placeholder.com/300",
                condition="Good",
                pickup_location="Junction Mall Kilimani",
                pickup_days="Weekends",
                pickup_times="11:00 - 15:00",
                special_instructions="Near the food court",
                is_available=True,
                giver_id=users[4].id,
                category_id=categories[5].id
            )
        ]
        
        db.session.add_all(items)
        db.session.commit()
        print(f"✅ Created {len(items)} items")
        
        # Create requests with messages
        request_messages = [
            "I'm a first-year student at KU and I have no furniture in my hostel. This would really help!",
            "My family was displaced by floods and we lost everything. We need kitchen items urgently.",
            "I have a young niece I'm caring for and she needs clothes. These would be perfect.",
            "I'm a student at South B primary and I need textbooks for my studies.",
            "I just moved to Nairobi and have no kitchen equipment. Please consider me.",
            "I'm expecting a baby next month and need baby clothes. God bless you for giving."
        ]
        
        requests_list = []
        
        # Create some pending requests
        requests_list.append(Request(
            message=request_messages[0],
            status="pending",
            seeker_id=users[2].id,
            item_id=items[0].id
        ))
        
        requests_list.append(Request(
            message=request_messages[1],
            status="approved",  # Approved to test phone reveal
            seeker_id=users[3].id,
            item_id=items[1].id
        ))
        
        requests_list.append(Request(
            message=request_messages[2],
            status="pending",
            seeker_id=users[1].id,
            item_id=items[2].id
        ))
        
        requests_list.append(Request(
            message=request_messages[3],
            status="rejected",
            seeker_id=users[0].id,
            item_id=items[3].id
        ))
        
        requests_list.append(Request(
            message=request_messages[4],
            status="pending",
            seeker_id=users[2].id,
            item_id=items[4].id
        ))
        
        requests_list.append(Request(
            message=request_messages[5],
            status="completed",  # Completed transaction
            seeker_id=users[0].id,
            item_id=items[5].id
        ))
        
        db.session.add_all(requests_list)
        db.session.commit()
        print(f"✅ Created {len(requests_list)} requests")
        
        # Mark the completed item as unavailable
        items[5].is_available = False
        db.session.commit()
        
        print("\n" + "="*50)
        print("🎉 DATABASE RESET AND SEEDED SUCCESSFULLY!")
        print("="*50)
        print("\n📊 SUMMARY:")
        print(f"   Users: {User.query.count()}")
        print(f"   Categories: {Category.query.count()}")
        print(f"   Items: {Item.query.count()}")
        print(f"   Requests: {Request.query.count()}")
        print("="*50)
        
        # Print test credentials
        print("\n🔑 TEST ACCOUNTS:")
        for user in users:
            print(f"   📱 {user.phone_number} (Password: password123) - {user.name}")

if __name__ == "__main__":
    reset_database()