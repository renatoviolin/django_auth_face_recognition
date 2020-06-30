from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, CreateView, View
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from auth_face.decorators import allowed_users
from auth_face import face_app
from django.http import JsonResponse
from auth_face import settings
import uuid
import base64
import os
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from apps.user_profile.models import Profile
from django.http import HttpResponseServerError
import numpy as np
from apps.user_profile import utils
from django.contrib.auth.forms import AuthenticationForm


class LoginFaceAjaxView(View):

    def post(self, request):
        filename = str(uuid.uuid4())
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        image_b64 = request.POST.get('imageBase64')
        imgstr = image_b64.split(',')[1]
        output = open(file_path, 'wb')
        decoded = base64.b64decode(imgstr)
        output.write(decoded)

        user_ids = []
        names = []
        score, idx = face_app.get_similarity(file_path, utils.EmbeddingsDataset().embeddings)
        os.remove(file_path)

        if score is not None:
            user = User.objects.get(id=utils.EmbeddingsDataset().user_ids[idx])
            if user:
                data = {
                    'id': user.id,
                    'name': user.username,
                    'score': round(score * 100, 2)
                }
                login(request, user)
                return JsonResponse(data)
        return HttpResponseServerError('Invalid user')


class NoPermission(TemplateView):
    template_name = 'no-permission.html'


class RedirectView(TemplateView):
    def get(self, request):
        if request.user.is_staff:
            return redirect('dashboard')
        else:
            return redirect('home')


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_users(['admin']), name='dispatch')
class DashboardView(TemplateView):
    def get(self, request):
        return render(request, 'dashboard.html', {})


@method_decorator(login_required(login_url='login'), name='dispatch')
class HomeView(TemplateView):
    def get(self, request):
        return render(request, 'common/home.html', {})


class LoginView(auth_views.LoginView):
    template_name = 'common/login.html'

    def get(self, request):
        utils.EmbeddingsDataset()
        return render(request, self.template_name, {'form': AuthenticationForm})


class LogoutView(auth_views.LogoutView):
    next_page = 'login'


class PasswordChangeView(auth_views.PasswordChangeView):
    success_url = reverse_lazy('redirect')
    template_name = 'common/password/password-change.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'common/password/password-reset-form.html'
    subject_template_name = 'common/password/password-reset-subject.txt'
    email_template_name = 'common/password/password-reset-email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'common/password/password-reset-done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'common/password/password-reset-confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'common/password/password-reset-complete.html'


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'common/register.html'
