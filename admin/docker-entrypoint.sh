#!/bin/sh
# Asegura SQLite, htpasswd inicial y migraciones antes de gunicorn.
set -e
install -d -m 0775 /app/db
install -d -m 0775 /opt/remasa/config
if [ ! -s /opt/remasa/config/externos.htpasswd ]; then
  htpasswd -cbB /opt/remasa/config/externos.htpasswd "__bootstrap__" "__change_me__"
fi
python manage.py migrate --noinput
exec "$@"
