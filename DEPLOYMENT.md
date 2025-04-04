# Instrucțiuni de Deployment pentru GhidulFit365

Acest document conține instrucțiuni detaliate pentru deployment-ul aplicației GhidulFit365 pe un server VPS cu Ubuntu.

## Cerințe

- Ubuntu 24.04 LTS
- Python 3.12+
- PostgreSQL 16+
- Nginx 1.24+
- Domeniu configurat (ghidulfit365.ro)

## Pași de Deployment

### Metoda recomandată: Crearea unui proiect Django nou

Din experiență, cea mai fiabilă metodă este să creăm un proiect Django nou și să configurăm totul de la zero. Această abordare evită multe probleme potențiale cu structura proiectului sau configurația.

```bash
# 1. Actualizează sistemul
apt update && apt upgrade -y

# 2. Instalează dependențele necesare
apt install -y git python3 python3-pip python3-venv postgresql postgresql-contrib nginx certbot python3-certbot-nginx python3-dev libpq-dev gcc build-essential

# 3. Creează directorul pentru proiect
mkdir -p /var/www/ghidulfit365
cd /var/www/ghidulfit365

# 4. Creează și activează mediul virtual
python3 -m venv venv
source venv/bin/activate

# 5. Instalează Django și alte dependențe
pip install django gunicorn psycopg2-binary django-jazzmin django-ckeditor Pillow

# 6. Creează un proiect Django nou
django-admin startproject fitness_blog .

# 7. Creează o aplicație blog
python manage.py startapp blog
```

Acum poți configura proiectul nou creat și apoi să copiezi conținutul (modele, view-uri, template-uri) din repository-ul original.

### 8. Configurează baza de date PostgreSQL

```bash
sudo -u postgres psql -c "CREATE DATABASE ghidulfit365;"
sudo -u postgres psql -c "CREATE USER ghidulfit365_user WITH PASSWORD 'adrianvilea2025';"
sudo -u postgres psql -c "ALTER ROLE ghidulfit365_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE ghidulfit365_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE ghidulfit365_user SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ghidulfit365 TO ghidulfit365_user;"
```

#### Important: Acordă permisiuni pentru schema public

Este esențial să acorzi permisiuni pentru schema public utilizatorului bazei de date. Fără aceste permisiuni, vei primi eroarea `permission denied for schema public` când încerci să aplici migrările Django:

```bash
sudo -u postgres psql -d ghidulfit365 -c "GRANT ALL ON SCHEMA public TO ghidulfit365_user;"
```

Dacă tot întâmpini probleme cu permisiunile, poți încerca să faci utilizatorul proprietar al bazei de date:

```bash
sudo -u postgres psql -c "ALTER DATABASE ghidulfit365 OWNER TO ghidulfit365_user;"
```

### 9. Configurează fișierul settings.py

Editează fișierul `/var/www/ghidulfit365/fitness_blog/settings.py` pentru a include setările necesare pentru baza de date și alte configurări:

```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['ghidulfit365.ro', 'www.ghidulfit365.ro', 'localhost', '127.0.0.1', '69.62.119.15']

# Add CSRF trusted origins for HTTPS
CSRF_TRUSTED_ORIGINS = [
    "https://ghidulfit365.ro",
    "https://www.ghidulfit365.ro",
    "http://69.62.119.15",
]

# Cookie settings
# DO NOT set cookie domains - this causes login issues with IP addresses
# SESSION_COOKIE_DOMAIN = None
# CSRF_COOKIE_DOMAIN = None

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Proxy settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ghidulfit365',
        'USER': 'ghidulfit365_user',
        'PASSWORD': 'adrianvilea2025',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/ghidulfit365/staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/ghidulfit365/media'
```

### 9. Aplică migrările și creează un superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

#### Probleme cu comanda createsuperuser

Dacă întâmpini eroarea `Unknown command: 'createsuperuser'` și comanda nu apare în lista de comenzi disponibile când rulezi `python manage.py help`, există o problemă cu instalarea sau configurarea Django. Verifică următoarele:

1. **Verifică dacă aplicația `django.contrib.auth` este inclusă în `INSTALLED_APPS`**:

```bash
cat fitness_blog/settings.py | grep -A 10 "INSTALLED_APPS"
```

Asigură-te că lista include `'django.contrib.auth'`:

```python
INSTALLED_APPS = [
    ...
    'django.contrib.auth',
    ...
]
```

2. **Verifică dacă fișierul settings.py este configurat corect**:

Dacă ai clonat repository-ul în `/var/www/ghidulfit365` dar structura proiectului este diferită, este posibil ca Django să nu găsească fișierul settings.py corect. Verifică structura proiectului:

```bash
ls -la
find . -name "settings.py"
```

3. **Recreează proiectul Django de la zero**:

Dacă tot întâmpini probleme, poți crea un proiect Django nou și apoi să copiezi fișierele necesare:

```bash
cd /tmp
django-admin startproject tempproject
cd /var/www/ghidulfit365
cp /tmp/tempproject/manage.py .
cp -r /tmp/tempproject/tempproject/* fitness_blog/
```

Acum editează fișierul settings.py pentru a include aplicațiile și setările tale.

4. **Asigură-te că fiecare comandă este rulată separat**:

```bash
# Corect - fiecare comandă pe o linie separată
python manage.py migrate
python manage.py createsuperuser

# Incorect - ambele comenzi pe aceeași linie
python manage.py migrate python manage.py createsuperuser
```

#### Crearea unui superuser prin shell

Alternativ, poți crea un superuser folosind shell-ul Django:

```bash
python manage.py shell
```

În shell-ul Python, execută:

```python
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'parola')
exit()
```

### 10. Colectează fișierele statice

```bash
python manage.py collectstatic --noinput
```

### 11. Configurează Gunicorn

Creează fișierul `/var/www/ghidulfit365/gunicorn.conf.py`:

```python
import multiprocessing

# Server socket
bind = "0.0.0.0:8001"  # Asigură-te că acest port corespunde cu cel din configurația Nginx
workers = multiprocessing.cpu_count() * 2 + 1

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "ghidulfit365"

# Worker timeout
timeout = 30

# Keep the workers alive
keepalive = 2
```

### 12. Configurează serviciul systemd pentru Gunicorn

Creează fișierul `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=Gunicorn daemon for GhidulFit365
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ghidulfit365
ExecStart=/var/www/ghidulfit365/venv/bin/gunicorn --config /var/www/ghidulfit365/gunicorn.conf.py fitness_blog.wsgi:application
Restart=on-failure
RestartSec=5s
Environment="DJANGO_DEBUG=False"

# Increase timeout for startup
TimeoutStartSec=600

# Log to journal
StandardOutput=journal
StandardError=journal
SyslogIdentifier=gunicorn

[Install]
WantedBy=multi-user.target
```

### 13. Configurează Nginx

Creează fișierul `/etc/nginx/sites-available/ghidulfit365`:

```nginx
# HTTP server - only redirects to HTTPS
server {
    listen 80;
    server_name ghidulfit365.ro www.ghidulfit365.ro;

    # Redirect HTTP to HTTPS
    return 301 https://$host$request_uri;
}

# HTTP server for IP address - allows direct access without SSL
server {
    listen 80;
    server_name 69.62.119.15;

    # For initial setup without SSL
    location /static/ {
        alias /var/www/ghidulfit365/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /var/www/ghidulfit365/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Special location for ads.txt to ensure it's always accessible
    location = /ads.txt {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8001/ads.txt;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8001;

        # Add these headers to help with cookie issues
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Server $host;

        # Simplify cookie handling to avoid authentication issues
        proxy_cookie_path / /;
    }
}

# Redirect www to non-www HTTPS
server {
    listen 443 ssl http2;
    server_name www.ghidulfit365.ro;
    return 301 https://ghidulfit365.ro$request_uri;

    ssl_certificate /etc/letsencrypt/live/ghidulfit365.ro/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ghidulfit365.ro/privkey.pem;
}

# Main HTTPS server block
server {
    listen 443 ssl http2;
    server_name ghidulfit365.ro;

    ssl_certificate /etc/letsencrypt/live/ghidulfit365.ro/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/ghidulfit365.ro/privkey.pem;

    client_max_body_size 100M;

    access_log /var/log/nginx/ghidulfit365.access.log;
    error_log /var/log/nginx/ghidulfit365.error.log;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        alias /var/www/ghidulfit365/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /var/www/ghidulfit365/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Special location for ads.txt to ensure it's always accessible
    location = /ads.txt {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8001/ads.txt;
    }

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme; # Django uses this to know it's behind HTTPS
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8001;

        # Add these headers to help with cookie issues
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Server $host;

        # Simplify cookie handling to avoid authentication issues
        proxy_cookie_path / /;
    }
}
```

### 14. Activează configurația Nginx și elimină configurația implicită

```bash
rm -f /etc/nginx/sites-enabled/default
ln -sf /etc/nginx/sites-available/ghidulfit365 /etc/nginx/sites-enabled/
```

### 15. Configurează ads.txt pentru Google AdSense

```bash
mkdir -p /var/www/ghidulfit365/templates
echo "google.com, pub-5227061222218296, DIRECT, f08c47fec0942fa0" > /var/www/ghidulfit365/templates/ads.txt
```

### 16. Setează permisiunile corecte

```bash
chown -R www-data:www-data /var/www/ghidulfit365
chmod -R 755 /var/www/ghidulfit365
chown -R www-data:www-data /var/log/gunicorn
```

### 17. Pornește serviciile

```bash
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn
systemctl restart nginx
```

### 18. Configurează SSL cu Let's Encrypt

```bash
certbot --nginx -d ghidulfit365.ro -d www.ghidulfit365.ro
```

### 19. Verifică dacă site-ul este accesibil

```bash
curl -I https://ghidulfit365.ro
```

## Depanare

### Probleme cu comenzile Django

Dacă comenzile Django precum `migrate`, `createsuperuser` sau `collectstatic` nu sunt recunoscute, verifică următoarele:

#### 1. Mediul virtual este activat

Asigură-te că mediul virtual este activat (ar trebui să vezi `(venv)` la începutul promptului):

```bash
source venv/bin/activate
```

#### 2. Django este instalat corect

Verifică dacă Django este instalat în mediul virtual:

```bash
pip list | grep Django
```

Dacă nu este instalat, instalează-l:

```bash
pip install Django==5.0.2
```

#### 3. Structura proiectului este corectă

Asigură-te că te afli în directorul care conține fișierul `manage.py`:

```bash
ls -la | grep manage.py
```

#### 4. Comenzile sunt executate separat

Asigură-te că fiecare comandă este executată separat, nu pe aceeași linie:

```bash
# Corect
python manage.py migrate
python manage.py createsuperuser

# Incorect
python manage.py migrate python manage.py createsuperuser
```

### Probleme de autentificare în panoul de administrare

Dacă întâmpini probleme de autentificare în panoul de administrare, verifică următoarele:

1. Asigură-te că `SESSION_COOKIE_DOMAIN` și `CSRF_COOKIE_DOMAIN` sunt comentate sau setate la `None` în settings.py.
2. Setează temporar `DEBUG = True` pentru a vedea mai multe informații despre erori.
3. Dezactivează temporar setările de securitate stricte:
   ```python
   SESSION_COOKIE_SECURE = False
   CSRF_COOKIE_SECURE = False
   ```
4. Asigură-te că Nginx transmite corect headerele pentru cookie-uri.
5. Verifică jurnalele pentru erori:
   ```bash
   sudo tail -f /var/log/gunicorn/error.log
   sudo tail -f /var/log/nginx/error.log
   ```

### Probleme cu Gunicorn

Dacă Gunicorn nu pornește sau se oprește imediat, verifică jurnalele:

```bash
sudo journalctl -u gunicorn -f
```

### Probleme cu Nginx

Dacă Nginx returnează eroarea 502 Bad Gateway, verifică dacă Gunicorn rulează și dacă portul configurat în Nginx corespunde cu cel din Gunicorn.

### Probleme cu baza de date

Dacă întâmpini erori legate de baza de date, verifică următoarele:

#### 1. Permisiuni pentru schema public

Eroarea `permission denied for schema public` apare când utilizatorul bazei de date nu are permisiuni pentru schema public:

```bash
sudo -u postgres psql -d ghidulfit365 -c "GRANT ALL ON SCHEMA public TO ghidulfit365_user;"
```

#### 2. Proprietarul bazei de date

Dacă tot întâmpini probleme, poți face utilizatorul proprietar al bazei de date:

```bash
sudo -u postgres psql -c "ALTER DATABASE ghidulfit365 OWNER TO ghidulfit365_user;"
```

#### 3. Probleme cu migrările

Dacă migrările eșuează cu erori legate de tabele care există deja, poți încerca să resetezi migrările pentru o aplicație specifică:

```bash
python manage.py migrate --fake sessions zero
python manage.py migrate sessions
```

## Actualizarea aplicației

Pentru a actualiza aplicația cu modificări noi din repository:

```bash
cd /var/www/ghidulfit365
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
systemctl restart gunicorn
```
