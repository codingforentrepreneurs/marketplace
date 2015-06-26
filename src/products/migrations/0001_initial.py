# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import products.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=500)),
                ('slug', models.SlugField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'products/image/')),
                ('title', models.CharField(max_length=120, null=True, blank=True)),
                ('featured_image', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(to='products.Category')),
            ],
            options={
                'verbose_name': 'Category Image',
                'verbose_name_plural': 'Category Images',
            },
        ),
        migrations.CreateModel(
            name='Featured',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('default', models.BooleanField(default=False)),
                ('jumbo_text', models.CharField(max_length=3000, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=180)),
                ('description', models.CharField(max_length=500)),
                ('download', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/Users/jmitch/Dropbox/cfeprojects/Marketplace/static/protected'), null=True, upload_to=products.models.download_loc)),
                ('price', models.DecimalField(max_digits=20, decimal_places=2)),
                ('sale_price', models.DecimalField(null=True, max_digits=20, decimal_places=2, blank=True)),
                ('slug', models.SlugField()),
                ('order', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-order'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'products/image/')),
                ('title', models.CharField(max_length=120, null=True, blank=True)),
                ('featured_image', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(to='products.Product')),
            ],
        ),
        migrations.AddField(
            model_name='featured',
            name='products',
            field=models.ManyToManyField(to='products.Product', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]
