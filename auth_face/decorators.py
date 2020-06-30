from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render


def allowed_users(allowed_roles):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user_groups = []
            for group in request.user.groups.all():
                user_groups.append(group.name)

            g1 = set(allowed_roles)
            g2 = set(user_groups)
            has_permission = g1.intersection(g2)

            if has_permission or request.user.is_staff:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('no_permission')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        user_groups = []
        for group in request.user.groups.all():
            user_groups.append(group.name)
        if 'admin' in user_groups:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('patient_tests', uid=request.user.patient.id)
    return wrapper_func
