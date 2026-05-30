from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Category, MenuItem, Review
from accounts.forms import ReviewForm


def home(request):
    """Homepage view"""
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True)[:6]
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'featured_items': featured_items,
        'categories': categories,
    }
    return render(request, 'menu/home.html', context)


def menu_list(request):
    """Menu page with all items"""
    categories = Category.objects.filter(is_active=True)
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    
    items = MenuItem.objects.filter(is_available=True)
    
    if category_id:
        items = items.filter(category_id=category_id)
    
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'items': items,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'menu/menu.html', context)


def menu_detail(request, pk):
    """Menu item detail view"""
    item = get_object_or_404(MenuItem, pk=pk, is_available=True)
    reviews = item.reviews.all()
    related_items = MenuItem.objects.filter(category=item.category, is_available=True).exclude(pk=pk)[:3]
    
    context = {
        'item': item,
        'reviews': reviews,
        'related_items': related_items,
        'avg_rating': sum([r.rating for r in reviews]) / len(reviews) if reviews else 0,
    }
    
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        context['user_review'] = user_review
        context['can_review'] = True
    
    return render(request, 'menu/detail.html', context)


@login_required(login_url='accounts:login')
def add_review(request, pk):
    """Add review for a menu item"""
    item = get_object_or_404(MenuItem, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.item = item
            review.save()
            messages.success(request, 'Your review has been posted!')
            return redirect('menu:detail', pk=pk)
    else:
        form = ReviewForm()
    
    return render(request, 'menu/add_review.html', {'form': form, 'item': item})

