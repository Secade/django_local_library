from django.contrib import admin
from .models import Profile
from .models import Author, Genre, Book, BookInstance, Language, Review, ReturnedBooks, Log

"""
class UserAdmin (admin.ModelAdmin):
    list_display = ('username')"""

class BookInline(admin.TabularInline):
    list_display = ('title','language','summary','isbn','genre','publisher','date_added_to_library')
    fields = [('title','summary'),'language','isbn','genre','publisher','date_added_to_library']
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'given_name', 'date_of_birth', 'date_of_death')
    fields = ['given_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    inlines = [BookInstanceInline]

    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ('Book', {
            'fields': ('book','id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        })
    )

    def has_add_permission(self, request):
        return False
    #def has_delete_permission(self, request, obj=None):
     #   return False
    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

class GenreAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(Genre, GenreAdmin)


class LanguageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(Language, LanguageAdmin)

class ProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(Profile, ProfileAdmin)

class ReturnedBooksAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True
    def has_delete_permission(self, request, obj=None):
        return True
    def has_change_permission(self, request, obj=None):
        return True

admin.site.register(ReturnedBooks, ReturnedBooksAdmin)

class ReviewInLine(admin.TabularInline):
    model = Review

admin.site.register(Review)

class LogsInLine (admin.TabularInline):
    list_display = ('timestamp','id', 'user','item', 'action')

class LogsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
   # def has_delete_permission(self, request, obj=None):
     #   return False
    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Log, LogsAdmin)
