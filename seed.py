# seed.py
from app import create_app, db
from models import User, Category, Item, Request
from datetime import datetime, timedelta

def seed_database():
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print(" Seeding database...")
        
        # Create categories
        categories = [
            Category(name="Furniture", description="Sofas, tables, beds, chairs"),
            Category(name="Kitchen", description="Pots, sufuria, utensils, plates"),
            Category(name="Electronics", description="TVs, phones, radios, laptops"),
            Category(name="Clothes", description="Children's clothes, adult clothes, shoes"),
            Category(name="Books", description="School books, novels, textbooks"),
            Category(name="Baby Items", description="Baby clothes, toys, equipment")
        ]
        
        db.session.add_all(categories)
        db.session.commit()
        print(f" Added {len(categories)} categories")
        
        # Create users (givers)
        users = [
            User(
                phone_number="0712345678",
                password_hash="temp_hash_1",
                name="Jane Mwangi",
                location="Roysambu, near Tuskys"
            ),
            User(
                phone_number="0723456789",
                password_hash="temp_hash_2",
                name="John Otieno",
                location="Donholm, near Shell"
            ),
            User(
                phone_number="0734567890",
                password_hash="temp_hash_3",
                name="Mary Wanjiku",
                location="Lang'ata, near Oilibya"
            ),
            User(
                phone_number="0745678901",
                password_hash="temp_hash_4",
                name="Peter Kimani",
                location="South B, near Nairobi West"
            )
        ]
        
        db.session.add_all(users)
        db.session.commit()
        print(f" Added {len(users)} users")
        
        # Create items
        items = [
            Item(
                title="Sofa Set - 3 seater",
                description="Brown leather sofa, still in good condition. Been in store for 6 months.",
                photo_url="https://example.com/sofa1.jpg",
                condition="Good",
                pickup_location="Tuskys Roysambu",
                pickup_days="Saturdays and Sundays",
                pickup_times="10:00 - 14:00",
                special_instructions="Call when you arrive, I'll bring it to the parking lot",
                is_available=True,
                giver_id=users[0].id,
                category_id=categories[0].id  # Furniture
            ),
            Item(
                title="Sufuria Set - 3 pieces",
                description="Three sufuria in excellent condition. Hardly used.",
                photo_url="https://example.com/sufuria1.jpg",
                condition="Like New",
                pickup_location="Shell Donholm",
                pickup_days="Weekdays after 5pm",
                pickup_times="17:00 - 19:00",
                special_instructions="I'll be at the petrol station, call me",
                is_available=True,
                giver_id=users[1].id,
                category_id=categories[1].id  # Kitchen
            ),
            Item(
                title="Children's clothes - Age 3-4",
                description="Mix of boys and girls clothes, my twins have outgrown them.",
                photo_url="https://example.com/clothes1.jpg",
                condition="Good",
                pickup_location="Oilibya Lang'ata",
                pickup_days="Saturday only",
                pickup_times="09:00 - 12:00",
                special_instructions="Near the checkout counter",
                is_available=True,
                giver_id=users[2].id,
                category_id=categories[3].id  # Clothes
            ),
            Item(
                title="Form 1 Textbooks - 2024",
                description="Complete set of Form 1 books, still useful.",
                photo_url="https://example.com/books1.jpg",
                condition="Fair",
                pickup_location="Nairobi West Shopping Center",
                pickup_days="Sunday",
                pickup_times="14:00 - 16:00",
                special_instructions="Text me when you arrive",
                is_available=True,
                giver_id=users[3].id,
                category_id=categories[4].id  # Books
            ),
            Item(
                title="Electric Kettle",
                description="Russell Hobbs kettle, works perfectly. Upgraded to a thermos.",
                photo_url="https://example.com/kettle1.jpg",
                condition="Good",
                pickup_location="Tuskys Roysambu",
                pickup_days="Saturdays",
                pickup_times="10:00 - 12:00",
                special_instructions="I'll be near the vegetables section",
                is_available=True,
                giver_id=users[0].id,
                category_id=categories[2].id  # Electronics
            )
        ]
        
        db.session.add_all(items)
        db.session.commit()
        print(f" Added {len(items)} items")
        
        # Create requests (many-to-many relationships with user-submittable attribute)
        requests = [
            Request(
                message="I'm a first-year student at KU and I have no furniture in my hostel. This sofa would really help!",
                status="pending",
                seeker_id=users[2].id,  # Mary requesting
                item_id=items[0].id      # Jane's sofa
            ),
            Request(
                message="My family was displaced by floods and we lost everything. We need kitchen items urgently.",
                status="approved",  # This one is approved to test phone reveal
                seeker_id=users[3].id,  # Peter requesting
                item_id=items[1].id      # John's sufuria
            ),
            Request(
                message="I have a young niece I'm caring for and she needs clothes. These would be perfect.",
                status="pending",
                seeker_id=users[1].id,  # John requesting
                item_id=items[2].id      # Mary's clothes
            ),
            Request(
                message="I'm a student at South B primary and I need textbooks for my studies.",
                status="rejected",  # Example of rejected request
                seeker_id=users[0].id,  # Jane requesting
                item_id=items[3].id      # Peter's books
            ),
            Request(
                message="I just moved to Nairobi and have no kitchen equipment. Please consider me.",
                status="pending",
                seeker_id=users[2].id,  # Mary requesting
                item_id=items[4].id      # Jane's kettle
            )
        ]
        
        db.session.add_all(requests)
        db.session.commit()
        print(f" Added {len(requests)} requests")
        
        print("\n" + "="*50)
        print(" DATABASE SEEDED SUCCESSFULLY!")
        print("="*50)
        
        # Print summary
        print(f"\n DATABASE SUMMARY:")
        print(f"   Users: {User.query.count()}")
        print(f"   Categories: {Category.query.count()}")
        print(f"   Items: {Item.query.count()}")
        print(f"   Requests: {Request.query.count()}")
        
        # Show relationship examples
        print(f"\n RELATIONSHIP EXAMPLES:")
        
        # One-to-Many: User -> Items
        jane = User.query.filter_by(name="Jane Mwangi").first()
        print(f"   {jane.name} has {len(jane.items)} items:")
        for item in jane.items:
            print(f"      - {item.title}")
        
        # Many-to-Many: Requests
        print(f"\n   Request Example (with user-submittable attribute):")
        approved_req = Request.query.filter_by(status="approved").first()
        print(f"      Message: '{approved_req.message}'")
        print(f"      Status: {approved_req.status}")
        print(f"      Seeker: {approved_req.seeker.name}")
        print(f"      Item: {approved_req.item.title}")
        print(f"      Giver Phone (revealed because approved): {approved_req.giver_phone}")
        
        print("="*50)

if __name__ == "__main__":
    seed_database()