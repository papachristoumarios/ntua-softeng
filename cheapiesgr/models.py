from django.db import models
from django.contrib.gis.db import models as gis_models
from django.db.models import Manager as GeoManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Volunteer(models.Model):
    ''' Volunteer is a profile model for a user '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmed_email = models.BooleanField(default=False)

    class Meta:
        db_table = 'volunteer'


class Shop(models.Model):
    name = models.CharField(max_length=500, verbose_name=_('name'))
    address = models.CharField(max_length=500, verbose_name=_('address'))
    city = models.CharField(max_length=500, verbose_name=_('city'))
    location = gis_models.PointField(
        geography=True, blank=True, null=True,
        verbose_name=_('location'))

    # update the manager
    objects = GeoManager()

    def __str__(self):
        return self.name

    def get_location(self):
        return self.location

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')


class Category(models.Model):
    category_name = models.CharField(max_length=200,
                                     verbose_name=('category_name'))
    category_description = models.CharField(
        max_length=200, verbose_name=_('category_description'))
    image = models.ImageField()

#   Ref for images: https://www.youtube.com/watch?v=-bjsz18pR54
#                   https://www.youtube.com/watch?v=PIvlcmnayOE

    def __str__(self):
        return self.category_description

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        db_table = 'category'


class Registration(models.Model):
    product_description = models.CharField(
        max_length=10000, verbose_name=_('product_discription'))
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name=_('price'))
    image = models.ImageField(blank=True, null=True,
                              verbose_name=_('image'))
    image_url = models.CharField(max_length=500, null=True,
                                 verbose_name=_('image_url'))

    date_of_registration = models.DateField()
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    withdrawn = models.BooleanField(default=False)

    def __str__(self):
        return self.product_description

    @property
    def location(self):
        return self.shop.location

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
