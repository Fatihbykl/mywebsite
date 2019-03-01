# Generated by Django 2.1.7 on 2019-02-27 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baslik', models.CharField(help_text='İçeriğinize başlık ekleyin', max_length=30, verbose_name='Başlık')),
                ('icerik', models.TextField(help_text='Filmi aklınızda kalan tüm ayrıntılarıyla anlatmaya çalışın', max_length=1500, verbose_name='İçerik')),
                ('tarih', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(editable=False, null=True, unique=True)),
            ],
        ),
    ]