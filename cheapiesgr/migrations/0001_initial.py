# Generated by Django 2.1.2 on 2019-01-03 22:55

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.CharField(max_length=2000, verbose_name='answer_text')),
            ],
            options={
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, verbose_name='category_name')),
                ('category_description', models.CharField(max_length=200, verbose_name='category_description')),
                ('image', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=2000, verbose_name='question_text')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField(verbose_name='stars')),
                ('validity_of_this_rate', models.IntegerField(verbose_name='validity_of_this_rate')),
                ('rate_explanation', models.CharField(max_length=1000, verbose_name='rate_explanation')),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_description', models.CharField(max_length=10000, verbose_name='product_discription')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='image')),
                ('image_url', models.CharField(max_length=500, null=True, verbose_name='image_url')),
                ('date_of_registration', models.DateField()),
                ('withdrawn', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheapiesgr.Category')),
            ],
            options={
                'verbose_name': 'registration',
                'verbose_name_plural': 'registrations',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='name')),
                ('address', models.CharField(max_length=500, verbose_name='address')),
                ('city', models.CharField(max_length=500, verbose_name='city')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='location')),
            ],
            options={
                'verbose_name': 'shop',
                'verbose_name_plural': 'shops',
            },
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed_email', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'volunteer',
            },
        ),
        migrations.AddField(
            model_name='registration',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheapiesgr.Shop'),
        ),
        migrations.AddField(
            model_name='registration',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rating',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheapiesgr.Registration'),
        ),
        migrations.AddField(
            model_name='rating',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='registration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheapiesgr.Registration'),
        ),
        migrations.AddField(
            model_name='question',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheapiesgr.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
