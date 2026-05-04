# ReMASA ID

Infraestructura de **identidad y acceso** para `remasa.com`: OAuth2 Proxy (Google), Nginx (TLS y rutas) y Dozzle.  
Repositorio: [https://github.com/jugauna/ReMASA-ID.git](https://github.com/jugauna/ReMASA-ID.git)

**Nodos de referencia**

| Rol | Valor |
|-----|--------|
| VPS producción (DigitalOcean) | `67.207.83.113` |
| Hostinger (WordPress intranet) | `89.117.7.185` |

---

## 1) Preparar la VPS (`67.207.83.113`)

Conéctate por SSH (usuario según tu servidor, ej. `root`):

```bash
ssh root@67.207.83.113
```

### Instalar Git

Ubuntu / Debian:

```bash
apt update
apt install -y git ca-certificates curl
```

### Instalar Docker Engine y Docker Compose

```bash
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker
docker compose version
```

---

## 2) Clonar el repositorio

```bash
cd /opt
git clone https://github.com/jugauna/ReMASA-ID.git
cd ReMASA-ID
```

---

## 3) Configurar variables de entorno

```bash
cp .env.example .env
nano .env
```

Completa al menos:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `OAUTH2_PROXY_COOKIE_SECRET` (ver sección siguiente)

El callback OAuth2 está fijado en `docker-compose.yml` como  
`https://login.remasa.com/oauth2/callback` y debe coincidir con **Google Cloud Console**.

### Generar `OAUTH2_PROXY_COOKIE_SECRET` (32 bytes en base64)

```bash
openssl rand -base64 32
```

Pega el resultado en `.env`.

---

## 4) Certificados TLS en `./data/certs/`

Antes del primer `docker compose up`, coloca en el servidor:

```text
./data/certs/fullchain.pem
./data/certs/privkey.pem
```

Ejemplo tras usar Let’s Encrypt en el host:

```bash
install -d -m 0750 ./data/certs
cp /ruta/a/fullchain.pem ./data/certs/fullchain.pem
cp /ruta/a/privkey.pem   ./data/certs/privkey.pem
chmod 0644 ./data/certs/fullchain.pem
chmod 0600 ./data/certs/privkey.pem
```

Nginx los monta en `/etc/nginx/certs/`. El puerto **80** solo redirige a **HTTPS (443)**.

---

## 5) DNS

Apunta los registros A de:

- `login.remasa.com`, `intranet.remasa.com`, `invoice.remasa.com`, `pyg.remasa.com`, `logs.remasa.com`

hacia **`67.207.83.113`**.

---

## 6) Levantar el stack

```bash
docker compose pull
docker compose up -d
docker compose ps
```

**Persistencia en disco (bind mounts)**

| Ruta en el repo | Uso |
|-----------------|-----|
| `./config` | Listas y configuración (p. ej. `authenticated_emails.txt`) |
| `./data/certs` | Certificados TLS |
| `./data/logs/nginx` | Logs de acceso y error de Nginx |
| `./data/dozzle` | Datos opcionales de Dozzle |

Los contenedores usan el prefijo **`remasa-id-`**. Nginx incluye `extra_hosts: host.docker.internal:host-gateway` para alcanzar apps Python en el **host** (puertos `PORT_INVOICE_APP` / `PORT_PYG_APP`).

---

## 7) Comprobaciones

- `https://login.remasa.com` — flujo OAuth2.
- `https://intranet.remasa.com` — proxy a Hostinger (`89.117.7.185`), cabecera `Host: intranet.remasa.com`.
- `https://invoice.remasa.com` — app en el host; **403** si el email no está en `nginx/includes/admin_allow.map` (IT Manager).
- `https://pyg.remasa.com` — app en el host (cualquier usuario autenticado `@remasa.com`, salvo restricciones propias de la app).
- `https://logs.remasa.com` — Dozzle; **403** fuera del mapa de IT Manager.
- `http://127.0.0.1:${PORT_LOGS}` — Dozzle por puerto directo (si aplica tu política de red).

---

## 8) Modo local (opcional)

Añade a `hosts` (`C:\Windows\System32\drivers\etc\hosts` o `/etc/hosts`):

```text
127.0.0.1 login.remasa.com
127.0.0.1 intranet.remasa.com
127.0.0.1 invoice.remasa.com
127.0.0.1 pyg.remasa.com
127.0.0.1 logs.remasa.com
```

Necesitas certificados locales válidos o un proxy de confianza para TLS.

---

## 9) IT Manager (invoice / logs)

Edita `nginx/includes/admin_allow.map` (una línea por email: `correo@remasa.com 1;`) y reinicia Nginx:

```bash
docker compose restart remasa-id-nginx
```

El hub estático `dashboard/index.html` usa la misma lista en JavaScript solo para la UX; la **autorización real** la aplica Nginx.
