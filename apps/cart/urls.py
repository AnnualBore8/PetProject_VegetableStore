from django.urls import path
from .views import ViewCart, ViewWishlist, ViewCartDel

app_name = 'cart'

urlpatterns = [
   path('', ViewCart.as_view(), name='cart'),
   path('wishlist/', ViewWishlist.as_view(), name='wishlist'),
   path('del/<int:product_id>', ViewCartDel.as_view(), name='del'),
]
