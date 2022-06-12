from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(r'all', views.UserAdminView, basename='users')

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('login', views.LoginView.as_view()),
    path('current', views.GetLogedUser.as_view()),
    path('login/google', views.GoogleLoginView.as_view()),
    path('profile', views.ProfileView.as_view()),
    path('verification-code/<str:identifier>', views.send_verification_code_view),
    path('validate-code', views.verify_verification_code_view),
    path('reset-password', views.reset_password_view),
] + router.urls