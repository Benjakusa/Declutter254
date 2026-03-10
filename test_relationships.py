# test_relationships.py
from app import create_app, db
from models import User, Category, Item, Request

def test_relationships():
    app = create_app()
    with app.app_context():
        print("\n🔍 TESTING RELATIONSHIPS...\n")
        
        # Test 1: One-to-Many (User -> Items)
        user = User.query.first()
        print(f"Test 1: User {user.name} has {len(user.items)} items")
        assert len(user.items) > 0, "User should have items"
        print("✅ One-to-Many (User->Items) works")
        
        # Test 2: One-to-Many (Category -> Items)
        category = Category.query.first()
        print(f"Test 2: Category {category.name} has {len(category.items)} items")
        assert len(category.items) > 0, "Category should have items"
        print("✅ One-to-Many (Category->Items) works")
        
        # Test 3: Many-to-Many through Request
        item = Item.query.first()
        print(f"Test 3: Item '{item.title}' has {len(item.requests)} requests")
        
        # Test 4: User-Submittable Attribute
        request = Request.query.first()
        print(f"Test 4: Request has message: '{request.message[:30]}...'")
        assert request.message is not None, "Request should have message"
        print("✅ User-submittable attribute (message) works")
        
        # Test 5: Phone number security
        pending_req = Request.query.filter_by(status='pending').first()
        approved_req = Request.query.filter_by(status='approved').first()
        
        print(f"Test 5: Pending request - giver phone: {pending_req.giver_phone}")
        assert pending_req.giver_phone is None, "Pending request should hide phone"
        
        print(f"   Approved request - giver phone: {approved_req.giver_phone}")
        assert approved_req.giver_phone is not None, "Approved request should reveal phone"
        print("✅ Phone number security works")
        
        print("\n🎉 ALL TESTS PASSED!")

if __name__ == "__main__":
    test_relationships()