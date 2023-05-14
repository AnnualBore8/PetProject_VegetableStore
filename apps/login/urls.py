from django.urls import path
from .views import LoginView, SingUpView, LogoutView

app_name = "login"

urlpatterns = [
   path('', LoginView.as_view(), name="login"),
   path('singup/', SingUpView.as_view(), name="singup"),
   path('logout/', LogoutView.as_view(), name="logout"),
]