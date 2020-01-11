from django.urls import path
from app.views import (
    index,
    RegisterView,
    LoginView,
    LogoutView,
    VoteView, CancelVote, themePage, CreatePoll, UserProfile, EditProfile)

urlpatterns = [
    path('', index, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('poll/<int:pk>/vote/<int:rez>', VoteView.as_view(), name='vote'),
    path('poll/<int:pk>/vote/cancel', CancelVote.as_view(), name='cancelVote'),
    path('theme/<int:theme_key>', themePage, name='themePage'),
    path('createpoll', CreatePoll.as_view(), name='createPoll'),
    path('userprofile/<int:pk>', UserProfile.as_view(), name='userProfile'),
    path('editprofile/<int:pk>', EditProfile.as_view(), name='editProfile'),
]