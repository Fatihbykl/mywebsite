from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from user.forms import registerForm, loginForm, profilModel
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import kullaniciProfili
from django.contrib.auth.models import User
from django.contrib import messages
from user.models import PasswordChange, Roles
from main_app.forms import ContactForms


def register(request):
    form = registerForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        kullaniciProfili.objects.create(profil=user)
        Roles.objects.create(user=user, role='1', puan=0)
        user.save()
        kullaniciProfili.k_adi2 = username
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
    contact = ContactForms(request.POST or None)
    passwordForm = PasswordChange(user=request.user, data=request.POST or None)
    profilForm = profilModel(request.POST or None)
    Profil = get_object_or_404(User, username=username)
    return render(request, 'userprofile.html',
                  context={'profil': Profil, 'editForm': profilForm, 'passForm': passwordForm, 'contactForm': contact})


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main-page'))


def edit_profile(request, username):
    Profil = get_object_or_404(User, username=username)
    editprof = profilModel(data=request.POST or None, files=request.FILES or None)
    if editprof.is_valid():
        ad = editprof.cleaned_data.get('ad', None)
        soyad = editprof.cleaned_data.get('soyad', None)
        film = editprof.cleaned_data.get('fav_film', None)
        yonet = editprof.cleaned_data.get('fav_yonetmen', None)
        foto = editprof.cleaned_data.get('profilFoto', None)

        if ad:
            Profil.profil.ad = ad
        if soyad:
            Profil.profil.soyad = soyad
        if film:
            Profil.profil.fav_film = film
        if yonet:
            Profil.profil.fav_yonetmen = yonet
        Profil.profil.save()
        return HttpResponseRedirect(reverse('profil', kwargs={'username': request.user.username}))
    return render(request, 'userprofile.html', context={'editForm': editprof})


def password_change(request):
    passwordForm = PasswordChange(user=request.user, data=request.POST or None)
    if passwordForm.is_valid():
        user = passwordForm.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Şifreniz başarıyla değiştirildi!', extra_tags='success')
        return HttpResponseRedirect(reverse('profil', kwargs={'username': request.user.username}))
    else:
        messages.error(request, 'Lütfen girdiğiniz bilgileri kontrol edin.', extra_tags='danger')
        return HttpResponseRedirect(reverse('profil', kwargs={'username': request.user.username}))
