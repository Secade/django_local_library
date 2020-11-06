from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group    
from .forms import borrowForm,commentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Book, Author, BookInstance, Genre, Language, Profile, Review, ReturnedBooks, Log

def index(request):
    """View function for home page of site"""

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.all().count()
    num_books_specific = Book.objects.filter(title__contains='of').count()
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

    return render(request, 'index.html',context=context)

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class LogListView (generic.ListView):
    model = Log
    queryset = Log.objects.order_by('-timestamp')
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorDetailView(generic.DetailView):
    model = Author


from django.shortcuts import get_object_or_404

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class AllLoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing all books on loan."""
    model=BookInstance
    template_name='catalog/bookinstance_list_all_borrowed_books.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.all()

import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse

from catalog.models import Author

class AuthorCreate(PermissionRequiredMixin,CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    success_url = reverse_lazy('author_modify')
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " added author '" + self.object.given_name+" "+self.object.last_name+"'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        return super(AuthorCreate, self).form_valid(form)

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    model = Author
    fields = ['given_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('author_modify')
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " edited author '" + self.object.given_name+" "+self.object.last_name+"'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        return super(BookUpdate, self).form_valid(form)



class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('author_modify')
    permission_required = 'catalog.can_mark_returned'



    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        Book.objects.filter(author=self.object.pk).delete()
        BookInstance.objects.filter(book__isnull=True).delete()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + ' deleted a book.'
        self.object.delete()
        log = Log(user = self.request.user, action = actionString, item = "book", timestamp = datetime.datetime.now())
        log.save()
        print("REACH BOOK DELETE")
        return HttpResponseRedirect(reverse_lazy('author_modify'))
        


from catalog.models import Book

class BookCreate(PermissionRequiredMixin,CreateView):
    model = Book
    fields = [ 'title', 
    'author',
    'language',
    'summary',
    'isbn',
    'genre',
    'publisher',
    'date_added_to_library']
    success_url = reverse_lazy('book_modify')
    permission_required = 'catalog.can_mark_returned'



    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " added book '" + self.object.title+"'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        print("REACH BOOK CREATE IF VALID")
        return super(BookCreate, self).form_valid(form)
        

class BookUpdate(PermissionRequiredMixin,UpdateView):
    model = Book
    fields = [ 'title', 
    'author',
    'language',
    'summary',
    'isbn',
    'genre',
    'publisher',
    'date_added_to_library']
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('book_modify')

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " edited book " + self.object.title + "'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK UPDATE IF VALID")
        return super(BookUpdate, self).form_valid(form)

class BookDelete(PermissionRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('book_modify')
    permission_required = 'catalog.can_mark_returned'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        BookInstance.objects.filter(book=self.object.pk).delete()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + ' deleted a book.'
        self.object.delete()
        log = Log(user = self.request.user, action = actionString, item = "book", timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK DELETE")
        return HttpResponseRedirect(reverse_lazy('book_modify'))

class BookInstanceCreate (PermissionRequiredMixin,CreateView):
    model = BookInstance
    fields = ['book', 'due_back','due_back','borrower','date_added']
    success_url = reverse_lazy('bookinstance_modify')
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " added a book instance for '" + self.object.book.title+"'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK INSTANCE CREATE IF VALID")
        return super(BookInstanceCreate, self).form_valid(form)

class BookInstanceUpdate(PermissionRequiredMixin,UpdateView):
    model = BookInstance
    fields = ['book', 'due_back','due_back','borrower','date_added']
    success_url = reverse_lazy('bookinstance_modify')
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " edited a book instance " + self.object.title + "'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK UPDATE IF VALID")
        return super(BookInstanceUpdate, self).form_valid(form)
    
class BookInstanceDelete(PermissionRequiredMixin,DeleteView):
    model = BookInstance
    success_url = reverse_lazy('bookinstance_modify')
    permission_required = 'catalog.can_mark_returned'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + ' deleted a book instance.'
        self.object.delete()
        log = Log(user = self.request.user, action = actionString, item = "book", timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK DELETE")
        return HttpResponseRedirect(reverse_lazy('bookinstance_modify'))

class LanguageCreate (PermissionRequiredMixin,CreateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('language_modify')
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " added language '" + self.object.language+"'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK INSTANCE CREATE IF VALID")
        return super(LanguageCreate, self).form_valid(form)

class LanguageUpdate(PermissionRequiredMixin,UpdateView):
    model = Language
    fields = '__all__'
    success_url = reverse_lazy('language_modify')
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " modified language '" + self.object.language+"'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK INSTANCE CREATE IF VALID")
        return super(LanguageUpdate, self).form_valid(form)

    
class LanguageDelete(PermissionRequiredMixin,DeleteView):
    model = Language
    success_url = reverse_lazy('language_modify')
    permission_required = 'catalog.can_mark_returned'

    def delete(self, request, *args, **kwargs):
        actionString = self.request.user.first_name +" "+self.request.user.last_name + ' deleted a book instance.'
        Book.objects.filter(language=self.object.pk).delete()
        self.object.delete()
        log = Log(user = self.request.user, action = actionString, item = "book", timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK DELETE")
        return HttpResponseRedirect(reverse_lazy('bookinstance_modify'))

class GenreCreate (PermissionRequiredMixin,CreateView):
    model = Genre
    fields = '__all__'
    success_url = reverse_lazy('genre_modify')
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " added genre '" + self.object.name+"'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK INSTANCE CREATE IF VALID")
        return super(GenreCreate, self).form_valid(form)

class GenreUpdate(PermissionRequiredMixin,UpdateView):
    model = Genre
    fields = '__all__'
    success_url = reverse_lazy('genre_modify')
    permission_required = 'catalog.can_mark_returned'

    def form_valid(self, form):
        self.object = form.save()
        actionString = self.request.user.first_name +" "+self.request.user.last_name + " modified genre '" + self.object.name+"'."
        log = Log(user = self.request.user, action = actionString, item = self.object, timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK INSTANCE CREATE IF VALID")
        return super(GenreUpdate, self).form_valid(form)
    
class GenreDelete(PermissionRequiredMixin,DeleteView):
    model = Genre
    success_url = reverse_lazy('genre_modify')
    permission_required = 'catalog.can_mark_returned'

    def delete(self, request, *args, **kwargs):
        actionString = self.request.user.first_name +" "+self.request.user.last_name + ' deleted a genre.'
        Book.objects.filter(name=self.object.pk).delete()
        self.object.delete()
        log = Log(user = self.request.user, action = actionString, item = "book", timestamp = datetime.datetime.now())
        log.save()
        #print("REACH BOOK DELETE")
        return HttpResponseRedirect(reverse_lazy('bookinstance_modify'))

class BooksModify(PermissionRequiredMixin,generic.ListView):
    model=Book
    template_name='catalog/book_modify.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

class BookInstanceModify(PermissionRequiredMixin,generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_modify.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

class AuthorsModify(PermissionRequiredMixin,generic.ListView):
    model=Author
    template_name='catalog/author_modify.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

class GenreModify(PermissionRequiredMixin,generic.ListView):
    model=Genre
    template_name='catalog/genre_modify.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

class LanguageModify(PermissionRequiredMixin,generic.ListView):
    model=Language
    template_name='catalog/language_modify.html'
    paginate_by=10
    permission_required = 'catalog.can_mark_returned'

class SystemLogs(PermissionRequiredMixin,generic.ListView):
    model=Language
    template_name='catalog/system_logs.html'
    paginate_by=10
    permission_required = 'catalog.can_add_staff'

from django.shortcuts import render

def error_404(request, exception):
        data = {}
        return render(request,'catalog/404.html', data)

def error_403(request, exception):
        data = {}
        return render(request,'catalog/403.html', data)

from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from axes.decorators import axes_dispatch
from .forms import SignUpForm
from django.contrib import messages

@axes_dispatch
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


            user = authenticate(username=username, password=password, request=request)
            login(request, user)

            actionString = user.profile.first_name + " "+ user.profile.last_name  + ' created an account.'
            log = Log(user = request.user, action = actionString, item = "User", timestamp = datetime.datetime.now())
            log.save()

            messages.success(request, f'Account created for {username}!')


            return redirect('/catalog/')
        else:
            print (form.errors)
            messages.error(request,"Can't SignUp")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})    

@axes_dispatch
def staff_add_view(request):
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
            user = authenticate(username=username, password=password, request=request)
            login(request, user)
            messages.success(request, f'Account created for {username}!')


            actionString = user.profile.first_name + " "+ user.profile.last_name  + ' created an account.'
            log = Log(user = request.user, action = actionString, item = "User", timestamp = datetime.datetime.now())
            log.save()
            return redirect('/catalog/')
        else:
            print (form.errors)
            messages.error(request,"Can't SignUp")
    else:
        form = SignUpForm()
    return render(request, 'staff_form.html', {'form':form})    

class UserProfile(LoginRequiredMixin, generic.ListView):
    template_name='catalog/profile.html'
    queryset = Profile.objects.all()

    def get_context_data(self, **kwargs):
        context = super(generic.ListView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.all()
        context['bookinstance_list'] = BookInstance.objects.all()
        context['reviews_list'] = Review.objects.all()
        context['returnedBooks_list'] = ReturnedBooks.objects.all()
        return context

def lockout_view(request):

    return render(request, 'lockout.html') 

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
            actionString = user.profile.first_name + " "+ user.profile.last_name  + ' reseted password.'
            log = Log(user = request.user, action = actionString, item = "User", timestamp = datetime.datetime.now())
            log.save()
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

def borrowBook_view(request, pk):
    currDate = datetime.datetime.now()
    user = request.user
    book_instance = get_object_or_404(BookInstance,pk=pk)

    if book_instance.status == 'a':

        book_instance.status = 'r'
        book_instance.borrower = user
        book_instance.due_back = currDate + datetime.timedelta(weeks=1)
        book_instance.save()
        return redirect('/catalog/profile/')
    else:
        return redirect('/catalog/')
    return render(request, 'book_detail.html')

def reviewCreate_view (request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = commentForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
           review = form.save(commit=False)
           review.user = request.user
           review.book = book
           review.rating = form.cleaned_data.get('rating')
           review.save()

           actionString = request.user.first_name + ' commented on ' + review.book.title
           log = Log(user = request.user, action = actionString, item = book, timestamp = datetime.datetime.now())
           log.save()
           return redirect('/catalog/book/'+str(book.pk))
        else:
            print (form.errors)
    else:
        form = commentForm()
    return render(request, 'catalog/review_form.html', {'form':form})

def returnBook_view(request, pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)

    if book_instance.status == 'r':
        book_instance.returnedBooks = ReturnedBooks(user=book_instance.borrower,return_date=datetime.date.today(),book=book_instance.book)
        book_instance.returnedBooks.save()
        book_instance.status = 'a'
        book_instance.borrower = None
        book_instance.due_back = None
        book_instance.save()
        
        actionString = request.user.first_name + ' returned book  "' + book_instance.book.title+'".'
        log = Log(user = request.user, action = actionString, item = "book instance", timestamp = datetime.datetime.now())
        log.save()

        return redirect('/catalog/onloan/')
    else:
        return redirect('/catalog/')
    return render(request, 'book_detail.html')