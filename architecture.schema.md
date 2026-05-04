# ReMASA Infrastructure Schema

## Code Repository
- **GitHub**: [https://github.com/jugauna/ReMASA-ID.git](https://github.com/jugauna/ReMASA-ID.git)

## Network Nodes
- **VPS DigitalOcean**: 67.207.83.113 (Host de la infraestructura)
- **Hostinger Server**: 89.117.7.185 (Backend de intranet.remasa.com)

## Domain Mapping
- `login.remasa.com`: Portal de identidad (OAuth2 Google + formulario htpasswd para externos).
- `intranet.remasa.com`: Proxy hacia Hostinger (WP).
- `invoice.remasa.com`: App local de extracción de facturas (Python/Django).
- `pyg.remasa.com`: App local de gestión de proyectos.
- `logs.remasa.com`: Acceso a Dozzle (Solo administradores).
- `admin.remasa.com`: Panel Django (`admin_app`) para gestionar usuarios externos y `externos.htpasswd` (solo IT Manager vía Nginx).

## Auth Flow
1. User requests subdominio.remasa.com.
2. Nginx checks for OAuth2 session.
3. If no session, redirects to login.remasa.com -> Google Auth **o** credencial externa (`externos.htpasswd`).
4. If @remasa.com (Google) o usuario htpasswd válido, OAuth2 Proxy emite sesión y cabeceras `X-Auth-Request-*`.
5. Service grants access based on email header (Google) o identidad htpasswd.
6. `admin.remasa.com`: tras OAuth2, Nginx restringe por `admin_allow.map`; Django usa `X-Auth-Request-Email` para sesión staff.

## Security Whitelist
- Domain: `@remasa.com`
- Manual Whitelist: `./config/authenticated_emails.txt`
- **IT Manager** (invoice / logs / admin): `./nginx/includes/admin_allow.map` (Nginx devuelve 403 fuera de esta lista; alinear con `dashboard/index.html` y usuario staff Django por email).
- **Usuarios externos**: `./config/externos.htpasswd` (regenerado por `admin_app` vía `htpasswd -b -B`).