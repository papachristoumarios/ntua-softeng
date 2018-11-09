from django.db import models
from django.contrib.auth.models import (AbstractBaseUser)
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Volunteer(AbstractBaseUser):
	username = models.CharField(max_length = 255, unique = True)
	email = models.CharField(max_length = 255, unique = True)
	active = models.BooleanField(default = True)
	staff = models.BooleanField(default = False)
	admin = models.BooleanField(default = False)
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
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


class Shop(models.Model):
    location = models.CharField(max_length = 200) # check out GeoDjango


class Category2(models.Model): # Highest level (abstract)
    category2_description = models.CharField(max_length = 200)
#   image = models.ImageField(...)


class Category1(models.Model): # Mid level (sparse)
    category1_description = models.CharField(max_length = 200)
    category2 = models.ForeignKey(Category2, on_delete = models.CASCADE)
#   image = models.ImageField(...)


class Category(models.Model): # Lowest level (dense)
    category_description = models.CharField(max_length = 200)
    category1 = models.ForeignKey(Category1, on_delete = models.CASCADE)
#   image = models.ImageField(...)


class Registration(models.Model):
    product_description = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
#   image = models.ImageField(...)
    date_of_registration = models.DateField()
    volunteer = models.ForeignKey(Volunteer, on_delete = models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Rating(models.Model):
    stars = models.IntegerField()
    validity_of_this_rate = models.IntegerField()
    rate_explanation = models.CharField(max_length = 1000)
    registration = models.ForeignKey(Registration, on_delete = models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete = models.CASCADE)


class Question(models.Model):
    question_text = models.CharField(max_length = 2000)
    registration = models.ForeignKey(Registration, on_delete = models.CASCADE)


class Answer(models.Model):
    answer_text = models.CharField(max_length = 2000)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)


