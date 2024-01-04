from django import forms
from .models import Announcement, Rating, Borrowing


class AnnouncementForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ('name', 'type', 'description', 'price', 'photo')
        widgets = {
            'name': forms.TextInput(attrs={'style': 'width: 300px; height: 20px;'}),
            'description': forms.TextInput(attrs={'style': 'width: 400px; height: 150px;'}),
        }


class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ('grade', 'comment')
        widgets = {
            'comment': forms.TextInput(attrs={'style': 'width: 400px; height: 50px;'}),
        }


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ('borrow_date', 'return_date')

        widgets = {
            'borrow_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'})
        }
