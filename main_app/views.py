from django.shortcuts import render, HttpResponseRedirect, reverse
from user.forms import registerForm


def deneme(request):
    selam = 'selam'
    return render(request, template_name='main-temp.html', context={'selam': selam})



