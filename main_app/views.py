from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, HttpResponse
from .models import Posts, Comments
from .forms import PostsModel, CommentModel, ContactForms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest, JsonResponse
from user.models import Roles


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
    puan = get_object_or_404(Roles, user=request.user)
    if form.is_valid():
        pk = form.save(commit=False)
        pk.yayinlayan = request.user

        puan.puan += 5
        puan.check_role()
        puan.save()

        pk.get_last_slug()
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
    puan = get_object_or_404(Roles, user=request.user)
    yorum = CommentModel(request.POST or None)
    post = get_object_or_404(Posts, slug=slug)
    if yorum.is_valid():
        pk = yorum.save(commit=False)
        pk.post = post
        pk.sahip = request.user

        puan.puan += 2
        puan.check_role()
        puan.save()

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


def like(request, slug, id):
    user = request.user
    com = get_object_or_404(Comments, id=id)
    if user in com.likes.all():
        com.likes.remove(user)
    else:
        com.likes.add(user)
    return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))


def report_post(request, slug):
    user = request.user
    post = get_object_or_404(Posts, slug=slug)
    if user in post.report.all():
        post.report.remove(user)
    else:
        post.report.add(user)
    return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))


def report(request, slug, id):
    user = request.user
    com = get_object_or_404(Comments, id=id)
    if user in com.reports.all():
        com.reports.remove(user)
    else:
        com.reports.add(user)
    return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))


def that_movie(request, slug, id):
    post = get_object_or_404(Posts, slug=slug)
    com = get_object_or_404(Comments, id=id)
    role = get_object_or_404(Roles, user=com.sahip)
    user = request.user
    if post.yayinlayan == user:
        if com.that_movie == 0:
            com.that_movie = 1
            com.save()

            role.puan += 10
            role.check_role()
            role.save()

            post.found = 1
            post.save()
        else:
            com.that_movie = 0
            post.found = 0
            post.save()
            com.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))
    else:
        return HttpResponseRedirect(reverse('login'))


def follow(request, slug):
    user = request.user
    post = get_object_or_404(Posts, slug=slug)
    if user in post.followers.all():
        post.followers.remove(user)
    else:
        post.followers.add(user)
    return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))
