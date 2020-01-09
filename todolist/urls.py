from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.todo, name='todo'),
    path('add_board/', views.add_board, name='add_board'),
    path('add_task/<int:pk>/', views.add_task, name='add_task'),
    path('check/<int:pk>/', views.check_task, name='check'),
    path('delete_task/<int:pk>/', views.delete_task, name='delete_task'),
    path('delete_board/<int:pk>/', views.delete_board, name='delete_board'),
    path('accounts/signup/', views.signup, name='signup'),
    path('search/', login_required(views.SearchResultsView.as_view()), name='search'),
    path('change_friendship/<int:pk>/', views.change_friendship, name='change_friendship'),
    path('share_board/', views.share_board, name='share_board'),
    path('<str:username>/', views.view_profile, name='profile'),
]