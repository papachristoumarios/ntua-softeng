from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db.models import Manager as GeoManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
class UserManager(BaseUserManager):
	def create_user(self,username, email,first_name, last_name, password=None,): 
    
		if not email:
			raise ValueError('The email is required to create this user')
		email = UserManager.normalize_email(email)
		cuser = self.model(username=username, email=email,first_name=first_name, last_name=last_name, is_staff=False, is_active=True, is_superuser=False, last_login=None,)
		cuser.set_password(password)
		cuser.save(using=self._db)
		return cuser

	def create_superuser(self,username, email,first_name=None,last_name=None, password=None, 
                                                           ):
		u = self.create_user(username,email,first_name,last_name, password, 
                                                           )
		u.is_staff = True
		u.is_active = True
		u.is_superuser = True
		u.save(using=self._db)
		return u


class Volunteer(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length = 255, unique = True,
    verbose_name = _('username'))
    email = models.CharField(max_length = 255, unique = True)
    is_active = models.BooleanField(default = True,
    verbose_name = _('active'))
    is_staff = models.BooleanField(default = False,
    verbose_name = _('staff'))
    is_superuser = models.BooleanField(default = False,
    verbose_name = _('admin'))
    confirmed_email = models.BooleanField(default=False) # is email confirmed
    first_name = models.CharField(max_length = 100,blank=True,null=True,
	verbose_name = _('first_name'))
    last_name = models.CharField(max_length = 100,blank=True,null=True,
	verbose_name = _('last_name'))
    objects = UserManager()

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
    def is_activee(self):
        return self.is_active

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def is_stafff(self):
        return self.is_staff

    @receiver(post_save, sender=AbstractBaseUser)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Volunteer.objects.create(user=instance)
        instance.profile.save()
    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name
    class Meta:
        verbose_name = _('Volunteer')
        verbose_name_plural = _('Volunteers')
		


		

class Shop(models.Model):
	address = models.CharField(max_length=100,
	verbose_name = _('address'))
	city = models.CharField(max_length=50,
	verbose_name = _('city'))
	location = gis_models.PointField(
										geography=True, blank=True, null=True,
										verbose_name = _('location'))

    #gis = gis_models.GeoManager() GeoManager is used as follow since Django 2.0 in order to do spatial lookups
	objects = GeoManager()

	def __str__(self):
		return self.address
	class Meta:
		verbose_name = _('shop')
		verbose_name_plural = _('shops')


class Category2(models.Model): # Highest level (abstract)
	category2_description = models.CharField(max_length = 200,
	verbose_name = _('category2_description'))
	image = models.ImageField()
#   Ref for images: https://www.youtube.com/watch?v=-bjsz18pR54
#                   https://www.youtube.com/watch?v=PIvlcmnayOE

	def __str__(self):
		return self.category2_description
	class Meta:
		verbose_name = _('category2')
		verbose_name_plural = _('category2s')



class Category1(models.Model): # Mid level (sparse)
	category1_description = models.CharField(max_length = 200,
	verbose_name = _('category1_description'))
	category2 = models.ForeignKey(Category2, on_delete = models.CASCADE)
	image = models.ImageField()

	def __str__(self):
		return self.category1_description
	class Meta:
		verbose_name = _('category1')
		verbose_name_plural = _('category1s')


class Category(models.Model): # Lowest level (dense)
	category_description = models.CharField(max_length = 200,
	verbose_name = _('category_description'))
	category1 = models.ForeignKey(Category1, on_delete = models.CASCADE)
	image = models.ImageField()

	def __str__(self):
		return self.category_description
	class Meta:
		verbose_name = _('category')
		verbose_name_plural = _('categorys')


class Registration(models.Model):
	product_description = models.CharField(max_length = 200,
	verbose_name = _('product_discription'))
	price = models.DecimalField(max_digits = 10, decimal_places = 2,
	verbose_name = _('price'))
	image = models.ImageField(blank=True, null=True,
	verbose_name = _('image'))
	date_of_registration = models.DateField()
	volunteer = models.ForeignKey(Volunteer, on_delete = models.CASCADE)
	shop = models.ForeignKey(Shop, on_delete = models.CASCADE)
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return self.product_description

	def get_price(self):
		return self.get_price
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

