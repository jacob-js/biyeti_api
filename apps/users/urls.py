from django.urls import path, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'all', views.UserAdminView, basename='users')
# router.register(r'^reset-password?/<str:phone>', views.PasswordResetView, basename='users')

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('current', views.GetLogedUser.as_view()),
    path('login/google', views.GoogleLoginView.as_view()),
    path('profile', views.ProfileView.as_view()),
    re_path(r'reset-password/(?P<phone>[(+*)][0-9]{0,15})', views.PasswordResetView.as_view()),
] + router.urls