from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views import View
import json

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Validaciones básicas
            if not username or not password:
                return JsonResponse({'error': 'Usuario y contraseña son obligatorios.'}, status=400)

            # Autenticar al usuario
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Iniciar sesión
                return JsonResponse({'message': 'Inicio de sesión exitoso.'})
            else:
                return JsonResponse({'error': 'Credenciales inválidas.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')

            # Validaciones básicas
            if not username or not password or not email:
                return JsonResponse({'error': 'Todos los campos son obligatorios.'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'El usuario ya existe.'}, status=400)

            # Crear el usuario
            user = User.objects.create(
                username=username,
                password=make_password(password),  # Hashear la contraseña
                email=email
            )
            return JsonResponse({'message': 'Usuario registrado con éxito.'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class LogoutView(View):
    def post(self, request):
        try:
            if request.user.is_authenticated:
                logout(request)  # Cierra la sesión del usuario
                return JsonResponse({'message': 'Sesión cerrada exitosamente.'}, status=200)
            else:
                return JsonResponse({'error': 'No estás autenticado.'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)