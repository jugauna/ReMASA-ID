# Changelog

## 2026-05-04 (Django + externos + portal login)
- Portal unificado: `proxy/custom_sign_in.html` (Google + formulario htpasswd), montado como `sign_in.html`; CSP login ajustada para estilos/JS inline.
- Servicio `remasa-id-admin`: Django `admin_app` (ExternalUser, signal `htpasswd`, admin listado rápido), SQLite `./data/db`, WhiteNoise + collectstatic.
- OAuth2 Proxy: `--htpasswd-file`, `--display-htpasswd-form=true`; rutas de config bajo `/opt/remasa/config`.
- Nginx: `admin.remasa.com` -> `remasa-id-admin:8000` (TLS, auth_request, solo IT Manager).
- Middleware `ProxyEmailAuthMiddleware` para sesión Django tras cabecera Nginx.

## 2026-05-04 (finalizacion produccion)
- Referencia de repo: `https://github.com/jugauna/ReMASA-ID.git`; VPS `67.207.83.113`, Hostinger `89.117.7.185`.
- Nginx: CSP estricta en login y apps; intranet sin CSP (WordPress); `proxy_ssl_server_name` y `Host` hacia Hostinger.
- Hardening modular: `hardening_base.conf`, `hardening_csp_login.conf`, `hardening_csp_apps.conf`.
- Persistencia: `./data/logs/nginx`, `./data/dozzle`; UI login y hub alineados a estética ReMASA; hub con rol IT Manager.
- README: instalacion Docker/Git en VPS, clonado, `.env`, certificados en `./data/certs/`.

## 2026-05-04 (produccion)
- VPS de referencia actualizada a `67.207.83.113` en documentacion y `.env.example`.
- Nginx: TLS en 443, redireccion 80->443, `server_tokens off`, cabeceras de seguridad.
- Certificados estandar: `/etc/nginx/certs/fullchain.pem` y `privkey.pem`.
- OAuth2: `OAUTH2_PROXY_REDIRECT_URL` fijo a `https://login.remasa.com/oauth2/callback`.
- Admins centralizados en `nginx/includes/admin_allow.map` para filtro 403 en invoice/logs.

## 2026-05-04
- Inicializacion de infraestructura ReMASA ID con `docker-compose.yml`.
- Centralizacion de configuracion en `.env.example`.
- Incorporacion de `nginx/default.conf.template` con `auth_request` y ruteo por subdominio.
- Filtro admin para `invoice.remasa.com` y `logs.remasa.com`.
- UI base: `proxy/custom.css`, `proxy/sign_in.html` y `dashboard/index.html`.
- Documentacion de despliegue y testing local en `README.md`.
