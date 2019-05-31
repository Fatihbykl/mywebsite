from django.shortcuts import render, reverse, HttpResponseRedirect, get_object_or_404
from .models import Posts, Comments, Notifications
from .forms import PostsModel, CommentModel, ContactForms, ReportForms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, HttpResponse
from user.models import Roles
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import omdb
import config
from googletrans import Translator


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
    if not request.user.is_authenticated:
        return render(request, template_name='posts.html', context={'gonderi': post})
    notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
    mess_count = Notifications.objects.filter(user=request.user, is_read=False).count()
    return render(request, template_name='posts.html',
                  context={'gonderi': post, 'msg': notifications, 'msgCount': mess_count})


@login_required(login_url='/kullanici/giris-yap')
def post_create(request):
    form = PostsModel(data=request.POST or None)
    notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
    puan = get_object_or_404(Roles, user=request.user)
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]
    last_comments = Comments.objects.all().order_by('-id')[:5]
    statistics = {
        'comment': Comments.objects.all().count(),
        'post': Posts.objects.all().count(),
        'found': Posts.objects.filter(found=0).count(),
        'users': User.objects.all().count(),
    }
    leaderboard = Roles().get_leaderboard_5()

    if form.is_valid():
        pk = form.save(commit=False)
        pk.yayinlayan = request.user

        puan.puan += 10
        puan.check_role()
        puan.save()

        pk.get_last_slug()
        form.save()

        msg = "%s adlı gönderin başarıyla oluşturuldu." % pk.baslik
        messages.add_message(request, messages.SUCCESS, message=msg, extra_tags='success')

        return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': pk.slug}))
    return render(request, 'post-create.html',
                  context={'createForm': form, 'msg': notifications,
                           'old_posts': eski_gonderi, 'last_comments': last_comments, 'statistics': statistics,
                           'leaderboard_5': leaderboard})


def post_detail(request, slug):
    yorum = CommentModel(request.POST or None)
    post = get_object_or_404(Posts, slug=slug)
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]
    last_comments = Comments.objects.all().order_by('-id')[:5]
    statistics = {
        'comment': Comments.objects.all().count(),
        'post': Posts.objects.all().count(),
        'found': Posts.objects.filter(found=0).count(),
        'users': User.objects.all().count(),
    }
    leaderboard = Roles().get_leaderboard_5()
    report_form = ReportForms(data=request.POST or None)
    try:
        choosen_comment = Comments.objects.get(post=post, that_movie=True)
    except:
        choosen_comment = False

    try:
        request.session['post-%s' % slug]
    except KeyError:
        request.session['post-%s' % slug] = True
        post.views_count += 1
        post.save()
    if not request.user.is_authenticated:
        return render(request, 'post-detail.html',
                      context={'post': post, 'yorumForm': yorum,
                               'old_posts': eski_gonderi,
                               'last_comments': last_comments, 'statistics': statistics, 'leaderboard_5': leaderboard})

    user_role = get_object_or_404(Roles, user=request.user).role
    notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
    comment_count = Comments.objects.filter(post=post).count()
    return render(request, 'post-detail.html',
                  context={'post': post, 'yorumForm': yorum, 'msg': notifications,
                           'role': user_role, 'reportForm': report_form, 'choosen_comment': choosen_comment,
                           'old_posts': eski_gonderi, 'comment_count': comment_count,
                           'last_comments': last_comments, 'statistics': statistics, 'leaderboard_5': leaderboard})


@login_required(login_url='/kullanici/giris-yap')
def comment(request, slug, sug_movie, movie_href):
    if request.method == 'GET':
        return HttpResponseBadRequest()
    puan = get_object_or_404(Roles, user=request.user)
    yorum = CommentModel(request.POST or None)
    post = get_object_or_404(Posts, slug=slug)
    if yorum.is_valid():
        pk = yorum.save(commit=False)
        pk.post = post
        pk.sahip = request.user
        pk.movie_tag = sug_movie
        pk.movie_tag_href = movie_href

        puan.puan += 5
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
    contact = ContactForms(data=request.POST or None)
    last_comments = Comments.objects.all().order_by('-id')[:5]
    statistics = {
        'comment': Comments.objects.all().count(),
        'post': Posts.objects.all().count(),
        'found': Posts.objects.filter(found=0).count(),
        'users': User.objects.all().count(),
    }
    leaderboard = Roles().get_leaderboard_5()
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]
    if contact.is_valid():
        if request.method == 'GET':
            return HttpResponseBadRequest()
        pk = contact.save(commit=False)
        if request.user.is_authenticated:
            pk.k_adi = request.user.username
            baslik = contact.cleaned_data['secenek']
            mesaj = contact.cleaned_data['mesaj']
            pk.secenek = baslik
            pk.mesaj = mesaj
            pk.email = request.user.email
            pk.ad = request.user.profil.ad
            pk.soyad = request.user.profil.soyad
            pk.save()
        else:
            pk.secenek = contact.cleaned_data['secenek']
            pk.mesaj = contact.cleaned_data['mesaj']
            pk.ad = contact.cleaned_data['ad']
            pk.soyad = contact.cleaned_data['soyad']
            pk.email = contact.cleaned_data['email']
            pk.save()
        return HttpResponseRedirect(reverse('gonderiler'))
    if not request.user.is_authenticated:
        return render(request, 'contact.html',
                      context={'contactForm': contact, 'leaderboard_5': leaderboard, 'old_posts': eski_gonderi,
                               'last_comments': last_comments,
                               'statistics': statistics})
    notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'contact.html',
                  context={'contactForm': contact, 'leaderboard_5': leaderboard, 'old_posts': eski_gonderi,
                           'last_comments': last_comments, 'msg': notifications,
                           'statistics': statistics})


def like(request, slug, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = request.user
    com = get_object_or_404(Comments, id=id)
    if user in com.likes.all():
        com.likes.remove(user)
        com.is_liked = 0
        com.save()
    else:
        com.likes.add(user)
        com.is_liked = 1
        com.save()
        if com.sahip != user:
            message = "<b>%s</b> yorumunu beğendi:<br>%s" % (user.username, com.yorum)
            Notifications.objects.create(user=com.sahip, message=message, notification_type='like',
                                         which_post_slug=com.post.slug)
    like_count = com.likes.all().count()
    return HttpResponse(like_count)


def report(request, slug, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    form = ReportForms(data=request.POST or None)
    user = request.user
    com = get_object_or_404(Comments, id=id)
    post = get_object_or_404(Posts, slug=slug)
    if form.is_valid():
        pk = form.save(commit=False)
        pk.reason = form.cleaned_data['reason']
        pk.comment = form.cleaned_data['comment']
        pk.which_post = slug
        pk.which_user = com.sahip.username
        pk.who = user.username
        pk.save()

        for admin in User.objects.filter(role_user__role=6):
            msg = "Rapor Özeti:<br> Raporlayan: %s <br>Raporlanan: %s <br> Neden: %s <br> Açıklama: %s" % (
            user.username, post.yayinlayan.username, pk.get_reason_display(), pk.comment)
            Notifications.objects.create(user=admin, message=msg, notification_type='report', which_post_slug=com.post.slug)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def report_post(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    form = ReportForms(data=request.POST or None)
    user = request.user
    post = get_object_or_404(Posts, slug=slug)
    if form.is_valid():
        pk = form.save(commit=False)
        pk.reason = form.cleaned_data['reason']
        pk.comment = form.cleaned_data['comment']
        pk.which_post = slug
        pk.which_user = post.yayinlayan.username
        pk.who = user.username
        pk.save()
        for admin in User.objects.filter(role_user__role=6):
            msg = "Rapor Özeti:<br> Raporlayan: %s <br>Raporlanan: %s <br> Neden: %s <br> Açıklama: %s" % (
                user.username, post.yayinlayan.username, pk.get_reason_display(), pk.comment)
            Notifications.objects.create(user=admin, message=msg, notification_type='report', which_post_slug=slug)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/kullanici/giris-yap')
def that_movie(request, slug, id):
    post = get_object_or_404(Posts, slug=slug)
    com = get_object_or_404(Comments, id=id)
    role = get_object_or_404(Roles, user=com.sahip)
    user = request.user

    if post.yayinlayan == user or request.user.role_user.role == 6:
        if com.that_movie == 0:
            com.that_movie = 1
            com.save()

            com.sahip.profil.buldugu_film += 1
            com.sahip.profil.save()

            role.puan += 25
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
    if request.user != post.yayinlayan:
        if user in post.followers.all():
            post.followers.remove(user)
        else:
            post.followers.add(user)
            message = "<b>%s</b> adlı kullanıcı gönderini takip ediyor." % user.username
            Notifications.objects.create(user=post.yayinlayan, message=message, notification_type='follow',
                                         which_post_slug=post.slug)
    return HttpResponse('')


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
    mess = Notifications.objects.filter(user=request.user).order_by('-created')[:5]
    post = get_object_or_404(Posts, slug=slug)
    form = PostsModel(instance=post, data=request.POST or None)
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]
    last_comments = Comments.objects.all().order_by('-id')[:5]
    statistics = {
        'comment': Comments.objects.all().count(),
        'post': Posts.objects.all().count(),
        'found': Posts.objects.filter(found=0).count(),
        'users': User.objects.all().count(),
    }
    leaderboard = Roles().get_leaderboard_5()

    if request.user == post.yayinlayan:
        if form.is_valid():
            form.save()
            msg = "%s adlı gönderin başarıyla güncellendi." % post.baslik
            messages.add_message(request, messages.SUCCESS, message=msg, extra_tags='success')
            return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': slug}))
    elif request.user != post.yayinlayan:
        return HttpResponseForbidden()
    return render(request, 'post-edit.html', context={'form': form, 'post': post, 'msg': mess, 'post_old': eski_gonderi,
                                                      'last_comments': last_comments,
                                                      'statistics': statistics, 'leaderboard_5': leaderboard})


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


def movie(request, imdb_id, movie_name):
    t = Translator()
    movie = omdb.get(imdbid=imdb_id)
    title = movie['title']
    year = movie['year']
    released_en = movie['released'].split(' ')
    released_t = t.translate(released_en[1], dest='tr').text.capitalize()
    released = released_en[0] + " " + released_t + " " + released_en[2]
    runtime = movie['runtime'].split(' ')[0]
    genre_en = movie['genre']
    genre = t.translate(genre_en, dest='tr').text.title()
    director = movie['director']
    writer = movie['writer']
    actors = movie['actors'].split(',')
    plot_en = movie['plot']
    plot = t.translate(plot_en, dest='tr').text
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


def scores(request):
    last_comments = Comments.objects.all().order_by('-id')[:5]
    statistics = {
        'comment': Comments.objects.all().count(),
        'post': Posts.objects.all().count(),
        'found': Posts.objects.filter(found=0).count(),
        'users': User.objects.all().count(),
    }
    r = Roles()
    leaderboard = r.get_leaderboard_full()
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]
    r_5 = r.get_leaderboard_5()
    page = request.GET.get('page', 1)
    paginator = Paginator(leaderboard, 5)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
        p = r.get_user_place(user=request.user)
        return render(request, 'score.html',
                      context={'leaderboard': post, 'leaderboard_5': r_5, 'last_comments': last_comments,
                               'statistics': statistics, 'msg': notifications,
                               'old_posts': eski_gonderi, 'user_place': p})

    return render(request, 'score.html',
                  context={'leaderboard': post, 'leaderboard_5': r_5, 'last_comments': last_comments,
                           'statistics': statistics,
                           'old_posts': eski_gonderi})


def rules(request):
    last_comments = Comments.objects.all().order_by('-id')[:5]
    statistics = {
        'comment': Comments.objects.all().count(),
        'post': Posts.objects.all().count(),
        'found': Posts.objects.filter(found=0).count(),
        'users': User.objects.all().count(),
    }
    leaderboard = Roles().get_leaderboard_5()
    eski_gonderi = Posts.objects.filter(found=0).order_by('tarih')[:5]
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(user=request.user, is_read=False).count()
        return render(request, 'rules.html',
                      context={'leaderboard_5': leaderboard, 'last_comments': last_comments, 'statistics': statistics,
                               'old_posts': eski_gonderi, 'msg': notifications})

    return render(request, 'rules.html',
                  context={'leaderboard_5': leaderboard, 'last_comments': last_comments, 'statistics': statistics,
                           'old_posts': eski_gonderi})
