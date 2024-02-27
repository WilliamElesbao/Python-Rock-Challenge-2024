from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth

# Create your views here.


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email inválido!'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Esse e-mail já foi cadastrado!'}, status=409)
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'nome de usuário deve conter caracteres alfanuméricos!'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Nome de usuário já em uso, escolha outro!'}, status=409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'A senha precisa conter mais de 6 caracteres')
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = True
                user.save()
                
                messages.success(request, 'Conta criada com sucesso!')
                return render(request, 'authentication/login.html')

        return render(request, 'authentication/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Bem vindo(a), ' +
                                     user.username)
                    return redirect('investments')
                
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Credenciais inválidas, tente novamente!')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Preencha todos os campos!')
        return render(request, 'authentication/login.html')

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'Logout realizado com sucesso!')
        return redirect('login')