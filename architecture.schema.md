# ReMASA Infrastructure Schema

## Code Repository
- **GitHub**: [https://github.com/jugauna/ReMASA-ID.git](https://github.com/jugauna/ReMASA-ID.git)

## Network Nodes
- **VPS DigitalOcean**: 67.207.83.113 (Host de la infraestructura)
- **Hostinger Server**: 89.117.7.185 (Backend de intranet.remasa.com)

## Domain Mapping
- `login.remasa.com`: Punto de entrada OAuth2.
- `intranet.remasa.com`: Proxy hacia Hostinger (WP).
- `invoice.remasa.com`: App local de extracción de facturas (Python/Django).
- `pyg.remasa.com`: App local de gestión de proyectos.
- `logs.remasa.com`: Acceso a Dozzle (Solo administradores).

## Auth Flow
1. User requests subdominio.remasa.com.
2. Nginx checks for OAuth2 session.
3. If no session, redirects to login.remasa.com -> Google Auth.
4. If @remasa.com, redirects back with X-Auth-Request-Email header.
5. Service grants access based on email header.

## Security Whitelist
- Domain: `@remasa.com`
- Manual Whitelist: `./config/authenticated_emails.txt`
- **IT Manager** (invoice / logs): `./nginx/includes/admin_allow.map` (Nginx devuelve 403 fuera de esta lista; debe alinearse con el hub en `dashboard/index.html`)