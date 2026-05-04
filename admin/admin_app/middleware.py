"""
Confía en X-Auth-Request-Email inyectado por Nginx (red interna Docker).
Tras OAuth2, inicia sesión Django si existe un usuario staff con ese email.
"""
from django.contrib.auth import get_user_model, login
from django.utils.deprecation import MiddlewareMixin


class ProxyEmailAuthMiddleware(MiddlewareMixin):
    """Si llega cabecera de identidad y existe usuario staff con ese email, inicia sesión."""

    def process_request(self, request):
        if request.user.is_authenticated:
            return None
        email = (request.META.get("HTTP_X_AUTH_REQUEST_EMAIL") or "").strip().lower()
        if not email:
            return None
        User = get_user_model()
        user = User.objects.filter(email__iexact=email, is_staff=True, is_active=True).first()
        if user:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return None
