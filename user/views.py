from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView, View
from django.http.response import JsonResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
# Create your views here.
from user.forms import UserPasswordForm
from user.models import HxUser


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        form = AuthenticationForm(request, **{
            'data': request.POST,
            'files': request.FILES,
        })
        if not form.is_valid():
            return JsonResponse({"status": -1, "message": "login failed!"})
        auth_login(self.request, form.get_user())
        return JsonResponse({"status": 0, "message": "ok", 'data': ""})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserInfoView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user: HxUser = request.user
            return JsonResponse({
                "is_authenticated": True,
                "user": {
                    "username": user.username,
                    "email": user.email,
                    "name": user.name,
                    "date_of_enter": user.date_of_enter,
                },
            })
        else:
            return JsonResponse({
                "is_authenticated": False,
                "user": None,
            })

    # def post(self, request):
    #     if request.user.is_authenticated:
    #         form = UserPasswordForm(request, **{
    #             "instance": request.user,
    #             'data': request.POST,
    #             'files': request.FILES,
    #         })
    #         if not form.is_valid():
    #             return JsonResponse({"status": -1, "message": "form not valid"})
    #         else:
    #             return JsonResponse({"status": 0, "message": "ok"})
    #     else:
    #         return JsonResponse({"status": -2, "message": "user not authenticated"})


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LogoutView(View):
    def post(self, request):
        auth_logout(request)
        return JsonResponse({
            "status": 0,
            "message": "ok",
        })


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ChangePasswordView(View):

    def post(self, request):
        form = PasswordChangeForm(**{
            "user": request.user,
            'data': request.POST,
            'files': request.FILES,
        })
        if not form.is_valid():
            return JsonResponse({"status": -1, "errors": form.errors})
        form.save()
        return JsonResponse({"status": 0, "errors": []})

