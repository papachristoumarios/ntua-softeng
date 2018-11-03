from django.db import models

# Create your models here.


class Volunteer(models.Model):
#   check out User Model:
#       https://wsvincent.com/django-referencing-the-user-model/
#   check out RegistrationFormUniqueEmail
    pass


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


