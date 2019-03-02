import json
import datetime
import copy
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.db.models import Manager as GeoManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + datetime.timedelta(days=n)

def stringify_date(date):
    return str(date.strftime("%Y-%m-%d"))

def decode_tags(tags):
    result = json.loads(tags)
    if isinstance(result, list):
        return result
    else:
        return [result]


class Volunteer(models.Model):
    ''' Volunteer is a profile model for a user '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmed_email = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('volunteer')
        verbose_name_plural = _('volunteers')
        db_table = 'volunteer'


class Shop(models.Model):
    name = models.CharField(max_length=500, verbose_name=_('name'))
    address = models.CharField(max_length=500, verbose_name=_('address'))
    city = models.CharField(max_length=500, verbose_name=_('city'))
    location = gis_models.PointField(
        geography=True, blank=True, null=True,
        verbose_name=_('location'))
    tags = models.CharField(max_length=500, default='[]') # Tags array as json
    withdrawn = models.BooleanField(default=False)
    objects = GeoManager()

    def __str__(self):
        return self.name

    def get_location(self):
        return self.location


    def serialize(self):
        data = {
            'id' : self.id,
            'name' : self.name,
            'address' : self.address,
            'lng' : float(self.location.x),
            'lat' : float(self.location.y),
            'tags' : decode_tags(str(self.tags)),
            'withdrawn' : self.withdrawn,
            'extraData' : {
                'city' : self.city
            }
        }

        return data

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')


class Category(models.Model):
    category_name = models.CharField(
        max_length=200, verbose_name=_('category_name'))
    category_description = models.CharField(
        max_length=200, default='', verbose_name=_('category_description'))
    image = models.ImageField()

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'category'

class Registration(models.Model):
    name = models.CharField(
        max_length=1000, verbose_name=_('name'))
    product_description = models.CharField(
        max_length=10000, verbose_name=_('product_discription'))
    image = models.ImageField(blank=True, null=True,
                              verbose_name=_('image'))
    image_url = models.CharField(max_length=500, null=True,
                                 verbose_name=_('image_url'))

    date_of_registration = models.DateField(default=datetime.date.today)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    withdrawn = models.BooleanField(default=False)
    tags = models.CharField(max_length=10000, default='[]', verbose_name=_('tags'))

    def __str__(self):
        return self.product_description

    @property
    def location(self):
        return self.shop.location

    def serialize(self):
        data = {
            'id' : self.id,
            'name' : self.name,
            'description' : self.product_description,
            'category' : str(self.category),
            'tags' : decode_tags(self.tags),
            'withdrawn' : self.withdrawn,
            'extraData' : {
                'prices' : self.prices_list
            }
        }
        return data

    @property
    def prices(self):
        return self.registrationprice_set.all()

    @property
    def prices_list(self):
        return [float(p) for p in self.registrationprice_set.values_list('price', flat=True)]

    @property
    def stars(self):
        r = self.rating_set.all().aggregate(models.Avg('stars'))['stars__avg']
        if r is None:
            return 0
        else:
            return r

    @stars.getter
    def stars(self):
        r = self.rating_set.all().aggregate(models.Avg('stars'))['stars__avg']
        if r is None:
            return 0
        else:
            return r

    @property
    def ratings(self):
        return self.rating_set.all().order_by('-stars')

    @property
    def questions(self):
        return self.question_set.all()

    class Meta:
        verbose_name = _('registration')
        verbose_name_plural = _('registrations')


class RegistrationPrice(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name=_('price'))
    date_from = models.DateField()
    date_to = models.DateField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    def serialize_interval(self, point=None):
        data = self.serialize(point=point)

        result = []

        for date in daterange(self.date_from, self.date_to):
            temp = copy.deepcopy(data)
            temp['date'] = stringify_date(date)
            result.append(temp)

        return result


    def serialize(self, point=None):
        if point == None:
            distance = -1
        else:
            distance = self.shop.location.distance(point) * 100
        data = {
            'price' : float(self.price),
            'productName' : self.registration.name,
            'productId' : self.registration.id,
            'productTags' : decode_tags(self.registration.tags),
            'shopId' : self.shop.id,
            'shopName' : self.shop.name,
            'shopTags' : decode_tags(self.shop.tags),
            'shopAddress' : self.shop.address,
            'shopDist' : distance
        }
        return data


class Rating(models.Model):
    stars = models.IntegerField(verbose_name=_('stars'))
    validity_of_this_rate = models.IntegerField(
        verbose_name=_('validity_of_this_rate'))
    rate_explanation = models.CharField(max_length=1000,
                                        verbose_name=_('rate_explanation'))
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.stars)

    @property
    def rating_range(self):
        return range(int(self.stars))

    @property
    def rating_range_inv(self):
        return range(5 - int(self.stars))

    class Meta:
        verbose_name = _('rating')
        verbose_name_plural = _('ratings')


class Question(models.Model):
    question_text = models.CharField(max_length=2000,
                                     verbose_name=_('question_text'))
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

    @property
    def answers(self):
        return self.answer_set.all()

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')


class Answer(models.Model):
    answer_text = models.CharField(max_length=2000,
                                   verbose_name=_('answer_text'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = _('answer')
        verbose_name_plural = _('answers')


class Report(models.Model):
    report_text = models.CharField(max_length=2000,
                                   verbose_name=_('answer_text'))
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.report_text

    class Meta:
        verbose_name = _('report')
        verbose_name_plural = _('reports')

class Favorite(models.Model):
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('favorite')
        verbose_name_plural = _('favorites')
        unique_together = ["registration", "volunteer"]
