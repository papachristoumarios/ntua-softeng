from django.forms import forms
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.forms import UserCreationForm
from cheapiesgr.models import Volunteer

class SignUpForm(UserCreationForm):

    class Meta:
        model = Volunteer

        fields = ('email',
                  'username',
				  'password', )
