from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "common"

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path("sign-up/", views.SignUpView.as_view(), name='sign-up'),
    path('logout/', views.logout_view, name='logout'),
    path('mypage/<str:username>', views.mypage, name="mypage"),
    path("account/<str:username>", views.UpdateAccountView.as_view(), name="account")
]