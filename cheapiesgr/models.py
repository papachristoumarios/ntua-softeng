from django.db import models

# Create your models here.

class Registration(models.Model):
	pass

class Volunteer(models.Model):
	pass

class Rating(models.Model):
	Stars = models.IntegerField()
	Validity_of_this_rate = models.IntegerField()
	Rate_explanation = models.CharField(max_length = 1000)
	Registration_id = models.ForeignKey(Registration, on_delete = models.CASCADE)
	Volunteer_id = models.ForeignKey(Volunteer, on_delete = models.CASCADE)

class Category2(models.Model):
	Category2_discription = models.CharField(max_length = 200)

class Category1(models.Model):
	Category1_discription = models.CharField(max_length = 200)
	Category2_id = models.ForeignKey(Category2, on_delete = models.CASCADE)

class Category(models.Model):
	Category_discription = models.CharField(max_length = 200)
	Category1_id = models.ForeignKey(Category1, on_delete = models.CASCADE)
