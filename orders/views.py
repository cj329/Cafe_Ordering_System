from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import uuid
from .models import Order, OrderItem
from menu.models import MenuItem
from accounts.forms import CheckoutForm


def get_cart_from_session(request):
    """Get cart from session"""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    return request.session['cart']


def save_cart_to_session(request, cart):
    """Save cart to session"""
    request.session['cart'] = cart
    request.session.modified = True


def cart(request):
    """View shopping cart"""
    cart = get_cart_from_session(request)
    cart_items = []
    total_price = 0
    
    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(pk=int(item_id))
            item_total = item.price * quantity
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'total': item_total
            })
            total_price += item_total
        except MenuItem.DoesNotExist:
            del cart[item_id]
    
    save_cart_to_session(request, cart)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_count': sum(cart.values()),
    }
    return render(request, 'orders/cart.html', context)


def add_to_cart(request, item_id):
    """Add item to cart"""
    item = get_object_or_404(MenuItem, pk=item_id, is_available=True)
    cart = get_cart_from_session(request)
    
    item_id_str = str(item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if item_id_str in cart:
        cart[item_id_str] += quantity
    else:
        cart[item_id_str] = quantity
    
    save_cart_to_session(request, cart)
    messages.success(request, f"{item.name} added to cart!")
    
    return redirect('orders:cart')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    item = get_object_or_404(MenuItem, pk=item_id)
    cart = get_cart_from_session(request)
    
    item_id_str = str(item_id)
    if item_id_str in cart:
        del cart[item_id_str]
    
    save_cart_to_session(request, cart)
    messages.success(request, f"{item.name} removed from cart!")
    
    return redirect('orders:cart')


def update_cart(request, item_id):
    """Update item quantity in cart"""
    item = get_object_or_404(MenuItem, pk=item_id)
    cart = get_cart_from_session(request)
    
    item_id_str = str(item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        if item_id_str in cart:
            del cart[item_id_str]
    else:
        cart[item_id_str] = quantity
    
    save_cart_to_session(request, cart)
    return redirect('orders:cart')


@login_required(login_url='accounts:login')
def checkout(request):
    """Checkout view"""
    cart = get_cart_from_session(request)
    
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('menu:menu_list')
    
    # Calculate total
    total_price = 0
    cart_items = []
    for item_id, quantity in cart.items():
        try:
            item = MenuItem.objects.get(pk=int(item_id))
            item_total = item.price * quantity
            cart_items.append({
                'item': item,
                'quantity': quantity,
                'total': item_total
            })
            total_price += item_total
        except MenuItem.DoesNotExist:
            pass
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.order_number = f"ORD-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
            order.total_price = total_price
            order.estimated_delivery = timezone.now() + timedelta(minutes=30)
            order.save()
            
            # Create order items
            for item_id, quantity in cart.items():
                try:
                    item = MenuItem.objects.get(pk=int(item_id))
                    OrderItem.objects.create(
                        order=order,
                        item=item,
                        quantity=quantity,
                        price=item.price
                    )
                except MenuItem.DoesNotExist:
                    pass
            
            # Clear cart
            request.session['cart'] = {}
            request.session.modified = True
            
            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('orders:order_confirmation', order_id=order.id)
    else:
        # Pre-fill form with user data
        form = CheckoutForm(initial={
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'email': request.user.email,
        })
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'orders/checkout.html', context)


def order_confirmation(request, order_id):
    """Order confirmation view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'orders/confirmation.html', context)


def order_tracking(request, order_id):
    """Order tracking view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'orders/tracking.html', context)



