from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "common"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path("sign-up/", views.SignUpView.as_view(), name='sign-up'),
    path('logout/', views.logout_view, name='logout'),
    path('account/<str:username>', views.MyPageView.as_view(), name="account"),
    path("account/<str:username>/update-page", views.AccountUpdateView.as_view(), name="account-update")
]