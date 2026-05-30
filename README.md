# Cafe Ordering System - Full Stack Application

A complete Django-based cafe ordering system with customer frontend and admin dashboard.

## 🚀 Features

### Customer Features
- **Homepage**: Hero section with featured items and category browsing
- **Menu System**: Browse items by category with search functionality
- **Shopping Cart**: Session-based cart with add/remove/update functionality
- **User Authentication**: Registration and login system
- **Checkout**: Complete order placement with delivery details
- **Order Tracking**: Real-time order status tracking
- **User Profile**: View order history and details
- **Product Reviews**: Rate and review menu items

### Admin Dashboard
- **Dashboard Stats**: Real-time analytics (orders, sales, users)
- **Order Management**: View, filter, and update order status
- **Category Management**: Create, edit, and delete menu categories
- **Menu Items**: Full CRUD operations with image uploads
- **Users Management**: View and manage customer accounts
- **Sales Reports**: Generate reports by date range
- **Sidebar Navigation**: Easy access to all admin functions

## 📋 Tech Stack

- **Backend**: Django 6.0.4
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite3
- **Authentication**: Django built-in auth system
- **Images**: Pillow for image handling
- **Icons**: Font Awesome 6.4.0

## 🗂️ Project Structure

```
Cafe_Ordering_System/
├── cafe_project/              # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                   # User authentication app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── menu/                       # Menu management app
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── orders/                     # Order management app
│   ├── models.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── dashboard/                  # Admin dashboard app
│   ├── views.py
│   └── urls.py
├── templates/                  # HTML templates
│   ├── base.html
│   ├── menu/
│   ├── accounts/
│   ├── orders/
│   └── dashboard/
├── static/                     # CSS and JavaScript files
│   ├── css/style.css
│   └── js/script.js
├── media/                      # User uploads (menu images)
├── manage.py
└── db.sqlite3                  # SQLite database
```

## 📦 Database Models

### User (Django Built-in)
- username, email, password, first_name, last_name

### Category
- name, description, icon, is_active

### MenuItem
- category (FK), name, description, price, image, is_available, is_featured

### Order
- user (FK), order_number, full_name, email, phone, address
- status (pending/confirmed/preparing/ready/out_for_delivery/delivered/cancelled)
- payment_method (cash/online), total_price, created_at, estimated_delivery

### OrderItem
- order (FK), item (FK), quantity, price

### Review
- user (FK), item (FK), rating (1-5), comment, created_at

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation Steps

1. **Navigate to project directory**:
   ```bash
   cd c:\Users\cj\Desktop\Cafe_Ordering_System
   ```

2. **Activate virtual environment**:
   ```bash
   venv\Scripts\activate
   ```

3. **Install dependencies** (if not already done):
   ```bash
   pip install django pillow
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (already done with admin/admin123):
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files** (for production):
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Customer Site: http://127.0.0.1:8000/
   - Admin Dashboard: http://127.0.0.1:8000/dashboard/
   - Django Admin: http://127.0.0.1:8000/admin/

## 👤 Test Credentials

### Admin Account
- **Username**: admin
- **Password**: gamer071
- **Access**: http://127.0.0.1:8000/dashboard/

## 🎯 URL Routes

### Customer URLs
- `/` - Homepage
- `/menu/` - Menu listing
- `/menu/<id>/` - Menu item detail
- `/orders/cart/` - Shopping cart
- `/orders/checkout/` - Checkout
- `/orders/confirmation/<id>/` - Order confirmation
- `/orders/tracking/<id>/` - Order tracking
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/profile/` - User profile
- `/accounts/logout/` - User logout

### Admin URLs
- `/dashboard/` - Dashboard home
- `/dashboard/orders/` - Orders management
- `/dashboard/categories/` - Categories management
- `/dashboard/menu-items/` - Menu items management
- `/dashboard/users/` - Users management
- `/dashboard/reports/` - Sales reports

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Color Scheme**: Warm cafe colors (brown, cream, beige)
- **Card-based Layout**: Clean, organized presentation
- **Smooth Animations**: Hover effects and transitions
- **Icons**: Font Awesome integration
- **Bootstrap 5**: Professional UI components

## 🔐 Security Features

- CSRF Protection on all forms
- Django built-in password hashing
- Session-based authentication
- Admin-only dashboard access
- Secure order processing

## 📊 Admin Dashboard Stats

- **Real-time Order Counts**: By status
- **Sales Metrics**: Today, Weekly, Monthly, Yearly
- **System Stats**: Total users, categories, menu items
- **Date-range Reports**: Filter and analyze sales data
- **Order Filters**: By status, customer, order number

## ✨ Key Features Implementation

### Shopping Cart
- Session-based storage (no database required)
- Add/remove items
- Update quantities
- Persistent across sessions

### Order Processing
- Generate unique order numbers
- Automatic delivery time calculation
- Payment method selection
- Order status workflow

### Admin Features
- Bulk operations ready
- Search and filter across all resources
- Image upload support
- Status tracking for orders

## 🚨 Troubleshooting

### Common Issues

1. **Port 8000 already in use**:
   ```bash
   python manage.py runserver 8001
   ```

2. **Database locked**:
   ```bash
   rm db.sqlite3
   python manage.py migrate
   ```

3. **Missing migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Images not displaying**:
   - Check MEDIA_URL and MEDIA_ROOT in settings.py
   - Ensure media folder exists
   - DEBUG=True is set

## 📝 Usage Examples

### Create a Menu Category
1. Login as admin at /dashboard/
2. Go to Categories
3. Click "Add New Category"
4. Fill in name, description, icon (e.g., "coffee")
5. Click "Create Category"

### Add Menu Item
1. Go to Menu Items in dashboard
2. Click "Add New Menu Item"
3. Select category, add name, description, price
4. Upload image (optional)
5. Check "Available" and "Featured" if needed
6. Save

### Update Order Status
1. Go to Orders in dashboard
2. Click on order to view details
3. Select new status from dropdown
4. Click "Update Status"

## 🔄 Workflow

### Customer Journey
1. Browse menu items
2. Add items to cart
3. Review cart
4. Checkout (login required)
5. Place order
6. Track order status
7. View order in profile

### Admin Workflow
1. Dashboard overview
2. Manage menu & categories
3. Review orders
4. Update order statuses
5. Generate reports
6. Manage users

## 📈 Future Enhancements

- Email notifications for order updates
- Payment gateway integration
- Real-time notifications (WebSocket)
- Multi-language support
- Advanced analytics
- Loyalty program
- Mobile app
- QR code ordering

## 📞 Support

For issues or questions, check the following:
1. Ensure all migrations are applied
2. Verify static files are collected
3. Check database connectivity
4. Review Django logs for errors

## 📄 License

This project is open source and available for educational purposes.

---

**Created**: May 6, 2026
**Version**: 1.0
**Django Version**: 6.0.4
**Python Version**: 3.14.4
