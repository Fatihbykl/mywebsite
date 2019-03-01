from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from user.forms import registerForm, loginForm
from django.contrib.auth import authenticate, login, logout
from .models import kullaniciProfili
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):
    form = registerForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        kullaniciProfili.objects.create(profil=user)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('gonderiler'))
    return render(request, 'register.html', context={'registerForm': form})


def Login(request):
    form = loginForm()
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('gonderiler'))
    else:

        messages.error(request, "Kullanıcı adı veya şifreniz hatalı", extra_tags='danger')
    return render(request, 'login.html', context={'loginForm': form})


def profil(request, username):
    Profil = get_object_or_404(User, username=username)
    return render(request, 'userprofile.html', context={'profil': Profil})


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main-page'))
