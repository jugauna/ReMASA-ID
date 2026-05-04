from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExternalUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("username", models.CharField(db_index=True, max_length=150, unique=True)),
                (
                    "password_plain",
                    models.TextField(
                        help_text="Contraseña en claro para regenerar externo.htpasswd (uso interno controlado)."
                    ),
                ),
                ("empresa", models.CharField(max_length=200)),
                ("activo", models.BooleanField(db_index=True, default=True)),
            ],
            options={
                "verbose_name": "Usuario externo",
                "verbose_name_plural": "Usuarios externos",
                "ordering": ["username"],
            },
        ),
    ]
