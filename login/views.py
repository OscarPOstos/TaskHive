from django.contrib.auth import authenticate, login
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