from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from .models import Posts, Comments, Notifications
from .forms import PostsModel, CommentModel, ContactForms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, HttpResponse
from user.models import Roles
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import omdb
import config


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
    if not request.user.is_authenticated:
        return render(request, template_name='posts.html',
                      context={'gonderi': post, 'contactForm': contact, })
    notifications = Notifications.objects.filter(user=request.user).order_by('-created')[:5]
    return render(request, template_name='posts.html',
                  context={'gonderi': post, 'contactForm': contact, 'msg': notifications})


@login_required(login_url='/kullanici/giris-yap')
def post_create(request):
    contact = ContactForms(request.POST or None)
    form = PostsModel(data=request.POST or None)
    notifications = Notifications.objects.filter(user=request.user).order_by('-created')[:5]
    puan = get_object_or_404(Roles, user=request.user)
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]
    if form.is_valid():
        pk = form.save(commit=False)
        pk.yayinlayan = request.user

        puan.puan += 5
        puan.check_role()
        puan.save()

        pk.get_last_slug()
        form.save()

        msg = "%s adlı gönderin başarıyla oluşturuldu." % pk.baslik
        messages.add_message(request, messages.SUCCESS, message=msg, extra_tags='success')

        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': pk.slug}))
    return render(request, 'post-create.html',
                  context={'createForm': form, 'contactForm': contact, 'msg': notifications,
                           'old_posts': eski_gonderi})


def post_detail(request, slug):
    contact = ContactForms(request.POST or None)
    yorum = CommentModel(request.POST or None)
    post = get_object_or_404(Posts, slug=slug)
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]

    try:
        request.session['post-%s' % slug]
    except KeyError:
        request.session['post-%s' % slug] = True
        post.views_count += 1
        post.save()
    if not request.user.is_authenticated:
        return render(request, 'post-detail.html',
                      context={'post': post, 'yorumForm': yorum, 'contactForm': contact, 'old_posts': eski_gonderi})

    user_role = get_object_or_404(Roles, user=request.user).role
    notifications = Notifications.objects.filter(user=request.user).order_by('-created')[:5]
    return render(request, 'post-detail.html',
                  context={'post': post, 'yorumForm': yorum, 'contactForm': contact, 'msg': notifications,
                           'role': user_role,
                           'old_posts': eski_gonderi})


@login_required(login_url='/kullanici/giris-yap')
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
        if post.yayinlayan != pk.sahip:
            message = "<b>%s</b> adlı gönderine <b>%s</b> adlı kullanıcı yorum yaptı." % (post.baslik, pk.k_adi)
            Notifications.objects.create(user=post.yayinlayan, message=message, notification_type='comment',
                                         which_post_slug=post.slug)
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
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = request.user
    com = get_object_or_404(Comments, id=id)
    if user in com.likes.all():
        com.likes.remove(user)
    else:
        com.likes.add(user)
        if com.sahip != user:
            message = "<b>%s</b> yorumunu beğendi:<br>%s" % (user.username, com.yorum)
            Notifications.objects.create(user=com.sahip, message=message, notification_type='like',
                                         which_post_slug=com.post.slug)
    like_count = com.likes.all().count()
    return HttpResponse(like_count)


@login_required(login_url='/kullanici/giris-yap')
def report_post(request, slug):
    user = request.user
    post = get_object_or_404(Posts, slug=slug)
    if user in post.report.all():
        post.report.remove(user)
    else:
        post.report.add(user)
        if post.report.all().count() > 10:
            for admin in User.objects.filter(role_user__role=6):
                msg = "Bu gönderi %s kez rapor edildi! Kontrol etmen gerekiyor." % post.report.all().count()
                Notifications.objects.create(user=admin, message=msg,
                                             notification_type='report', which_post_slug=post.slug)
    report_count = post.report.all().count()
    return HttpResponse(report_count)


def report(request, slug, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = request.user
    com = get_object_or_404(Comments, id=id)
    if user in com.reports.all():
        com.reports.remove(user)
    else:
        com.reports.add(user)
        report_count = com.reports.all().count()
        # --------> rapor sayısını düzelt
        if report_count > 0:
            for admin in User.objects.filter(role_user__role=6):
                msg = "Bir yorum %s kez rapor edildi! Kontrol etmen gerekiyor.<br>-->%s" % (report_count, com.yorum)
                Notifications.objects.create(user=admin, message=msg,
                                             notification_type='report', which_post_slug=com.post.slug)
    report_count = com.reports.all().count()
    return HttpResponse(report_count)


@login_required(login_url='/kullanici/giris-yap')
def that_movie(request, slug, id):
    post = get_object_or_404(Posts, slug=slug)
    com = get_object_or_404(Comments, id=id)
    role = get_object_or_404(Roles, user=com.sahip)
    user = request.user

    if post.yayinlayan == user:
        if com.that_movie == 0:
            com.that_movie = 1
            com.save()

            com.sahip.profil.buldugu_film += 1
            com.sahip.profil.save()

            role.puan += 10
            role.check_role()
            role.save()

            post.found = 1
            post.save()

            for followers in post.followers.all():
                msg = "Takip ettiğin <b>%s</b> başlıklı gönderideki film bulundu!" % post.baslik
                Notifications.objects.create(user=followers, message=msg,
                                             notification_type='movieFound', which_post_slug=post.slug)
        else:
            com.that_movie = 0
            post.found = 0
            post.save()
            com.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))
    else:
        return HttpResponseForbidden()


@login_required(login_url='/kullanici/giris-yap')
def follow(request, slug):
    user = request.user
    post = get_object_or_404(Posts, slug=slug)
    if user in post.followers.all():
        post.followers.remove(user)
    else:
        post.followers.add(user)
        message = "<b>%s</b> adlı kullanıcı gönderini takip ediyor." % user.username
        Notifications.objects.create(user=post.yayinlayan, message=message, notification_type='follow',
                                     which_post_slug=post.slug)
    follow_count = post.followers.all().count()
    return HttpResponse(follow_count)


@login_required(login_url='/kullanici/giris-yap')
def delete_post(request, slug):
    post = get_object_or_404(Posts, slug=slug)
    if request.user == post.yayinlayan:
        post.delete()
        return HttpResponseRedirect(reverse('gonderiler'))
    else:
        return HttpResponseForbidden()


@login_required(login_url='/kullanici/giris-yap')
def edit_post(request, slug):
    contact = ContactForms(request.POST or None)
    mess = Notifications.objects.filter(user=request.user).order_by('-created')[:5]
    post = get_object_or_404(Posts, slug=slug)
    form = PostsModel(instance=post, data=request.POST or None)
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]
    if request.user == post.yayinlayan:
        if form.is_valid():
            form.save()
            msg = "%s adlı gönderin başarıyla güncellendi." % post.baslik
            messages.add_message(request, messages.SUCCESS, message=msg, extra_tags='success')
            return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))
    elif request.user != post.yayinlayan:
        return HttpResponseForbidden()
    return render(request, 'post-edit.html', context={'form': form, 'post': post, 'msg': mess, 'post_old': eski_gonderi,
                                                      'contactForm': contact})


@login_required(login_url='/kullanici/giris-yap')
def delete_comment(request, pk, slug):
    comment = get_object_or_404(Comments, pk=pk)
    user_role = get_object_or_404(Roles, user=request.user).role
    if request.user == comment.sahip or user_role == 6:
        comment.delete()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))
    else:
        return HttpResponseForbidden()


omdb.set_default('apikey', config.OMDB_API_KEY)
omdb.set_default('tomatoes', True)
omdb.set_default('fullplot', True)


def movie(request, movie_name):
    movie = omdb.get(title=movie_name)
    title = movie['title']
    year = movie['year']
    released = movie['released']
    runtime = movie['runtime']
    genre = movie['genre']
    director = movie['director']
    writer = movie['writer']
    actors = movie['actors'].split(',')
    plot = movie['plot']
    country = movie['country']
    awards = movie['awards']
    poster = movie['poster']
    metascore = movie['metascore']
    imdb = movie['imdb_rating']
    imdb_id = movie['imdb_id']
    tomato = movie['tomato_rating']
    return render(request, 'movie-detail.html',
                  context={'title': title, 'year': year, 'released': released, 'runtime': runtime,
                           'genre': genre, 'director': director, 'writer': writer, 'actors': actors,
                           'plot': plot, 'country': country, 'awards': awards, 'poster': poster, 'metascore': metascore,
                           'imdb': imdb, 'imdb_id': imdb_id, 'tomato': tomato})


def search_movie(request, movie_name):
    movie = omdb.search_movie(movie_name)
    list = []
    for i in movie:
        list.append(i['title'])
        list.append(i['year'])
        list.append(i['poster'])
        list.append(i['imdb_id'])

    return JsonResponse(list, safe=False)
