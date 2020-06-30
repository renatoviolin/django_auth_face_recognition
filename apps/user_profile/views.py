from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm, ProfileForm
from django.contrib import messages
from auth_face import face_app
import numpy as np


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get(self, request):
        user = request.user
        profile = user.profile
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)


class ProfileUpdateView(TemplateView):
    template_name = 'profile-form.html'

    def get(self, request):
        user = request.user
        profile = user.profile
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = request.user
        profile = user.profile
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            url = profile.profile_image.url[1:]
            e = face_app.generate_emb(url)
            profile.embedding = e.tostring()
            profile.save()

            messages.success(request, 'Your profile was successfully updated!')
            return redirect(reverse_lazy('profile'))

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return self.render_to_response(context)
