from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse # Used to generate URLs be reversing the URL patterns
import uuid # Required for unique book instances
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
    name = models.CharField(max_length=200,help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name
        
class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character ISBN number')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    publisher = models.CharField(max_length=300, null=True)
    date_added_to_library = models.DateField(null=True, blank=True)
    review = models.ForeignKey('Review', on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        """String for representing the Model object."""
        return self.title  

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])  


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey('Profile', on_delete=models.SET_NULL, null = True, blank=True)
    date_added = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('a','Available'),
        ('r','Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
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

class Author(models.Model):
    """Model representing an author."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID')
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
    user =  models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    review =  models.CharField(max_length=500)
    rating =  models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])


    def __str__(self):
        """String for representing the Model object."""
        return self.review  

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('review-details', args=[str(self.id)])  
    

# User Stuff (7/4/20)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

    answer =  models.CharField(max_length=30)

    def __str__(self):
        return self.user.username
    
    

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)

    instance.profile.save()
