from django.shortcuts import render, HttpResponseRedirect, reverse
from user.forms import registerForm
from .models import Posts
from .forms import PostsModel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def deneme(request):
    selam = 'selam'
    return render(request, template_name='main-temp.html', context={'selam': selam})


def post_views(request):
    post_list = Posts.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 12)

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request, template_name='posts.html', context={'gonderi': post})


def post_create(request):
    form = PostsModel(data=request.POST or None)
    if form.is_valid():
        title = form.cleaned_data['baslik']
        description = form.cleaned_data['icerik']
        Posts.objects.create(baslik=title, icerik=description, yayinlayan=request.user)
        return HttpResponseRedirect(reverse('gonderiler'))
    return render(request, 'post-create.html', context={'createForm': form})
