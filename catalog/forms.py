import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check if a date is not in the past
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        #Remember to always return the cleaned data
        return data

from catalog.models import Profile, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    
    QUESTION_SAMPLES = (
        ('1', 'In what city did you have your first ever birthday party?'),
        ('2', 'What is the last name of your Science class teacher in high school?'),
        ('3', 'Which company manufactured your first mobile phone?'),
        ('4', 'Who was your childhood hero?'),
        ('5', 'Where was your best family vacation?')
    )

    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=100)
    idno = forms.CharField(max_length=8)
    question = forms.CharField(widget=forms.Select(choices = QUESTION_SAMPLES))
    answer = forms.CharField(max_length=30)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email is already in use.')
    
    class Meta():   
        model = User
        fields = ('username','first_name','last_name','idno','email','password1','password2','question','answer')


class QuestionForm(forms.Form):
    answer = forms.CharField(max_length=100, help_text="Enter answer to question.", widget=forms.TextInput(attrs={'autocomplete':'off'}))
    def clean_answer(self):
        answer1 = self.cleaned_data['answer']

        return answer1

    class Meta():
        fields = ('answer')


class EmailForm(forms.Form):
    email = forms.EmailField(max_length=100, help_text="Enter Email Address", widget=forms.TextInput(attrs={'autocomplete':'off'}))

    class Meta():
        fields = ('email')

from django.contrib.auth.forms import SetPasswordForm
class PasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New Password Confirmation"), widget=forms.PasswordInput)

    class Meta():
        fields = ('new_password1', 'new_password2')

class borrowForm (forms.Form):
    comm_borrow = forms.CharField()

class commentForm (forms.ModelForm):
    
    print("ReviewForm")
    rating = forms.IntegerField(label =_("Rating"))
    review = forms.CharField(max_length=300, label=_("Review"), widget=forms.TextInput(attrs={'autocomplete':'off'}))
   # book = forms.CharField()

    class Meta():
        model = Review
        fields = ('rating', 'review')

    
