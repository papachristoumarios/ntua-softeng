from django.contrib.auth.forms import UserCreationForm
from cheapiesgr.models import MyUser
from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Shop

def get_categories():
    iterable = Category.objects.all().order_by('category_name')
    result = []
    for category in iterable:
        result.append((category.id, category.category_name))
    return tuple(result)

def get_shops():
    iterable = Shop.objects.all().order_by('name')
    result = [(-1, 'Άλλο')]
    for shop in iterable:
        result.append((shop.id, shop.name))

    return tuple(result)

def get_stars():
    return tuple([(1, '1 αστέρι')] + [(i, str(i) + ' αστέρια') for i in range(2, 6)])


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
        widget=forms.Textarea(attrs={'placeholder': 'Πληκτρολογήστε μια περιγραφή για το προϊόν','class' : 'form-control','id': 'description'}),
    )

    price = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Δώστε τιμή για το προϊόν','class' : 'form-control','id': 'price'}),
    )


    location = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'placeholder': 'Δώστε κατάστημα (επιλέξτε άλλο αν δεν υπάρχει)','class' : 'form-control','id': 'location'}),
        choices=get_shops()
    )

    new_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Καταχωρήστε νέο κατάστημα','class' : 'form-control','id': 'new_location'}),
    )


    img = forms.FileField(
        widget=forms.FileInput(attrs={'accept':'image/*'})
    )

    category = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control','id': 'category'}),
        choices=get_categories()
    )

class ReviewForm(forms.Form):

    rate_explanation = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Πληκτρολογήστε μια αξιολόγηση για το προϊόν','class' : 'form-control','id': 'rate_explanation'}),
    )

    stars = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control','id': 'stars'}),
        choices=get_stars()
    )


class QuestionForm(forms.Form):

    question = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Κάντε μια ερώτηση','class' : 'form-control','id': 'question', 'cols': 30, 'rows': 2}),
    )


class AnswerForm(forms.Form):

    answer = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Απαντήστε','class' : 'form-control','id': 'answer'}),
    )
