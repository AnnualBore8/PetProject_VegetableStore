from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


class LoginView(View):

    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home:index')
        return render(request, 'login/login.html', {"error": form.errors.get("__all__")})


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('home:index')


class SingUpView(View):

    def get(self, request):
        return render(request, 'login/singup.html')
