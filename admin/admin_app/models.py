from django.db import models


class ExternalUser(models.Model):
    """Usuario externo autenticado vía htpasswd (OAuth2 Proxy)."""

    username = models.CharField(max_length=150, unique=True, db_index=True)
    password_plain = models.TextField(
        help_text="Contraseña en claro: solo para regenerar externo.htpasswd vía htpasswd. "
        "Restringir acceso al panel y al disco; valorar cifrado en reposo en evoluciones."
    )
    empresa = models.CharField(max_length=200)
    activo = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["username"]
        verbose_name = "Usuario externo"
        verbose_name_plural = "Usuarios externos"

    def __str__(self):
        return f"{self.username} ({self.empresa})"
