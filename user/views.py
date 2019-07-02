from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from user.forms import registerForm, loginForm, profilModel, ChangePhotoForm, PasswordChange
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import kullaniciProfili
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.contrib import messages
from user.models import Roles
from main_app.models import Notifications, Posts
from datetime import datetime
import re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('gonderiler'))
    form = registerForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        kullaniciProfili.objects.create(profil=user, date_joined=datetime.now(), k_adi2=username)
        Roles.objects.create(user=user, role='1', puan=0)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                msg = "Profiline hoşgeldin! Buradan profilini güncelleyebilirsin."
                messages.add_message(request, message=msg, extra_tags='info', level=messages.INFO)
                return HttpResponseRedirect(reverse('settings', kwargs={'username': username}))
    return render(request, 'register.html', context={'registerForm': form})


def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('gonderiler'))
    form = loginForm(data=request.GET or None)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        print(username)
        if re.match(regex, username):
            try:
                user_email = User.objects.get(email=username)
                username = user_email.username
            except:
                messages.add_message(request, messages.ERROR, "Girdiğiniz email sistemde kayıtlı değil.",
                                     extra_tags='danger')
                return render(request, 'login.html', context={'loginForm': form})
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('gonderiler'))
        else:
            messages.add_message(request, messages.ERROR, 'Kullanıcı adı veya şifre hatalı!', extra_tags='danger')
    return render(request, 'login.html', context={'loginForm': form})


def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main-page'))


@login_required(login_url='/kullanici/giris-yap')
def profile_photo_change(request, username):
    profil = get_object_or_404(User, username=username)
    form = ChangePhotoForm(data=request.POST or None, files=request.FILES or None)
    if form.is_valid():
        photo = form.cleaned_data.get('profilFoto')
        profil.profil.profilFoto = photo
        profil.profil.save()
        return HttpResponseRedirect(reverse('profile-info', kwargs={'username': username}))
    return render(request, 'userprofile.html', context={'photoForm': form})


@login_required(login_url='/kullanici/giris-yap')
def choose_photo(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        choosen = request.POST.get('select')
        user.profil.choose_photo = int(choosen)
        user.profil.profilFoto = user.profil.get_choose_photo_display()
        user.profil.save()
        return HttpResponseRedirect(reverse('profile-info', kwargs={'username': username}))
    return HttpResponseRedirect(reverse('profile-info', kwargs={'username': username}))


@login_required(login_url='/kullanici/giris-yap')
def password_change(request):
    passwordForm = PasswordChange(user=request.user, data=request.POST or None)
    if passwordForm.is_valid():
        if request.method == "GET":
            return HttpResponseBadRequest()
        user = passwordForm.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Şifreniz başarıyla değiştirildi!', extra_tags='success')
        return HttpResponseRedirect(reverse('profile-info', kwargs={'username': request.user.username}))
    else:
        msg = "Lütfen girdiğiniz bilgileri kontrol edin."
        messages.add_message(request, messages.ERROR, message=msg, extra_tags='danger')
        return HttpResponseRedirect(reverse('profile-info', kwargs={'username': request.user.username}))


@login_required(login_url='/kullanici/giris-yap')
def profile_settings(request, username):
    user = get_object_or_404(User, username=username)
    notifications = Notifications.objects.filter(is_read=False, user=user).count()
    editprof = profilModel(instance=user.profil, data=request.POST or None, files=request.FILES or None)
    passwordForm = PasswordChange(user=request.user, data=request.POST or None)
    form = ChangePhotoForm(data=request.POST or None, files=request.FILES or None)
    Profil = get_object_or_404(User, username=username)
    if editprof.is_valid():
        if request.method == "GET":
            return HttpResponseBadRequest()
        ad = editprof.cleaned_data.get('ad', None)
        soyad = editprof.cleaned_data.get('soyad', None)
        film = editprof.cleaned_data.get('fav_film', None)
        yonet = editprof.cleaned_data.get('fav_yonetmen', None)
        dogum_tarihi = editprof.cleaned_data.get('dogum_gunu', None)
        try:
            cinsiyet = request.POST['cinsiyet']
        except:
            cinsiyet = ""

        Profil.profil.ad = ad
        Profil.profil.soyad = soyad
        Profil.profil.fav_film = film
        Profil.profil.fav_yonetmen = yonet
        Profil.profil.dogum_gunu = dogum_tarihi
        Profil.profil.cinsiyet = cinsiyet

        if not Profil.profil.is_updated:
            Profil.profil.is_updated = 1
            Profil.role_user.puan += 20
            Profil.role_user.save()

        Profil.profil.save()
        msg = "Profil bilgileriniz güncellendi."
        messages.add_message(request, messages.SUCCESS, message=msg, extra_tags='success')
        return HttpResponseRedirect(reverse('profile-info', kwargs={'username': username}))
    return render(request, 'profile-tabs/edit-profile.html',
                  context={'profil': Profil, 'editForm': editprof, 'photoForm': form, 'passwordForm': passwordForm,
                           'msg': notifications})


def profile_info(request, username):
    Profil = get_object_or_404(User, username=username)
    form_photo = ChangePhotoForm(data=request.POST or None, files=request.FILES or None)
    if not request.user.is_authenticated:
        return render(request, 'profile-tabs/user-info.html',
                      context={'profil': Profil, 'photoForm': form_photo})
    notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'profile-tabs/user-info.html',
                  context={'profil': Profil, 'msg': notifications, 'photoForm': form_photo})


def my_posts(request, username):
    Profil = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=username)
    posts = Posts.objects.filter(yayinlayan=user)
    form_photo = ChangePhotoForm(data=request.POST or None, files=request.FILES or None)

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 8)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    if not request.user.is_authenticated:
        return render(request, 'profile-tabs/myposts.html',
                      context={'posts': post, 'profil': Profil, 'photoForm': form_photo})
    notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'profile-tabs/myposts.html',
                  context={'posts': post, 'profil': Profil, 'msg': notifications, 'photoForm': form_photo})


@login_required(login_url='/kullanici/giris-yap')
def profile_notifications(request, username):
    notif = Notifications.objects.filter(user=request.user, is_read=False).count()
    notifications = Notifications.objects.filter(user=request.user).order_by('-created')
    Profil = get_object_or_404(User, username=username)
    form_photo = ChangePhotoForm(data=request.POST or None, files=request.FILES or None)
    page = request.GET.get('page', 1)
    paginator = Paginator(notifications, 8)

    if Profil.username == request.user.username:
        notifs = Notifications.objects.filter(user=request.user, is_read=False)
        if notifs:
            for i in notifs:
                i.is_read = True
                i.save()

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request, 'profile-tabs/profile-notifications.html',
                  context={'profil': Profil, 'msg': notif, 'notifications': post, 'photoForm': form_photo})


def bookmarks(request, username):
    Profil = get_object_or_404(User, username=username)
    bookmark = Posts.objects.filter(followers=Profil)
    form_photo = ChangePhotoForm(data=request.POST or None, files=request.FILES or None)

    page = request.GET.get('page', 1)
    paginator = Paginator(bookmark, 8)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    if not request.user.is_authenticated:
        return render(request, 'profile-tabs/bookmarks.html',
                      context={'bookmark': post, 'profil': Profil, 'photoForm': form_photo})

    notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'profile-tabs/bookmarks.html',
                  context={'bookmark': post, 'msg': notifications, 'profil': Profil, 'photoForm': form_photo})
