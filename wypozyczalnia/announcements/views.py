from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Announcement, Rating, Borrowing
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from .forms import AnnouncementForm, RatingForm, BorrowingForm


def home(request):
    context = {}
    context['data'] = Announcement.objects.all()
    if request.user.is_authenticated:
        username = request.user.username
        context['userStatus'] = 'Witaj użytkowniku ' + username
    else:
        context['userStatus'] = 'Niezalogowany'
    return render(request, 'announcements/home.html', context)


def signup_page(request):
    context = {}
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
            context['error'] = 'Podana nazwa użytkownika już istnieje! Proszę podać inną nazwę użytkownika.'
            return render(request, 'announcements/signup.html', context)
        except User.DoesNotExist:
            if request.POST['password1'] != request.POST['password2']:
                context['error'] = 'Podane hasła nie są takie same! Proszę wprowadzić identyczne hasła.'
                return render(request, 'announcements/signup.html', context)
            else:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)
                return redirect('http://127.0.0.1:8000/')
    else:
        return render(request, 'announcements/signup.html', context)


def login_page(request):
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            context['error'] = 'Podane hasło lub login są błędne! Podaj poprawne dane.'
            return render(request, 'announcements/login.html', context)
    else:
        return render(request, 'announcements/login.html')


def logout_page(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('http://127.0.0.1:8000/')
    else:
        return redirect('http://127.0.0.1:8000/')


def my_announcements(request):
    context = {}
    username = request.user.username
    context['data'] = Announcement.objects.filter(author__username=username)
    return render(request, 'announcements/my_announcements.html', context)


def add_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('detail_announcement', pk=announcement.pk)
    else:
        form = AnnouncementForm()
    return render(request, 'announcements/add_announcement.html', {'form': form})


def detail_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    rating = announcement.comments.all()

    average_rating = rating.aggregate(average=Avg('grade'))['average']
    average_rating = average_rating if average_rating else 0

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.announcement_id = announcement.pk
            rating.user = request.user
            rating.save()
            return redirect('detail_announcement', pk=announcement.pk)
    else:
        form = RatingForm(instance=announcement)
    return render(request, 'announcements/detail_announcement.html', {'announcement': announcement, 'rating': rating,
                                                                      'form': form, 'average_rating': average_rating})


def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST or None, request.FILES or None, instance=announcement)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('detail_announcement', pk=announcement.pk)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'announcements/edit_announcement.html', {'form': form})


def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    return render(request, 'announcements/delete_announcement.html', {'del_announcement': announcement})


@login_required
def borrow_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if announcement.available:
        if request.method == "POST":
            form = BorrowingForm(request.POST)
            if form.is_valid():
                borrowing = form.save(commit=False)
                borrowing.announcement = announcement
                borrowing.borrower = request.user
                borrowing.borrow_date = timezone.now()
                announcement.available = False
                announcement.save()
                borrowing.save()
                return render(request, 'announcements/succes_borrow.html')
        else:
            initial_data = {
                'borrow_date': timezone.now().date()
            }
            form = BorrowingForm(initial=initial_data)
        return render(request, 'announcements/borrow_announcement.html', {'announcement': announcement, 'form': form})
    else:
        return render(request, 'announcements/borrow_error.html', {'announcement': announcement})


@login_required
def return_announcement(request, pk):
    borrowing = get_object_or_404(Borrowing, pk=pk)
    announcement = borrowing.announcement
    announcement.available = True
    announcement.save()
    borrowing.delete()
    return render(request, 'announcements/return_announcement.html', {'borrowing': borrowing})


@login_required
def my_borrowings(request):
    context = {}
    borrowings = Borrowing.objects.filter(borrower=request.user)
    today = timezone.now().date()

    for borrowing in borrowings:
        return_date = borrowing.return_date
        borrow_date = borrowing.borrow_date

        total_price = borrowing.announcement.price * (return_date - borrow_date).days
        borrowing.total_price = total_price

        if return_date:
            days_left = (return_date - today).days
            borrowing.days_left = days_left

    context['borrowings'] = borrowings
    return render(request, 'announcements/my_borrowings.html', context)


def search_announcements(request):

    searched = request.POST['searched']
    announcements = Announcement.objects.filter(name__contains=searched)
    return render(request, 'announcements/search_announcements.html', {'searched': searched,
                                                                       'announcements': announcements})

