
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path('onloan/', views.AllLoanedBooksListView.as_view(), name="all-borrowed"),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),

]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]

urlpatterns+=[
    path('bookinstance/create/', views.BookInstanceCreate.as_view(), name ='book_instance_create'),
    path('bookinstance/<int:pk>/update/', views.BookInstanceUpdate.as_view(), name ='book_instance_update'),
    path('bookinstance/<int:pk>/delete/', views.BookInstanceDelete.as_view(), name ='book_instance_delete'),
]

urlpatterns += [
    path('profile/', views.UserProfile.as_view(), name='user_profile'),
]

urlpatterns += [
    path('modifybooks/', views.BooksModify.as_view(), name='book_modify'),
    path('signup/', views.signup_view, name="signup"),
    path('lockout/', views.lockout_view, name="lockout"),
    path('passwordreset/', views.passwordReset_view, name="reset"),
    path('emailreset/', views.emailRequest_view, name="email-reset"),
]