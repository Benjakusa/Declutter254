# test_models.py
from app import create_app, db
from models import User, Category

def test_create_records():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them fresh
        db.drop_all()
        db.create_all()
        
        # Create a test user
        user = User(
            phone_number="0712345678",
            password_hash="temp_hash_will_fix_later",
            name="John Doe",
            location="Roysambu, near Tuskys"
        )
        
        # Create categories
        furniture = Category(name="Furniture", description="Sofas, tables, chairs")
        kitchen = Category(name="Kitchen", description="Pots, utensils, sufuria")
        electronics = Category(name="Electronics", description="TVs, phones, radios")
        clothes = Category(name="Clothes", description="Children's clothes, adult clothes")
        books = Category(name="Books", description="School books, novels")
        
        # Add to database
        db.session.add(user)
        db.session.add_all([furniture, kitchen, electronics, clothes, books])
        db.session.commit()
        
        print("=" * 50)
        print("TEST RECORDS CREATED SUCCESSFULLY!")
        print("=" * 50)
        print(f"User: {user.name} - {user.phone_number}")
        print("\nCategories created:")
        for cat in [furniture, kitchen, electronics, clothes, books]:
            print(f"   - {cat.name}: {cat.description}")
        print("=" * 50)
        
        # Verify they were saved
        users_count = User.query.count()
        categories_count = Category.query.count()
        print(f"\nDatabase stats:")
        print(f"   - Total users: {users_count}")
        print(f"   - Total categories: {categories_count}")
        print("=" * 50)

if __name__ == "__main__":
    test_create_records()