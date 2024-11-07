from django.urls import path
from apps.account.views import UserSignupView, UserSigninView, RoleListView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('signin/', UserSigninView.as_view(), name='signin'),
    path('roles/', RoleListView.as_view(), name='roles'),
]