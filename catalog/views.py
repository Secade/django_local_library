from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group    

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre, Profile

def index(request):
    """View function for home page of site"""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    num_genres = Genre.objects.all().count()

    num_books_specific = Book.objects.filter(title__contains='of').count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits+1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_specific': num_books_specific,
        'num_visits': num_visits
    }

    # Render the HTML tempate index.html with the data in the context variable
    return render(request, 'index.html',context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

    def borrowBook (self, request, obj):
        print("Hello World") 
        matching_names_except_this = self.get_queryset(request).filter(name=obj.title).exclude(pk=obj.id)
        matching_names_except_this.delete()
        obj.status = 'r'
        obj.save()
        #self.message_user(request, "This villain is now unique")
        return HttpResponseRedirect(".")

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author


from django.shortcuts import get_object_or_404

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginate_by=10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='a').order_by('due_back')

from django.contrib.auth.mixins import PermissionRequiredMixin

class AllLoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing all books on loan."""
    model=BookInstance
    template_name='catalog/bookinstance_list_all_borrowed_books.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='a').order_by('due_back')

import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance,pk=pk)

    #If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request(binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

        # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

        context = {
            'form': form,
            'book_instance': book_instance,
        }

        return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse

from catalog.models import Author

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    success_url = reverse_lazy('authors')

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

from catalog.models import Book

class BookCreate(CreateView):
    model = Book
    fields = [ 'title', 
    'author',
    'language',
    'summary',
    'isbn',
    'genre',
    'publisher',
    'date_added_to_library']
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
    model = Book
    fields = [ 'title', 
    'author',
    'language',
    'summary',
    'isbn',
    'genre',
    'publisher',
    'date_added_to_library']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')


class BookInstanceCreate (CreateView):
    model = BookInstance
    fields = ['book', 'due_back','due_back','borrower','date_added']
    success_url = reverse_lazy('books')

class BookInstanceUpdate(UpdateView):
    model = BookInstance
    fields = ['book', 'due_back','due_back','borrower','date_added']
    

class BookInstanceDelete(DeleteView):
    model = BookInstance
    success_url = reverse_lazy('books')

class BooksModify(PermissionRequiredMixin,generic.ListView):
    model=Book
    template_name='catalog/book_modify.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

from django.shortcuts import render

def error_404(request, exception):
        data = {}
        return render(request,'catalog/404.html', data)

def error_403(request, exception):
        data = {}
        return render(request,'catalog/403.html', data)

#Registration stuff (7/4/20)
from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm

def signup_view(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.idno = form.cleaned_data.get('idno')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.question = form.cleaned_data.get('question')
            user.profile.answer = form.cleaned_data.get('answer')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            group = Group.objects.get(name='Teacher/Student')
            user.groups.add(group)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('/catalog/')
        else:
            print (form.errors)
            messages.error(request,"Can't SignUp")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})    

class UserProfile(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name='catalog/profile.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='a').order_by('due_back')

def lockout_view(request):

    return render(request, 'lockout.html') 

#Password Reset (11/04/2020)

from .forms import QuestionForm, EmailForm
from catalog.models import Profile
from django.contrib.auth.models import User

def passwordReset_view(request):
    form = QuestionForm(request.POST)
    uEmail = request.session['user_email']
    request.user = uEmail
    user = request.user
    print(user)
    if form.is_valid():
        answer = form.cleaned_data['answer']
        print(user.profile.answer)
        if answer == user.profile.answer:
            return redirect('/passwordchange/')
        else:   
            print(form.errors)
    else:
        form = QuestionForm()
    return render(request, 'password_question.html', {'form':form})

from catalog.models import Profile
from django.contrib.auth import forms
from django.contrib.auth import get_user_model

def emailRequest_view(request):
    user = get_user_model()
    form = EmailForm(request.POST)
    if form.is_valid():
        u = user.objects.get(email=form.cleaned_data['email'])
        request.session['user_email'] = u
        return redirect('/passwordreset/')
    else:
        form = EmailForm()
    return render(request, 'password_reset_form.html', {'form':form})

from .forms import PasswordForm


def changePassword_view(request):
    if 'user_email' in request.session:
        uEmail = request.session['user_email']
        request.user = uEmail
        user = request.user
    
    form = PasswordForm(request.user, request.POST)
    if form.is_valid():
        password1 = form.cleaned_data.get('new_password2')
        print(password1)
        form.save()
        if 'user_email' in request.session:
            del request.session['user_email']
        return redirect('/accounts/login')
    else:
        form = PasswordForm(request.user, request.POST)
    return render(request, 'password_reset.html', {'form':form})
