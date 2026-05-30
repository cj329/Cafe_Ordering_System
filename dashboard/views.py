from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q, F
from datetime import timedelta, date, datetime
from django.contrib.auth.models import User
from menu.models import Category, MenuItem, Review
from orders.models import Order, OrderItem
import json
# pyrefly: ignore [missing-import]
from django.http import JsonResponse


def is_admin(user):
    """Check if user is admin"""
    return user.is_staff or user.is_superuser


def _month_offset(base_date, months_back):
    """Return a date that is `months_back` months before `base_date` (safe across year boundaries)."""
    month = base_date.month - months_back
    year = base_date.year
    while month <= 0:
        month += 12
        year -= 1
    return base_date.replace(year=year, month=month, day=1)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def dashboard(request):
    """Admin dashboard view with comprehensive statistics"""
    today = timezone.now().date()
    now = timezone.now()

    # ===== ORDER STATISTICS =====
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    confirmed_orders = Order.objects.filter(status='confirmed').count()
    preparing_orders = Order.objects.filter(status='preparing').count()
    ready_orders = Order.objects.filter(status='ready').count()
    out_for_delivery_orders = Order.objects.filter(status='out_for_delivery').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()

    # ===== USER & CATEGORY STATISTICS =====
    total_users = User.objects.count()
    total_categories = Category.objects.count()
    total_menu_items = MenuItem.objects.count()
    total_reviews = Review.objects.count()

    # ===== SALES DATA =====
    orders_today = Order.objects.filter(created_at__date=today)
    today_sales = orders_today.aggregate(total=Sum('total_price'))['total'] or 0

    # Weekly sales (last 7 days)
    week_start = today - timedelta(days=6)
    weekly_orders = Order.objects.filter(created_at__date__gte=week_start)
    weekly_sales = weekly_orders.aggregate(total=Sum('total_price'))['total'] or 0

    # Monthly sales (current month)
    month_start = today.replace(day=1)
    monthly_orders = Order.objects.filter(created_at__date__gte=month_start)
    monthly_sales = monthly_orders.aggregate(total=Sum('total_price'))['total'] or 0

    # Yearly sales (current year)
    yearly_orders = Order.objects.filter(created_at__year=today.year)
    yearly_sales = yearly_orders.aggregate(total=Sum('total_price'))['total'] or 0

    # ===== TOP SELLING ITEMS =====
    top_items = OrderItem.objects.values('item__name', 'item__id').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('price') * F('quantity'))
    ).order_by('-total_quantity')[:5]

    # ===== DAILY SALES FOR CHART (Last 7 days) =====
    daily_sales = []
    daily_labels = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        sales = Order.objects.filter(
            created_at__date=d,
            status__in=['confirmed', 'preparing', 'ready', 'out_for_delivery', 'delivered']
        ).aggregate(total=Sum('total_price'))['total'] or 0
        daily_sales.append(float(sales))
        daily_labels.append(d.strftime('%a'))

    # ===== MONTHLY SALES FOR CHART (Last 12 months) — safe year-boundary =====
    monthly_chart_data = []
    monthly_chart_labels = []
    for i in range(11, -1, -1):
        month_date = _month_offset(today, i)
        month_sales = Order.objects.filter(
            created_at__year=month_date.year,
            created_at__month=month_date.month,
            status__in=['confirmed', 'preparing', 'ready', 'out_for_delivery', 'delivered']
        ).aggregate(total=Sum('total_price'))['total'] or 0
        monthly_chart_data.append(float(month_sales))
        monthly_chart_labels.append(month_date.strftime('%b %y'))

    # ===== CATEGORY-WISE SALES =====
    category_sales = []
    category_labels = []
    categories = Category.objects.all()
    for category in categories:
        cat_sales = OrderItem.objects.filter(
            item__category=category,
            order__status__in=['confirmed', 'preparing', 'ready', 'out_for_delivery', 'delivered']
        ).aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
        if cat_sales > 0:
            category_sales.append(float(cat_sales))
            category_labels.append(category.name)

    # ===== RECENT ORDERS =====
    recent_orders = Order.objects.prefetch_related('items', 'items__item').order_by('-created_at')[:5]

    # ===== ORDER STATUS DISTRIBUTION =====
    status_colors = {
        'pending': '#FFC107',
        'confirmed': '#17A2B8',
        'preparing': '#FF6B6B',
        'ready': '#28A745',
        'out_for_delivery': '#007BFF',
        'delivered': '#20C997',
        'cancelled': '#6C757D',
    }

    status_data = {
        'pending': pending_orders,
        'confirmed': confirmed_orders,
        'preparing': preparing_orders,
        'ready': ready_orders,
        'out_for_delivery': out_for_delivery_orders,
        'delivered': delivered_orders,
        'cancelled': cancelled_orders,
    }

    context = {
        # Order stats
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'preparing_orders': preparing_orders,
        'ready_orders': ready_orders,
        'out_for_delivery_orders': out_for_delivery_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,

        # User & Category stats
        'total_users': total_users,
        'total_categories': total_categories,
        'total_menu_items': total_menu_items,
        'total_reviews': total_reviews,

        # Sales stats
        'today_sales': float(today_sales),
        'weekly_sales': float(weekly_sales),
        'monthly_sales': float(monthly_sales),
        'yearly_sales': float(yearly_sales),

        # Chart data
        'daily_sales_data': json.dumps(daily_sales),
        'daily_labels': json.dumps(daily_labels),
        'monthly_chart_data': json.dumps(monthly_chart_data),
        'monthly_chart_labels': json.dumps(monthly_chart_labels),
        'category_sales': json.dumps(category_sales),
        'category_labels': json.dumps(category_labels),

        # Top items
        'top_items': top_items,

        # Recent orders
        'recent_orders': recent_orders,

        # Status colors
        'status_colors': status_colors,
        'status_data': status_data,
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def orders_list(request):
    """Orders management view"""
    status_filter = request.GET.get('status')
    search_query = request.GET.get('search', '')

    orders = Order.objects.prefetch_related('items').all()

    if status_filter and status_filter != 'all':
        orders = orders.filter(status=status_filter)

    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(full_name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    orders = orders.order_by('-created_at')

    status_choices = Order.STATUS_CHOICES

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
        'status_choices': status_choices,
    }
    return render(request, 'dashboard/orders.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def order_detail(request, order_id):
    """Order detail view - status update only"""
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in Order.STATUS_CHOICES]:
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}')
            return redirect('dashboard:order_detail', order_id=order_id)

    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'dashboard/order_detail.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def categories_list(request):
    """Categories management view"""
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'dashboard/categories.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def category_form(request, category_id=None):
    """Add/Edit category view"""
    category = None
    if category_id:
        category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        icon = request.POST.get('icon')
        is_active = request.POST.get('is_active') == 'on'

        if not name:
            messages.error(request, 'Category name is required.')
            return redirect('dashboard:categories')

        if category:
            category.name = name
            category.description = description
            category.icon = icon
            category.is_active = is_active
            category.save()
            messages.success(request, 'Category updated successfully!')
        else:
            Category.objects.create(
                name=name,
                description=description,
                icon=icon,
                is_active=is_active
            )
            messages.success(request, 'Category created successfully!')

        return redirect('dashboard:categories')

    items = []
    if category:
        items = category.items.all()
        
    context = {
        'category': category,
        'items': items
    }
    return render(request, 'dashboard/category_form.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def delete_category(request, category_id):
    """Delete category view"""
    category = get_object_or_404(Category, pk=category_id)
    category.delete()
    messages.success(request, f'Category "{category.name}" deleted successfully!')
    return redirect('dashboard:categories')


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def menu_items_list(request):
    """Menu items management view"""
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category')

    items = MenuItem.objects.all()

    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    if category_filter:
        items = items.filter(category_id=category_filter)

    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
    }
    return render(request, 'dashboard/menu_items.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def menu_item_form(request, item_id=None):
    """Add/Edit menu item view"""
    item = None
    if item_id:
        item = get_object_or_404(MenuItem, pk=item_id)

    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        image = request.FILES.get('image')

        if not all([category_id, name, price]):
            messages.error(request, 'Category, name, and price are required.')
            return redirect('dashboard:menu_items')

        try:
            category = Category.objects.get(pk=category_id)

            if item:
                item.category = category
                item.name = name
                item.description = description
                item.price = price
                item.is_available = is_available
                item.is_featured = is_featured
                if image:
                    item.image = image
                item.save()
                messages.success(request, 'Menu item updated successfully!')
            else:
                MenuItem.objects.create(
                    category=category,
                    name=name,
                    description=description,
                    price=price,
                    is_available=is_available,
                    is_featured=is_featured,
                    image=image
                )
                messages.success(request, 'Menu item created successfully!')

            return redirect('dashboard:menu_items')
        except Category.DoesNotExist:
            messages.error(request, 'Selected category does not exist.')

    initial_category_id = request.GET.get('category')
    categories = Category.objects.all()
    context = {
        'item': item,
        'categories': categories,
        'initial_category_id': initial_category_id,
    }
    return render(request, 'dashboard/menu_item_form.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def delete_menu_item(request, item_id):
    """Delete menu item view"""
    item = get_object_or_404(MenuItem, pk=item_id)
    item_name = item.name
    item.delete()
    messages.success(request, f'Menu item "{item_name}" deleted successfully!')
    return redirect('dashboard:menu_items')


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def users_list(request):
    """Users management view"""
    search_query = request.GET.get('search', '')

    users = User.objects.all()

    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    users = users.order_by('-date_joined')
    context = {
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'dashboard/users.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def search(request):
    """Global search view across orders, menu items, and users"""
    query = request.GET.get('q', '').strip()

    order_results = []
    menu_results = []
    user_results = []

    if query:
        order_results = Order.objects.filter(
            Q(order_number__icontains=query) |
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(address__icontains=query)
        ).order_by('-created_at')[:20]

        menu_results = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).select_related('category')[:20]

        user_results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).order_by('-date_joined')[:20]

    context = {
        'query': query,
        'order_results': order_results,
        'menu_results': menu_results,
        'user_results': user_results,
        'total_results': len(order_results) + len(menu_results) + len(user_results),
    }
    return render(request, 'dashboard/search.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def reports(request):
    """Sales reports view — date-wise filtering with chart data"""
    start_date_str = request.GET.get('start_date', '')
    end_date_str = request.GET.get('end_date', '')

    today = timezone.now().date()
    
    start_date = None
    end_date = None

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = None
            end_date = None

    # Default to last 30 days if no valid range provided
    if not start_date or not end_date:
        start_date = today - timedelta(days=29)
        end_date = today
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

    # Filter orders for the selected range
    orders = Order.objects.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

    # Core statistics - Filter for successful/revenue-generating statuses
    revenue_statuses = ['confirmed', 'preparing', 'ready', 'out_for_delivery', 'delivered']
    revenue_orders = orders.filter(status__in=revenue_statuses)

    total_sales = revenue_orders.aggregate(total=Sum('total_price'))['total'] or 0
    total_orders = orders.count()
    revenue_orders_count = revenue_orders.count()
    avg_order_value = float(total_sales) / revenue_orders_count if revenue_orders_count > 0 else 0

    # Orders by status — compute percentage for progress bars in Python
    orders_by_status = []
    for status_val, status_label in Order.STATUS_CHOICES:
        count = orders.filter(status=status_val).count()
        pct = round((count / total_orders * 100), 1) if total_orders > 0 else 0
        orders_by_status.append({
            'label': status_label,
            'value': status_val,
            'count': count,
            'pct': pct,
        })

    # Top selling items for the date range - only from revenue-generating orders
    top_items = OrderItem.objects.filter(order__in=revenue_orders).values(
        'item__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('price') * F('quantity'))
    ).order_by('-total_quantity')[:10]

    # Daily sales chart data for the date range
    chart_labels = []
    chart_data = []
    
    delta = end_date - start_date
    num_days = delta.days + 1
    
    # If range is too wide, group by week instead
    if num_days <= 31:
        for i in range(num_days):
            d = start_date + timedelta(days=i)
            day_sales = revenue_orders.filter(created_at__date=d).aggregate(
                total=Sum('total_price')
            )['total'] or 0
            chart_labels.append(d.strftime('%b %d'))
            chart_data.append(float(day_sales))
    else:
        # Weekly grouping
        current = start_date
        while current <= end_date:
            week_end = min(current + timedelta(days=6), end_date)
            week_sales = revenue_orders.filter(
                created_at__date__gte=current,
                created_at__date__lte=week_end
            ).aggregate(total=Sum('total_price'))['total'] or 0
            chart_labels.append(current.strftime('%b %d'))
            chart_data.append(float(week_sales))
            current = week_end + timedelta(days=1)

    context = {
        'total_sales': float(total_sales),
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'orders_by_status': orders_by_status,
        'top_items': top_items,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'dashboard/reports.html', context)


@login_required(login_url='accounts:login')
@user_passes_test(is_admin)
def analytics_data(request):
    """AJAX endpoint returning JSON analytics data for chart refresh"""
    today = timezone.now().date()
    period = request.GET.get('period', '7')

    try:
        days = int(period)
    except ValueError:
        days = 7

    labels = []
    data = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        sales = Order.objects.filter(
            created_at__date=d,
            status__in=['confirmed', 'preparing', 'ready', 'out_for_delivery', 'delivered']
        ).aggregate(total=Sum('total_price'))['total'] or 0
        labels.append(d.strftime('%b %d'))
        data.append(float(sales))

    return JsonResponse({'labels': labels, 'data': data})
