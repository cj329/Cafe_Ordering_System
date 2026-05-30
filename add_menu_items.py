import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_project.settings')
django.setup()

from menu.models import Category, MenuItem

def remake_menu():
    print("Remaking the menu...")

    # Menu items data organized by category (using UPPERCASE as requested)
    menu_data = {
        'HOT COFFEE': {
            'icon': 'coffee',
            'items': [
                ('Cappuccino', 120),
                ('Café Latte', 150),
                ('Velvet Coffee', 180),
                ('Flat White', 140),
                ('Cinnamon Coffee', 160),
                ('Espresso', 100),
                ('Vanilla Latte', 170),
                ('Filter Coffee', 130),
            ]
        },
        'SNACKS': {
            'icon': 'hamburger',
            'items': [
                ('Sandwich', 120),
                ('Cottage Cheese Fry', 160),
                ('Garlic Bread', 140),
                ('Bread Sticks', 110),
                ('Veg Burger', 180),
                ('Veg Pizza', 220),
                ('Chicken Pockets', 170),
                ('Pita Bread', 130),
            ]
        },
        'COLD COFFEE': {
            'icon': 'snowflake',
            'items': [
                ('Vegan Shake', 160),
                ('Cold Coffee', 140),
                ('Cold Mocha', 180),
                ('Iced Tea', 100),
                ('Chilled Latte', 170),
                ('Belgian Chocolate', 190),
                ('Crunchy Frappé', 210),
                ('Chocolate Shake', 180),
            ]
        },
        'DESSERT': {
            'icon': 'cake-candles',
            'items': [
                ('Cheesecake', 160),
                ('Choco Fantasy', 180),
                ('Brownie', 120),
                ('Choco Fudge', 150),
                ('Vanilla Scoop', 100),
                ('Berry Cheesecake', 190),
                ('Strawberry Cake', 170),
                ('Red Velvet Cake', 200),
            ]
        }
    }

    # Clear existing data to ensure a clean remake
    print("Clearing existing menu items and categories...")
    MenuItem.objects.all().delete()
    Category.objects.all().delete()

    # Create categories and items
    for category_name, category_data in menu_data.items():
        category = Category.objects.create(
            name=category_name,
            description=f'{category_name} items',
            icon=category_data['icon'],
            is_active=True
        )
        print(f"Created category: {category_name}")
        
        for item_name, price in category_data['items']:
            MenuItem.objects.create(
                name=item_name,
                category=category,
                description=f'Delicious {item_name.lower()}',
                price=price,
                is_available=True,
                is_featured=False
            )
            print(f"  + Added: {item_name} - {price}")

    print("\nMenu has been successfully remade!")

if __name__ == "__main__":
    remake_menu()
