from django.urls import path, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'', views.UserAdminView, basename='users')

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('current', views.GetLogedUser.as_view()),
    path('login/google', views.GoogleLoginView.as_view()),
] + router.urls