import json

from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import AccountForm

class LoginView(View):
    def get(self, request):
        return render(request, "common/login.html", context={"login_failed": False})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, "common/login.html", context={"login_failed": True})



class SignUpView(View):
    def get(self, request):
        form = AccountForm()
        context = {'form': form}
        return render(request, 'common/sign_up.html', context)
    
    def post(self, request):
        form = AccountForm(request.POST)

        if not form.is_valid():
            return JsonResponse({"message": "글자 수가 너무 많아 회원가입에 실패하였습니다."}, status=400)

        if User.objects.filter(username=form.cleaned_data["username"]):
            return JsonResponse({"message": "이미 존재하는 아이디입니다."}, status=400)

        user = User.objects.create_user(username=form.cleaned_data["username"],
                                    password=form.cleaned_data["password"],
                                    first_name=form.cleaned_data["first_name"],
                                    last_name=form.cleaned_data["last_name"],
                                    email=form.cleaned_data["email"])
        user.save()

        return JsonResponse({"message": "회원가입에 성공하였습니다!"}, status=200)




class MyPageView(LoginRequiredMixin, View):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("사용자를 찾을 수 없습니다.")

        context = {"username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "joined_date": user.date_joined}

        return render(request, "common/mypage.html", context)

    @method_decorator(require_http_methods("DELETE"))
    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("사용자를 찾을 수 없습니다.")

        if request.user != user:
            return JsonResponse({"message": "탈퇴` 권한이 없습니다."}, status=401)

        user.delete()
        return JsonResponse({"message": "탈퇴하셨습니다."})



class AccountUpdateView(LoginRequiredMixin, View):
    def get(self, request, username):
        form = AccountForm()
        context = {'form': form, 'username': username}
        return render(request, 'common/update_account.html', context)

    @method_decorator(require_http_methods("PATCH"))
    def patch(self, request, username):
        data = json.loads(request.body.decode('utf-8'))
        user = request.user
        form = AccountForm(data)
        print(data)

        if not form.is_valid():
            print("error")
            print(form.errors)
            return JsonResponse({"message": form.errors}, status=400)

        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        
        user.save()

        return JsonResponse({"message": "회원정보가 수정되었습니다."}, status=200)



def logout_view(request):
    logout(request)
    return JsonResponse({"message": "로그아웃하셨습니다."}, status=200)