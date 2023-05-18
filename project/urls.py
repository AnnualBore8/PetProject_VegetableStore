"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.utils.translation import activate
from django.conf import settings
print(settings.LANGUAGE_COOKIE_NAME)


def switch_language(request):
    new_language = request.GET.get('language')
    # request.session['django_language'] = new_language
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, new_language)
    # activate(new_language)
    # Перенаправление пользователя на предыдущую страницу
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('other/', include('apps.other.urls')),
    path('', include('apps.home.urls')),
    path('cart/', include('apps.cart.urls')),
    path('shop/', include('apps.shop.urls')),
    path('checkout/', include('apps.checkout.urls')),
    path('blog/', include('apps.blog.urls')),
    path('login/', include('apps.login.urls')),
    path('', include('social_django.urls', namespace='social')),
    path('switch-language/', switch_language, name='switch_language')
]
