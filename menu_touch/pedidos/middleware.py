from django.shortcuts import redirect
from django.conf import settings

class CheckLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si el usuario no está autenticado y no está en la página de login
        if not request.session.get('mesa_token') and request.path != settings.LOGIN_URL:
            # Redirigir a la página de login
            return redirect(settings.LOGIN_URL)

        # Continuar con la respuesta normal si el usuario está autenticado
        response = self.get_response(request)
        return response
