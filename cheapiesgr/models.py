from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db.models import Manager as GeoManager
from django.utils.translation import gettext_lazy as _



class MyUser(AbstractBaseUser):
	username = models.CharField(max_length = 255, unique = True,
	verbose_name = _('username'))
	email = models.CharField(max_length = 255, unique = True)
	active = models.BooleanField(default = True,
	verbose_name = _('active'))
	staff = models.BooleanField(default = False,
	verbose_name = _('staff'))
	admin = models.BooleanField(default = False,
	verbose_name = _('admin'))
	confirmed_email = models.BooleanField(default=False) # is email confirmed
	USERNAME_FIELD = 'username'
#   USERNAME_FIELD and password are required by default
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def get_email(self):
		return self.email

	@property
	def is_email_confirmed(self):
		return self.confirmed_email

	@property
	def is_active(self):
		return self.active

	@property
	def is_admin(self):
		return self.admin

	@property
	def is_staff(self):
		return self.staff

	@receiver(post_save, sender=AbstractBaseUser)
	def update_user_profile(sender, instance, created, **kwargs):
		if created:
			Volunteer.objects.create(user=instance)
		instance.profile.save()



class Volunteer(models.Model):
#   Class Volunteer is used to extend MyUser safely
	user = models.OneToOneField(MyUser, on_delete = models.CASCADE)
	first_name = models.CharField(max_length = 100,
	verbose_name = _('first_name'))
	last_name = models.CharField(max_length = 100,
	verbose_name = _('last_name'))

	def __str__(self):
		return self.user

	def get_last_name(self):
		return self.last_name

	def get_first_name(self):
		return self.first_name
	class Meta:
		verbose_name = _('volunteer')
		verbose_name_plural = _('volunteers')


class Shop(models.Model):
	name = models.CharField(max_length=500, verbose_name=_('name'))
	address = models.CharField(max_length=500,
	verbose_name = _('address'))
	city = models.CharField(max_length=500,
	verbose_name = _('city'))
	location = gis_models.PointField(
										geography=True, blank=True, null=True,
										verbose_name = _('location'))

	#gis = gis_models.GeoManager() GeoManager is used as follow since Django 2.0 in order to do spatial lookups
	objects = GeoManager()

	def __str__(self):
		return self.name

	def get_location(self):
		return self.location

	class Meta:
		verbose_name = _('shop')
		verbose_name_plural = _('shops')


class Category(models.Model): # Highest level (abstract)
	category_name = models.CharField(max_length = 200,
	verbose_name = _('category_name'))
	category_description = models.CharField(max_length = 200,
	verbose_name = _('category_description'))
	image = models.ImageField()
#   Ref for images: https://www.youtube.com/watch?v=-bjsz18pR54
#                   https://www.youtube.com/watch?v=PIvlcmnayOE

	def __str__(self):
		return self.category_description

	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('categorys')


class Registration(models.Model):
	product_description = models.CharField(max_length = 10000,
	verbose_name = _('product_discription'))
	price = models.DecimalField(max_digits = 10, decimal_places = 2,
	verbose_name = _('price'))
	image = models.ImageField(blank=True, null=True,
	verbose_name = _('image'))
	image_url = models.CharField(max_length=500, null=True,
	verbose_name = _('image_url'))

	date_of_registration = models.DateField()
	volunteer = models.ForeignKey(Volunteer, on_delete = models.CASCADE)
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	withdrawn = models.BooleanField(default=False)

	def __str__(self):
		return self.product_description

	@property
	def location(self):
		return self.shop.location

	@property
	def stars(self):
		r = self.rating_set.all().aggregate(models.Avg('stars'))['stars__avg']
		if r == None:
			return 0
		else:
			return r

	@stars.getter
	def stars(self):
		r = self.rating_set.all().aggregate(models.Avg('stars'))['stars__avg']
		if r == None:
			return 0
		else:
			return r

	class Meta:
		verbose_name = _('registration')
		verbose_name_plural = _('registrations')


class Rating(models.Model):
	stars = models.IntegerField(verbose_name = _('stars'))
	validity_of_this_rate = models.IntegerField(verbose_name = _('validity_of_this_rate'))
	rate_explanation = models.CharField(max_length = 1000,
	verbose_name = _('rate_explanation'))
	registration = models.ForeignKey(Registration, on_delete = models.CASCADE)
	volunteer = models.ForeignKey(Volunteer, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.stars)

	def get_explanation(self):
		return self.rate_explanation

	def get_validity(self):
		return self.validity_of_this_rate

	class Meta:
		verbose_name = _('rating')
		verbose_name_plural = _('ratings')


class Question(models.Model):
	question_text = models.CharField(max_length = 2000,
	verbose_name = _('question_text'))
	registration = models.ForeignKey(Registration, on_delete = models.CASCADE)

	def __str__(self):
		return self.question_text
	class Meta:
		verbose_name = _('question')
		verbose_name_plural = _('questions')


class Answer(models.Model):
	answer_text = models.CharField(max_length = 2000,
	verbose_name = _('answer_text'))
	question = models.ForeignKey(Question, on_delete = models.CASCADE)

	def __str__(self):
		return self.answer_text
	class Meta:
		verbose_name = _('answer')
		verbose_name_plural = _('answers')
