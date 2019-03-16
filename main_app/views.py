from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from .models import Posts
from .forms import PostsModel, CommentModel, ContactForms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User

def deneme(request):
    selam = 'selam'
    return render(request, template_name='main-temp.html', context={'selam': selam})


def post_views(request):
    post_list = Posts.objects.all()
    contact = ContactForms(request.POST or None)
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 12)

    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)
    return render(request, template_name='posts.html', context={'gonderi': post, 'contactForm': contact})


def post_create(request):
    contact = ContactForms(request.POST or None)
    form = PostsModel(data=request.POST or None)
    if form.is_valid():
        pk = form.save(commit=False)
        pk.yayinlayan = request.user
        form.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': pk.slug}))
    return render(request, 'post-create.html', context={'createForm': form, 'contactForm': contact})


def post_detail(request, slug):
    contact = ContactForms(request.POST or None)
    yorum = CommentModel(request.POST or None)
    post = get_object_or_404(Posts, slug=slug)
    return render(request, 'post-detail.html', context={'post': post, 'yorumForm': yorum, 'contactForm': contact})


def comment(request, slug):
    if request.method == 'GET':
        return HttpResponseBadRequest
    yorum = CommentModel(request.POST or None)
    post = get_object_or_404(Posts, slug=slug)
    if yorum.is_valid():
        pk = yorum.save(commit=False)
        pk.post = post
        pk.k_adi = request.user.username
        pk.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))


def contact_us(request):
    if request.method == 'GET':
        return HttpResponseBadRequest
    contact = ContactForms(data=request.POST or None)
    if contact.is_valid():
        pk = contact.save(commit=False)
        pk.k_adi = request.user.username
        baslik = contact.cleaned_data['secenek']
        mesaj = contact.cleaned_data['mesaj']
        pk.secenek = baslik
        pk.mesaj = mesaj
        pk.save()
        return HttpResponseRedirect(reverse('gonderiler'))
    return HttpResponseRedirect(reverse('gonderiler'))


