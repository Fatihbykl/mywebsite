from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.shortcuts import reverse
from datetime import datetime


class Posts(models.Model):
    yayinlayan = models.ForeignKey(User, related_name='yayinlayan', default=1, on_delete=True)
    baslik = models.CharField(max_length=70, blank=False, help_text='İçeriğinize başlık ekleyin',
                              verbose_name='Başlık')
    icerik = models.TextField(max_length=2500, blank=False,
                              help_text='Filmi aklınızda kalan tüm ayrıntılarıyla anlatmaya çalışın',
                              verbose_name='İçerik')
    tarih = models.DateTimeField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(null=True, unique=True, editable=False)
    found = models.BooleanField(default=0)
    report = models.ManyToManyField(User, related_name='report')
    followers = models.ManyToManyField(User, related_name='followers')
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return 'Gönderi Başlığı : %s' % self.baslik

    class Meta:
        verbose_name_plural = 'Gönderiler'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    def get_slug(self):
        slug = slugify(unidecode(self.baslik))
        new_slug = slug
        num = 1
        while Posts.objects.filter(slug=new_slug).exists():
            num += 1
            new_slug = '%s-%s' % (slug, num)
        return new_slug

    def get_last_slug(self):
        if self.id is not None:
            self.slug = self.get_slug()
        else:
            cur_slug = Posts.objects.filter(slug=self.slug)
            if cur_slug != self.slug:
                self.slug = self.get_slug()

    def get_comments(self):
        return self.comment.all().order_by('-id')


class Comments(models.Model):
    post = models.ForeignKey(Posts, related_name='comment', on_delete=models.CASCADE)
    k_adi = models.CharField(max_length=50, editable=False, default=1)
    sahip = models.ForeignKey(User, related_name='sahip', on_delete=models.CASCADE)
    yorum = models.TextField(max_length=1000, blank=False, null=True, verbose_name='Yorumunuz')
    time = models.DateTimeField(auto_now_add=True, auto_now=False)
    likes = models.ManyToManyField(User, related_name='likes')
    reports = models.ManyToManyField(User, related_name='reports')
    that_movie = models.BooleanField(default=0)

    def __str__(self):
        return 'Başlık : {0} || Kullanıcı Adı: {1} || Beğeniler : {2} || Şikayetler : {3}'.format(self.post.baslik,
                                                                                                  self.k_adi,
                                                                                                  self.likes.all().count(),
                                                                                                  self.reports.all().count())

    class Meta:
        verbose_name_plural = 'Yorumlar'


class ContactUs(models.Model):
    choices = (('None', 'Lütfen mesajınıza uygun başlık seçin'), ('oneri', 'Öneri'), ('sikayet', 'Şikayet'))
    secenek = models.CharField(choices=choices, max_length=10, default='None')
    mesaj = models.TextField(max_length=1000, blank=False, null=True)
    k_adi = models.CharField(max_length=50, editable=False, default=1)

    def __str__(self):
        return 'Gönderen : %s || Tipi : %s' % (self.k_adi, self.secenek)

    class Meta:
        verbose_name_plural = 'İletişim'


class Notifications(models.Model):
    TYPE = (('comment', 'Yorum'), ('report', 'Rapor'), ('movieFound', 'Film Bulundu'),
            ('like', 'Beğeni'), ('follow', 'Takip'))
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=80)
    notification_type = models.CharField(choices=TYPE, max_length=20, default='like')
    which_post_slug = models.CharField(max_length=100, default='slug')

    def __str__(self):
        return "Kullanıcı: %s || Mesaj: %s || Tipi: %s" % self.user.username, self.message, self.notification_type

    def get_all_notifications(self):
        return self.objects.all()
