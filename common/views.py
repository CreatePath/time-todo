from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AccountUpdateForm

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
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'common/sign_up.html', context)
    
    def post(self, request):
        form = SignUpForm(request.POST)

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



class AccountUpdateView(View):
    def get(self, request):
        form = AccountUpdateForm()
        context = {'form': form}
        return render(request, 'common/update_account.html', context)
    
    def patch(self, request):
        form = SignUpForm(request.POST)

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

    def delete(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404("사용자를 찾을 수 없습니다.")

        if request.user != user:
            return JsonResponse({"message": "탈퇴 권한이 없습니다."}, status=401)

        user.delete()
        return JsonResponse({"message": "탈퇴하셨습니다."})



@login_required(redirect_field_name="/common/mypage")
def mypage(request, username):
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



def logout_view(request):
    logout(request)
    return JsonResponse({"message": "로그아웃하셨습니다."}, status=200)