from django.db import models
from django.contrib.auth.model import (
    AbstractBaseUser
)
# Create your models here.


class MyUser(AbstractBaseUser):
#   Ref: https://www.youtube.com/watch?v=HshbjK1vDtY
#   Default fields: id, password, last_login
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True) # can login
    confirmed_email = models.BooleanField(default=False) # is email confirmed
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
#   USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [email]

    def __str__(self):
        return self.username

    def get_email(self):
        return self.email

    @property
    def is_active(self):
        return self.active

    @property
    def is_email_confirmed(self):
        return self.confirmed_email


class Volunteer(models.Model):
#   Class Volunteer is used to extend MyUser safely
    user = models.OneToOneField(MyUser)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user

    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name


class Shop(models.Model):
    location = models.CharField(max_length = 200) # check out GeoDjango


class Category2(models.Model): # Highest level (abstract)
    category2_description = models.CharField(max_length = 200)
    image = models.ImageField() 
#   Ref for images: https://www.youtube.com/watch?v=-bjsz18pR54
#                   https://www.youtube.com/watch?v=PIvlcmnayOE

    def __str__(self):
        return self.category2_description


class Category1(models.Model): # Mid level (sparse)
    category1_description = models.CharField(max_length = 200)
    category2 = models.ForeignKey(Category2, on_delete = models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.category1_description


class Category(models.Model): # Lowest level (dense)
    category_description = models.CharField(max_length = 200)
    category1 = models.ForeignKey(Category1, on_delete = models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.category_description


class Registration(models.Model):
    product_description = models.CharField(max_length = 200)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    image = models.ImageField(blank=True, null=True)
    date_of_registration = models.DateField()
    volunteer = models.ForeignKey(Volunteer, on_delete = models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return self.product_description

    def get_price(self):
        return self.get_price


class Rating(models.Model):
    stars = models.IntegerField()
    validity_of_this_rate = models.IntegerField()
    rate_explanation = models.CharField(max_length = 1000)
    registration = models.ForeignKey(Registration, on_delete = models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.stars)

    def get_explanation(self):
        return self.rate_explanation

    def get_validity(self):
        return self.validity_of_this_rate


class Question(models.Model):
    question_text = models.CharField(max_length = 2000)
    registration = models.ForeignKey(Registration, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.question_text


class Answer(models.Model):
    answer_text = models.CharField(max_length = 2000)
    question = models.ForeignKey(Question, on_delete = models.CASCADE)

    def __str__(self):
        return self.answer_text
