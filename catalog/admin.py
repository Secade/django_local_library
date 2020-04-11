from django.contrib import admin
from .models import Profile

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(BookInstance)
# admin.site.register(Language)
# admin.site.register(Profile)


"""
class UserAdmin (admin.ModelAdmin):
    list_display = ('username')"""

class BookInline(admin.TabularInline):
    list_display = ('title','language','summary','isbn','genre','publisher','date_added_to_library')
    fields = [('title','summary'),'language','isbn','genre','publisher','date_added_to_library']
    model = Book

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'given_name', 'date_of_birth', 'date_of_death')
    fields = ['given_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

    # removes the add, change, delete button (11/04/2020)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

#Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    inlines = [BookInstanceInline]

    # removes the add, change, delete button (11/04/2020)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

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

    # removes the add, change, delete button (11/04/2020)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)

class GenreAdmin(admin.ModelAdmin):
    # removes the add, change, delete button (11/04/2020)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Genre, GenreAdmin)


class LanguageAdmin(admin.ModelAdmin):
    # removes the add, change, delete button (11/04/2020)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Language, LanguageAdmin)

class ProfileAdmin(admin.ModelAdmin):
    # removes the add, change, delete button (11/04/2020)
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Profile, ProfileAdmin)