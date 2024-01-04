from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my_announcements/', views.my_announcements, name='my_announcements'),
    path('signup/', views.signup_page, name='signup_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('add_announcement/', views.add_announcement, name='add_announcement'),
    path('announcement/<int:pk>/', views.detail_announcement, name='detail_announcement'),
    path('announcement/<int:pk>/edit/', views.edit_announcement, name='edit_announcement'),
    path('announcement/<int:pk>/delete/', views.delete_announcement, name='delete_announcement'),
    path('borrow_announcement/<int:pk>/', views.borrow_announcement, name='borrow_announcement'),
    path('my_borrowings/', views.my_borrowings, name='my_borrowings'),
    path('announcement/<int:pk>/return_announcement/', views.return_announcement, name='return_announcement'),
    path('search/', views.search_announcements, name='search_announcements'),
]