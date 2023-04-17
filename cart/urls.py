from django.urls import path
from .views import ViewCart, ViewWishlist

app_name = 'cart'

urlpatterns = [
   path('', ViewCart.as_view(), name='cart'),
   path('wishlist/', ViewWishlist.as_view(), name='wishlist'),
]
