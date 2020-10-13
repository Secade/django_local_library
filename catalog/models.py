from django.db import models
from django.contrib.auth.models import User
from datetime import date
import datetime
from django.urls import reverse
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=200,help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name
        
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    publisher = models.CharField(max_length=50, null=True)
    date_added_to_library = models.DateField(null=True, blank=True)
    year = models.IntegerField(validators=[MaxValueValidator(datetime.date.today().year), MinValueValidator(1900)], null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title  

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])  


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    returnedBooks = models.ForeignKey('ReturnedBooks', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('a','Available'),
        ('r','Reserved'),
    )
	
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='a',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


    def get_absolute_url(self):
        return reverse('book instance-detail', args=[str(self.id)]) 

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    @property
    def is_available(self):
        if self.due_back == None:
            return True
        return False

class Author(models.Model):
    """Model representing an author."""
    given_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['given_name', 'last_name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.given_name}'     

class Language(models.Model):
    """Model representing a language"""
    language = models.CharField(max_length=100)

    class Meta:
        ordering = ['language']

    def __str__(self):
        """String for representing the Model object."""
        return self.language

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
    book =  models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    user =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    review =  models.TextField(max_length=1000, help_text='Enter a brief review of the book')
    rating =  models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], help_text='1 - Lowest, 10 - Highest')

    def __str__(self):
        """String for representing the Model object."""
        return self.review  

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('review-details', args=[str(self.id)])  

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    idno = models.CharField(max_length=8)

    QUESTION_SAMPLES = (
        ('1', 'In what city did you have your first ever birthday party?'),
        ('2', 'What is the last name of your Science class teacher in high school?'),
        ('3', 'Which company manufactured your first mobile phone?'),
        ('4', 'Who was your childhood hero?'),
        ('5', 'Where was your best family vacation?')
    )

    question = models.CharField(
        max_length=1,
        choices=QUESTION_SAMPLES,
        blank=True,
        default='m',
        help_text='Security Question',
    )

    answer =  models.CharField(max_length=30, blank=True)

    class Meta:
        permissions = (("can_add_staff", "Add Staff Profile"),)

    def __str__(self):
        return self.user.username
    
class ReturnedBooks(models.Model):
    user =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    return_date = models.DateField(null=True, blank=True)
    book =  models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.user.username
    

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)

    instance.profile.save()