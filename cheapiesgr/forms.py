from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import Category, Shop, Volunteer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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
    return tuple([(1, '1 αστέρι')] + [(i, str(i) + ' αστέρια')
                 for i in range(2, 6)])


class UserRegistrationForm(forms.Form):
    """User Signup Form"""

    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
                                    'placeholder': 'Εισάγετε το email σας',
                                    'class': 'form-control',
                                    'id': 'email'}),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
                                    'placeholder': 'Πληκτρολογήστε ένα όνομα χρήστη',
                                    'class': 'form-control',
                                    'id': 'username'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Πληκτρολογήστε ένα κωδικό',
                                        'class': 'form-control',
                                        'id': 'pwd'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Επαναλάβετε τον κωδικό σας',
                                        'class': 'form-control',
                                        'id': 'pwd2'})
    )
    accept = forms.BooleanField(
        required=True
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
                                    'placeholder': 'Εισάγετε το όνομα σας',
                                    'class': 'form-control',
                                    'id': 'name'})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
                                    'placeholder': 'Εισάγετε το όνομα σας',
                                    'class': 'form-control',
                                    'id': 'surname'})
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("Το email υπάρχει ήδη", code='email exists')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise ValidationError("Το όνομα χρήστη πρέπει να αποτελείται από τουλάχιστον 4 χαρακτήρες", code='small_username')
        if len(username) > 100:
            raise ValidationError("Χρησιμοποιήστε ένα μικρότερο όνομα χρήστη", code='long_username')
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Το όνομα χρήστη υπάρχει ήδη", code='username_exists')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Οι κωδικοί δεν ταιριάζουν", code='passwords_not_match')
        return password1

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        usr = User.objects.create_user(username=username,
                                       email=email,
                                       password=password,
                                       first_name=first_name,
                                       last_name=last_name)
        usr.save()
        volunteer = Volunteer(user=usr, confirmed_email=True)
        volunteer.save()


class UserLoginForm(forms.Form):
    """ User login form """

    user = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Πληκτρολογήστε το όνομα χρήστη σας','class' : 'form-control','id': 'username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Πληκτρολογήστε τον κωδικό πρόσβασής σας','class' : 'form-control','id': 'pwd'})
    )

    def clean_user(self):
        user = self.cleaned_data.get('user')
        r_user = User.objects.filter(username=user)
        if r_user.count() == 0:
            raise  ValidationError("Ο χρήστης δεν βρέθηκε στο σύστημα", code='user_not_exists')
        self.usr = user
        return user

    def clean_password(self):
        user = self.cleaned_data.get('user')
        password = self.cleaned_data.get('password')
        user = authenticate(username=user, password=password)

        if user is None:
            raise ValidationError("Λάθος κωδικός πρόσβασης",code='wrong_password')
        return password



class AddProductForm(forms.Form):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Πληκτρολογήστε μια όνομα για το προϊόν','class' : 'form-control','id': 'name'}),
    )


    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Πληκτρολογήστε μια περιγραφή για το προϊόν','class' : 'form-control','id': 'description'}),
    )

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Δώστε ετικέτες για το προϊόν, χωρισμένες με κόμμα','class' : 'form-control','id': 'tags'}),
    )

    price = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Δώστε τιμή για το προϊόν','class' : 'form-control','id': 'price'}),
    )


    location = forms.ModelChoiceField(
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Δώστε κατάστημα (επιλέξτε άλλο αν δεν υπάρχει)','class' : 'form-control','id': 'location'}),
        queryset=Shop.objects.all(),
        empty_label='Άλλο'
    )

    new_shop_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Όνομα καταστήματος','class' : 'form-control fullw','style' : ' style="padding-top: 1rem;"','id': 'new_shop_name'}),
    )
    new_shop_city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Πόλη','class' : 'form-control fullw','style' : ' style="padding-top: 1rem;"','id': 'new_shop_city'})
    )
    new_shop_street = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Οδός','class' : 'form-control fullw','style' : ' style="padding-top: 1rem;"','id': 'new_shop_street'})
    )
    new_shop_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Αριθμός','class' : 'form-control fullw','style' : ' style="padding-top: 1rem;"','id': 'new_shop_number'})
    )

    shot = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'id':'shot'})
    )

    img = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept':'image/*;capture=camera'})
    )

    img_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'id':'img_url'})
    )

    category = forms.ModelChoiceField(
        required=True,
        widget=forms.Select(attrs={'class' : 'form-control','id': 'category'}),
        queryset=Category.objects.all(),
        initial=0
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


class FavoritesForm(forms.Form):
    """ Add to favorites """
    pass

class UserProfileForm(forms.Form):
    """User Profile Form"""


    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Πληκτρολογήστε τον (παλαιό) κωδικό σας',
                                        'class': 'form-control',
                                        'id': 'pwd_old'})
    )


    new_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Πληκτρολογήστε τον νέο σας κωδικό',
                                        'class': 'form-control',
                                        'id': 'pwd'})
    )

    new_password_repeat = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
                                        'placeholder': 'Επαναλάβετε τον νέο σας κωδικό',
                                        'class': 'form-control',
                                        'id': 'new_pwd_rep'})
    )

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('username')
        super(UserProfileForm, self).__init__(*args, **kwargs)


    def clean_old_password(self):
        username = self.user
        password = self.cleaned_data.get('old_password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError("Λάθος κωδικός πρόσβασης",code='wrong_password')
        return password

    def clean_new_password_repeat(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('new_password_repeat')
        if password1 != password2:
            raise ValidationError("Οι κωδικοί δεν ταιριάζουν", code='passwords_not_match')
        return password1
