import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_project.settings')
django.setup()

from menu.models import Category, MenuItem
from django.contrib.auth.models import User

print("🔄 Populating database with sample data...\n")

# Create categories
categories_data = [
    {
        'name': 'Coffee',
        'description': 'Hot and cold coffee beverages',
        'icon': 'coffee'
    },
    {
        'name': 'Pastries',
        'description': 'Fresh baked pastries and desserts',
        'icon': 'cake-candles'
    },
    {
        'name': 'Sandwiches',
        'description': 'Delicious sandwiches and wraps',
        'icon': 'sandwich'
    },
    {
        'name': 'Beverages',
        'description': 'Juice, tea, and other drinks',
        'icon': 'water'
    },
    {
        'name': 'Breakfast',
        'description': 'Morning specials and breakfast items',
        'icon': 'utensils'
    },
]

categories = {}
for cat_data in categories_data:
    cat, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'description': cat_data['description'],
            'icon': cat_data['icon'],
            'is_active': True
        }
    )
    categories[cat_data['name']] = cat
    if created:
        print(f"✓ Created category: {cat.name}")
    else:
        print(f"- Category already exists: {cat.name}")

# Create menu items
items_data = [
    # Coffee
    {'category': 'Coffee', 'name': 'Espresso', 'description': 'Strong and bold single shot espresso', 'price': 45.00, 'featured': False},
    {'category': 'Coffee', 'name': 'Cappuccino', 'description': 'Creamy cappuccino with perfect foam', 'price': 65.00, 'featured': True},
    {'category': 'Coffee', 'name': 'Latte', 'description': 'Smooth and creamy coffee latte', 'price': 65.00, 'featured': True},
    {'category': 'Coffee', 'name': 'Americano', 'description': 'Classic black coffee drink', 'price': 50.00, 'featured': False},
    {'category': 'Coffee', 'name': 'Iced Coffee', 'description': 'Refreshing cold brew coffee', 'price': 55.00, 'featured': False},
    
    # Pastries
    {'category': 'Pastries', 'name': 'Croissant', 'description': 'Buttery French croissant', 'price': 50.00, 'featured': True},
    {'category': 'Pastries', 'name': 'Blueberry Muffin', 'description': 'Fresh blueberry muffin', 'price': 40.00, 'featured': True},
    {'category': 'Pastries', 'name': 'Chocolate Cake', 'description': 'Rich chocolate layer cake', 'price': 85.00, 'featured': False},
    {'category': 'Pastries', 'name': 'Donut', 'description': 'Glazed donut', 'price': 30.00, 'featured': False},
    {'category': 'Pastries', 'name': 'Cheesecake', 'description': 'New York style cheesecake', 'price': 75.00, 'featured': False},
    
    # Sandwiches
    {'category': 'Sandwiches', 'name': 'Club Sandwich', 'description': 'Triple-stacked club sandwich', 'price': 140.00, 'featured': False},
    {'category': 'Sandwiches', 'name': 'Chicken Wrap', 'description': 'Grilled chicken in whole wheat wrap', 'price': 120.00, 'featured': True},
    {'category': 'Sandwiches', 'name': 'Turkey Panini', 'description': 'Toasted turkey and cheese panini', 'price': 130.00, 'featured': False},
    {'category': 'Sandwiches', 'name': 'Veggie Sandwich', 'description': 'Fresh veggie sandwich', 'price': 100.00, 'featured': False},
    
    # Beverages
    {'category': 'Beverages', 'name': 'Orange Juice', 'description': 'Fresh squeezed orange juice', 'price': 65.00, 'featured': False},
    {'category': 'Beverages', 'name': 'Green Tea', 'description': 'Healthy green tea', 'price': 50.00, 'featured': False},
    {'category': 'Beverages', 'name': 'Smoothie', 'description': 'Mixed fruit smoothie', 'price': 85.00, 'featured': True},
    {'category': 'Beverages', 'name': 'Iced Tea', 'description': 'Refreshing iced tea', 'price': 45.00, 'featured': False},
    
    # Breakfast
    {'category': 'Breakfast', 'name': 'Pancakes', 'description': 'Fluffy pancakes with syrup', 'price': 120.00, 'featured': True},
    {'category': 'Breakfast', 'name': 'French Toast', 'description': 'Golden French toast', 'price': 110.00, 'featured': False},
    {'category': 'Breakfast', 'name': 'Egg Benedict', 'description': 'Classic eggs benedict', 'price': 125.00, 'featured': False},
    {'category': 'Breakfast', 'name': 'Oatmeal', 'description': 'Creamy oatmeal with toppings', 'price': 80.00, 'featured': False},
]

for item_data in items_data:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        defaults={
            'category': categories[item_data['category']],
            'description': item_data['description'],
            'price': item_data['price'],
            'is_available': True,
            'is_featured': item_data['featured']
        }
    )
    if created:
        print(f"✓ Created menu item: {item.name}")
    else:
        print(f"- Item already exists: {item.name}")

print("\n✅ Sample data population complete!")
print("\nYou can now:")
print("1. Visit http://127.0.0.1:8000/ to view the homepage")
print("2. Visit http://127.0.0.1:8000/dashboard/ to access the admin dashboard")
print("3. Login with: admin / admin123")
