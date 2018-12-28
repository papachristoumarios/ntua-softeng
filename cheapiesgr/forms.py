from django.contrib.auth.forms import UserCreationForm
from cheapiesgr.models import MyUser
from django import forms
from django.core.exceptions import ValidationError
from .models import Category

def get_categories():
    iterable = Category.objects.all()
    result = []
    for category in iterable:
        result.append((category.id, category.category_name))

    return tuple(result)

class UserRegistrationForm(forms.Form):
    """User Signup Form"""

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Εισάγετε το email σας','class' : 'form-control','id': 'email'}),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Πληκτρολογήστε ένα όνομα χρήστη','class' : 'form-control','id': 'username'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Πληκτρολογήστε ένα κωδικό','class' : 'form-control','id': 'pwd'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Επαναλάβετε τον κωδικό σας','class' : 'form-control','id': 'pwd2'})
    )
    accept = forms.BooleanField(
        required=True
    )
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = MyUser.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Το email υπάρχει ήδη", code='email exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username)<4:
            raise ValidationError("Το όνομα χρήστη πρέπει να αποτελείται από τουλάχιστον 4 χαρακτήρες", code='small_username')
        if len(username)>100:
            raise ValidationError("Χρησιμοποιήστε ένα μικρότερο όνομα χρήστη", code='long_username')
        r = MyUser.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Το όνομα χρήστη υπάρχει ήδη", code='username_exists')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Οι κωδικοί δεν ταιριάζουν",code='passwords_not_match')
        return password1

    #def save(self, commit=True):
        #Εδώ πρέπει να κάνουμε το query στο model για να επιβεβαιώσουμε την εγγραφή



class UserLoginForm(forms.Form):
    """ User login form """

    user = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Πληκτρολογήστε το όνομα χρήστη ή το email σας','class' : 'form-control','id': 'username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Πληκτρολογήστε τον κωδικό πρόσβασής σας','class' : 'form-control','id': 'pwd'})
    )

    def clean_username(self):
        user = self.cleaned_data.get('user')
        r_user = MyUser.objects.filter(username=username)
        r_mail = MyUser.objects.filter(email=user)
        if r_user.count()==0 and r_mail.count()==0:
            raise  ValidationError("Ο χρήστης δεν βρέθηκε στο σύστημα", code='user_not_exists')
        return user

    def clean_password(self):
        user = self.cleaned_data.get('user')
        password = self.cleaned_data.get('user')
        ##Query(user,mail)
        if (0==0):
            raise ValidationError("Λάθος κωδικός πρόσβασης",code='wrong_password')
        return password



class AddProductForm(forms.Form):

    description = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Πληκτρολογήστε μια περιγραφή για το προϊόν','class' : 'form-control','id': 'description'}),
    )

    price = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Δώστε τιμή για το προϊόν','class' : 'form-control','id': 'price'}),
    )


    location = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Δώστε τοποθεσία','class' : 'form-control','id': 'location'}),
    )

    image = forms.FileField(required=False)

    category = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control','id': 'location'}),
        choices=get_categories()
    )
