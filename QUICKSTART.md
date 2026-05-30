# 🚀 Quick Start Guide - Cafe Ordering System

## ⚡ 5-Minute Setup

### Step 1: Navigate to Project
```bash
cd c:\Users\cj\Desktop\Cafe_Ordering_System
```

### Step 2: Activate Virtual Environment
```bash
venv\Scripts\activate
```

### Step 3: Run the Server
```bash
python manage.py runserver
```

### Step 4: Access the Application
Open your browser and visit:
- **Customer Site**: http://127.0.0.1:8000/
- **Admin Dashboard**: http://127.0.0.1:8000/dashboard/
- **Django Admin**: http://127.0.0.1:8000/admin/

---

## 👤 Login Credentials

**Admin Account:**
```
Username: admin
Password: admin123
```

---

## 🎯 What's Ready to Test

### Sample Data Included
✓ 5 Menu Categories (Coffee, Pastries, Sandwiches, Beverages, Breakfast)
✓ 27 Menu Items with prices
✓ Admin user account
✓ Sample order workflows

### Pages to Explore

#### Customer Side
1. **Homepage** (`/`) - Hero section with featured items
2. **Menu** (`/menu/`) - Browse all items by category
3. **Item Details** - Click any item to see full details
4. **Shopping Cart** (`/orders/cart/`) - Add items here
5. **Checkout** (`/orders/checkout/`) - Complete purchase
6. **Order Tracking** - Track your orders
7. **Profile** (`/accounts/profile/`) - View order history

#### Admin Dashboard
1. **Dashboard** (`/dashboard/`) - See statistics
2. **Orders** - View and manage orders
3. **Categories** - Add/edit/delete categories
4. **Menu Items** - Manage menu items
5. **Users** - View customer accounts
6. **Reports** - Generate sales reports

---

## 🛒 Complete Customer Journey

### Try the Full Workflow:

#### 1. Register New Account
```
Go to: http://127.0.0.1:8000/accounts/register/
- Enter username, email, password
- Create account
```

#### 2. Browse Menu
```
Go to: http://127.0.0.1:8000/menu/
- Browse items by category
- Click on any item to see details
- Add reviews (after purchasing)
```

#### 3. Add Items to Cart
```
- Click "Add to Cart" on any item
- Confirm quantity
- Item added to cart
```

#### 4. View Cart
```
Go to: http://127.0.0.1:8000/orders/cart/
- See all items
- Update quantities
- Remove items if needed
```

#### 5. Checkout
```
Go to: http://127.0.0.1:8000/orders/checkout/
- Fill delivery details
- Select payment method
- Place order
```

#### 6. Order Confirmation
```
- See order number
- View order details
- Get estimated delivery time
```

#### 7. Track Order
```
Go to: http://127.0.0.1:8000/accounts/profile/
- Click "Track" on any order
- See real-time status
- View delivery timeline
```

---

## 👨‍💼 Admin Tasks

### Login to Dashboard
```
1. Go to: http://127.0.0.1:8000/dashboard/
2. Admin login (if needed)
3. See dashboard statistics
```

### Manage Categories
```
1. Dashboard → Categories
2. Click "Add New Category"
3. Enter name, description, icon
4. Save
```

### Add Menu Item
```
1. Dashboard → Menu Items
2. Click "Add New Menu Item"
3. Select category
4. Enter name, price, description
5. Upload image (optional)
6. Check "Featured" to show on homepage
7. Save
```

### Update Order Status
```
1. Dashboard → Orders
2. Click on an order
3. Select new status from dropdown
4. Click "Update Status"
```

### View Reports
```
1. Dashboard → Reports
2. Select date range
3. Click "Generate"
4. View sales statistics
```

---

## 🔍 Key URLs Reference

```
Customer Pages:
  /                           - Homepage
  /menu/                      - All menu items
  /menu/<id>/                 - Item details
  /orders/cart/               - Shopping cart
  /orders/checkout/           - Checkout
  /accounts/register/         - Sign up
  /accounts/login/            - Sign in
  /accounts/profile/          - My orders

Admin Pages:
  /dashboard/                 - Admin home
  /dashboard/orders/          - Order management
  /dashboard/categories/      - Category management
  /dashboard/menu-items/      - Menu items
  /dashboard/users/           - User management
  /dashboard/reports/         - Sales reports
```

---

## 📱 Test on Different Devices

### Desktop
```
http://127.0.0.1:8000
- Full experience
- All features working
```

### Mobile Browser
```
Open same URL on mobile
- Responsive design
- Touch-friendly buttons
- Mobile navigation
```

---

## 🧪 Test Cases to Try

### Customer Testing
- [ ] Register new account
- [ ] Browse menu items
- [ ] Search for items
- [ ] Filter by category
- [ ] View item details
- [ ] Add items to cart
- [ ] Update cart quantities
- [ ] Remove items from cart
- [ ] Proceed to checkout
- [ ] Place order
- [ ] Track order status
- [ ] View order history
- [ ] Leave review on item

### Admin Testing
- [ ] View dashboard stats
- [ ] Search orders
- [ ] Filter orders by status
- [ ] Update order status
- [ ] Add new category
- [ ] Edit category
- [ ] Delete category
- [ ] Add menu item
- [ ] Edit menu item
- [ ] Upload item image
- [ ] Toggle featured items
- [ ] View all users
- [ ] Generate sales report
- [ ] Filter report by date

---

## 🐛 Troubleshooting Quick Fixes

### Port Already in Use
```bash
python manage.py runserver 8001
```
Then visit: http://127.0.0.1:8001/

### Static Files Not Showing
```bash
python manage.py collectstatic
```

### Database Issues
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Reset Everything
```bash
rm db.sqlite3
python manage.py migrate
python setup_admin.py
python populate_sample_data.py
```

---

## 📊 Admin Dashboard Stats Explained

| Stat | Meaning |
|------|---------|
| Total Orders | All orders ever placed |
| New Orders | Orders with "Pending" status |
| Confirmed Orders | Orders confirmed by staff |
| Preparing Orders | Orders being prepared |
| Out for Delivery | Orders in transit |
| Delivered Orders | Completed orders |
| Cancelled Orders | Cancelled/rejected orders |
| Today's Sales | Revenue from today |
| Weekly Sales | Revenue from last 7 days |
| Monthly Sales | Revenue from this month |
| Yearly Sales | Revenue from this year |

---

## 💡 Tips & Tricks

1. **Search Items**: Use the search bar on menu page
2. **Filter by Category**: Click category in sidebar
3. **Featured Items**: Homepage shows featured items only
4. **Track Orders**: Updates real-time in dashboard
5. **Admin Stats**: Update when orders change status
6. **Mobile**: Everything is responsive
7. **Logout**: Click profile dropdown → Logout

---

## 🎓 Learning Resources

### In the Project
- `README.md` - Comprehensive documentation
- `PROJECT_SUMMARY.md` - Technical details
- Code comments throughout files
- Django admin panel (built-in)

### Online Resources
- Django Docs: https://docs.djangoproject.com/
- Bootstrap: https://getbootstrap.com/
- Font Awesome: https://fontawesome.com/

---

## 🎯 Next Steps

1. **Explore the Interface** - Browse around, add items to cart
2. **Try Admin Panel** - Manage categories and items
3. **Place Test Order** - Go through complete checkout
4. **Check Reports** - View sales data
5. **Experiment** - Add new categories, menu items, etc.

---

## ✅ Checklist Before Deployment

- [ ] Change admin password
- [ ] Update SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up email (for notifications)
- [ ] Configure payment gateway (optional)
- [ ] Test all workflows
- [ ] Verify static files
- [ ] Check database backups
- [ ] Set up HTTPS

---

## 📞 Common Questions

**Q: How do I add my own menu items?**
A: Go to Dashboard → Menu Items → Add New Menu Item

**Q: Can I upload images for items?**
A: Yes! When adding/editing menu items, use the image upload field

**Q: How do I change order status?**
A: Go to Dashboard → Orders → Click order → Select status → Update

**Q: Can customers see incomplete orders?**
A: Yes, they see all orders in their profile

**Q: How do I reset the database?**
A: Delete db.sqlite3 and run migrations again

---

**Happy Ordering! 🎉**

For more details, see README.md and PROJECT_SUMMARY.md
