from django.shortcuts import render, HttpResponseRedirect, reverse
from user.forms import registerForm, loginForm
from django.contrib.auth import authenticate, login


def register(request):
    form = registerForm(data=request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('login-register'))
    return render(request, 'register.html', context={'registerForm': form})


def loginn(request):
    form = loginForm(data=request.POST or None)
    return render(request, 'login.html', context={'loginForm': form})
