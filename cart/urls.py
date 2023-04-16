from django.urls import path
from .views import ViewCart

app_name = 'cart'

urlpatterns = [
   path('', ViewCart.as_view(), name='cart'),
]
