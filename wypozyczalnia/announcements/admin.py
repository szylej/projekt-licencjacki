from django.contrib import admin
from .models import Announcement, Rating, Borrowing

# Register your models here.


class RatingInline(admin.TabularInline):
    model = Rating


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    inlines = [
        RatingInline
    ]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'announcement', 'grade']
    list_filter = ['announcement']


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('announcement', 'borrower', 'borrow_date', 'return_date')
