from django.shortcuts import render
from django.views import View
from .models import Cart
from django.db.models import F


class ViewCart(View):
   def get(self, request):
       cart = Cart.objects.filter(user=request.user).annotate(
           total_price=F('product__price') * F('quantity')
       )
       return render(request, 'cart/cart.html', {"data": cart})


class ViewWishlist(View):
   def get(self, request):
       return render(request, 'cart/wishlist.html')
