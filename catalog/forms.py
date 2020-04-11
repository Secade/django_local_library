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

from catalog.models import Profile, Author,Language, Genre, Book
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

    first_name = forms.CharField(max_length=20, help_text='First Name')
    last_name = forms.CharField(max_length=20, help_text='Last Name')
    email = forms.EmailField(max_length=100, help_text='Email')
    idno = forms.CharField(max_length=8, help_text='Id Number')
    question = forms.CharField(widget=forms.Select(choices = QUESTION_SAMPLES))
    answer = forms.CharField(max_length=30, help_text='Answer')
    
    class Meta():   
        model = User
<<<<<<< HEAD
        fields = ('username','first_name','last_name','idno','email','password1','password2','question','answer')

    
=======
        fields = ('username','first_name','last_name','idno','email','password1','password2','question','answer')
>>>>>>> parent of 3a06c9a... Stable Version April 11 2020
