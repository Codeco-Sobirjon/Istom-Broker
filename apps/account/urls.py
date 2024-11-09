from django.urls import path
from apps.account.views import (
    UserSignupView, UserSigninView, RoleListView,
    CustomUserDetailView, PasswordUpdateView
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', UserSigninView.as_view(), name='signin'),
    path('roles/', RoleListView.as_view(), name='roles'),
    path('user/', CustomUserDetailView.as_view(), name='user-detail'),
    path('update-password/', PasswordUpdateView.as_view(), name='update-password'),
]