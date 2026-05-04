import logging
import subprocess
from pathlib import Path

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from admin_app.models import ExternalUser

logger = logging.getLogger(__name__)

HTPASSWD_PATH = Path("/opt/remasa/config/externos.htpasswd")


def _write_bootstrap_file() -> None:
    HTPASSWD_PATH.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["htpasswd", "-cbB", str(HTPASSWD_PATH), "__bootstrap__", "__change_me__"],
        check=True,
        capture_output=True,
    )


def rebuild_externos_htpasswd() -> None:
    """Regenera externo.htpasswd a partir de usuarios activos (htpasswd -b -B)."""
    users = list(
        ExternalUser.objects.filter(activo=True).exclude(password_plain="").order_by("username")
    )
    if not users:
        _write_bootstrap_file()
        return

    HTPASSWD_PATH.parent.mkdir(parents=True, exist_ok=True)
    first = True
    for u in users:
        cmd = ["htpasswd", "-b", "-B"]
        if first:
            cmd.insert(1, "-c")
            first = False
        cmd.extend([str(HTPASSWD_PATH), u.username, u.password_plain])
        subprocess.run(cmd, check=True, capture_output=True)


@receiver(post_save, sender=ExternalUser)
def external_user_post_save(sender, instance, **kwargs):
    try:
        rebuild_externos_htpasswd()
    except subprocess.CalledProcessError as e:
        err = getattr(e, "stderr", None) or b""
        logger.exception("htpasswd falló post_save: %s", err)


@receiver(post_delete, sender=ExternalUser)
def external_user_post_delete(sender, instance, **kwargs):
    try:
        rebuild_externos_htpasswd()
    except subprocess.CalledProcessError as e:
        err = getattr(e, "stderr", None) or b""
        logger.exception("htpasswd falló post_delete: %s", err)
