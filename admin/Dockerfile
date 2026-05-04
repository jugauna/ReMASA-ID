# ReMASA ID — panel Django (admin_app) + htpasswd (apache2-utils)
FROM python:3.11-alpine

RUN apk add --no-cache apache2-utils

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

# Estáticos del admin Django (WhiteNoise)
RUN DJANGO_SECRET_KEY=collectstatic-build DJANGO_ALLOWED_HOSTS=localhost \
    python manage.py collectstatic --noinput

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=remasa_id_core.settings

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "/app/docker-entrypoint.sh"]
CMD ["gunicorn", "remasa_id_core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "2", "--timeout", "120"]
