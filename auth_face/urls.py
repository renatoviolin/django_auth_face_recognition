from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from apps.common.views import *
from apps.user_profile.views import *

urlpatterns = [
    path('', RedirectView.as_view(), name='redirect'),
    path('admin/', admin.site.urls, name='admin'),

    path('no_permission/', NoPermission.as_view(), name='no_permission'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('home/', HomeView.as_view(), name='home'),

    path('login_face/', LoginFaceAjaxView.as_view(), name='login_face'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update', ProfileUpdateView.as_view(), name='profile_update'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
