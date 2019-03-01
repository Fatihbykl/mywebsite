from django.db import models
from django.contrib.auth.models import User


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
