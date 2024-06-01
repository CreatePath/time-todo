from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from .forms import SignUpForm

class LoginView(View):
    def get(self, request):
        return render(request, "common/login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('/')
        return redirect("common:login")



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

def logout_view(request):
    logout(request)
    return redirect("common:login")