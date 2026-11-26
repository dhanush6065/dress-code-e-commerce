from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from wishlist.models import Wishlist, WishlistItem
from products.models import Product


@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    items = wishlist.items.select_related('product').all()

    return render(request, 'wishlist/wishlist.html', {
        'wishlist': wishlist,
        'items': items,
    })


@login_required
def add_to_wishlist(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        WishlistItem.objects.get_or_create(
            wishlist=wishlist,
            product=product
        )

    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, item_id):
    if request.method == 'POST':
        wishlist = get_object_or_404(Wishlist, user=request.user)

        item = get_object_or_404(
            WishlistItem,
            id=item_id,
            wishlist=wishlist
        )

        item.delete()

    return redirect('wishlist')