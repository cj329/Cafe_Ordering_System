from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem


class Order(models.Model):
    """Order model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ]

    ONLINE_PAYMENT_CHOICES = [
        ('gcash', 'GCash'),
        ('paymaya', 'PayMaya'),
        ('credit_card', 'Credit Card'),
        ('other', 'Other Transaction'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    
    # Customer details
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    # Order details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    online_payment_method = models.CharField(max_length=20, choices=ONLINE_PAYMENT_CHOICES, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"

    def get_status_display_detailed(self):
        """Get detailed status display with emoji"""
        status_map = {
            'pending': '⏳ Pending',
            'confirmed': '✅ Confirmed',
            'preparing': '🍳 Preparing',
            'ready': '🎉 Ready for Pickup',
            'out_for_delivery': '🚚 Out for Delivery',
            'delivered': '📦 Delivered',
            'cancelled': '❌ Cancelled',
        }
        return status_map.get(self.status, self.get_status_display())

    def get_status_step(self):
        """Return the step number (1-6) for tracking progress"""
        steps = {
            'pending': 1,
            'confirmed': 2,
            'preparing': 3,
            'ready': 4,
            'out_for_delivery': 5,
            'delivered': 6,
            'cancelled': 0,
        }
        return steps.get(self.status, 1)


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.name} x{self.quantity}"

    def get_total(self):
        return self.price * self.quantity

