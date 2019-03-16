from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django import forms


class Posts(models.Model):
    yayinlayan = models.ForeignKey(User, related_name='yayinlayan', default=1, on_delete=True)
    baslik = models.CharField(max_length=30, blank=False, help_text='İçeriğinize başlık ekleyin',
                              verbose_name='Başlık')
    icerik = models.TextField(max_length=1500, blank=False,
                              help_text='Filmi aklınızda kalan tüm ayrıntılarıyla anlatmaya çalışın',
                              verbose_name='İçerik')
    tarih = models.DateTimeField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(null=True, unique=True, editable=False)

    def __str__(self):
        return '%s' % self.baslik

    class Meta:
        verbose_name_plural = 'Gönderiler'
        ordering = ['-id']

    def get_slug(self):
        slug = slugify(unidecode(self.baslik))
        new_slug = slug
        num = 1
        while Posts.objects.filter(slug=new_slug).exists():
            num += 1
            new_slug = '%s-%s' % (slug, num)
        return new_slug

    def save(self, *args, **kwargs):
        if self.id is not None:
            self.slug = self.get_slug()
        else:
            cur_slug = Posts.objects.filter(slug=self.slug)
            if cur_slug != self.slug:
                self.slug = self.get_slug()
        super(Posts, self).save(*args, **kwargs)

    def get_comments(self):
        return self.comment.all()


class Comments(models.Model):
    post = models.ForeignKey(Posts, related_name='comment', on_delete=True)
    k_adi = models.CharField(max_length=50, editable=False, default=1)
    yorum = models.TextField(max_length=1000, blank=False, null=True, verbose_name='Yorumunuz')
    time = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.post

    class Meta:
        verbose_name_plural = 'Yorumlar'


class ContactUs(models.Model):
    choices = (('None', 'Lütfen mesajınıza uygun başlık seçin'), ('oneri', 'Öneri'), ('sikayet', 'Şikayet'))
    secenek = models.CharField(choices=choices, max_length=10, default='None')
    mesaj = models.TextField(max_length=1000, blank=False, null=True)
    k_adi = models.CharField(max_length=50, editable=False, default=1)

    def __str__(self):
        return '%s tarafından %s' % (self.k_adi, self.secenek)

    class Meta:
        verbose_name_plural = 'İletişim'
