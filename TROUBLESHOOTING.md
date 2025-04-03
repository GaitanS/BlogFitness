# Ghid de Depanare pentru GhidulFit365

Acest document oferă soluții pentru problemele comune care pot apărea în timpul instalării și utilizării site-ului GhidulFit365.

## Probleme de Autentificare în Panoul de Administrare

### Problema: Nu poți rămâne autentificat în panoul de administrare

Dacă te autentifici cu succes, dar ești redirecționat înapoi la pagina de login în loc să ajungi la panoul de administrare, încearcă următoarele soluții:

#### 1. Verifică setările pentru cookie-uri în settings.py

```python
# Asigură-te că aceste linii sunt comentate sau eliminate
# SESSION_COOKIE_DOMAIN = ".ghidulfit365.ro"
# CSRF_COOKIE_DOMAIN = ".ghidulfit365.ro"

# Adaugă aceste setări
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 1209600  # 2 săptămâni în secunde
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Dezactivează temporar securitatea cookie-urilor pentru depanare
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

#### 2. Verifică configurația Nginx

Asigură-te că Nginx transmite corect headerele pentru cookie-uri:

```nginx
location / {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-Server $host;
    proxy_redirect off;
    proxy_pass http://127.0.0.1:8001;
    
    # Simplifică gestionarea cookie-urilor
    proxy_cookie_path / /;
}
```

#### 3. Verifică jurnalele pentru erori

```bash
sudo tail -f /var/log/gunicorn/error.log
sudo tail -f /var/log/nginx/error.log
```

#### 4. Activează modul de depanare

Setează `DEBUG = True` în settings.py pentru a vedea mai multe informații despre erori.

#### 5. Șterge cookie-urile din browser

Șterge toate cookie-urile pentru domeniul ghidulfit365.ro și încearcă să te autentifici din nou.

#### 6. Verifică dacă există probleme cu sesiunile în baza de date

```bash
cd /var/www/ghidulfit365
source venv/bin/activate
python manage.py shell
```

În shell-ul Python, execută:

```python
from django.contrib.sessions.models import Session
# Verifică câte sesiuni există
print(Session.objects.count())
# Șterge toate sesiunile
Session.objects.all().delete()
exit()
```

#### 7. Creează un utilizator nou pentru testare

```bash
cd /var/www/ghidulfit365
source venv/bin/activate
python manage.py createsuperuser
```

## Probleme cu Gunicorn

### Problema: Gunicorn nu pornește sau se oprește imediat

#### 1. Verifică jurnalele Gunicorn

```bash
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/gunicorn/error.log
```

#### 2. Verifică dacă există erori de sintaxă în settings.py

```bash
cd /var/www/ghidulfit365
source venv/bin/activate
python manage.py check
```

#### 3. Verifică dacă Gunicorn poate porni manual

```bash
cd /var/www/ghidulfit365
source venv/bin/activate
gunicorn fitness_blog.wsgi:application --bind=0.0.0.0:8001 --log-level=debug
```

## Probleme cu Nginx

### Problema: Nginx returnează eroarea 502 Bad Gateway

#### 1. Verifică dacă Gunicorn rulează

```bash
sudo systemctl status gunicorn
```

#### 2. Verifică dacă Nginx este configurat corect

```bash
sudo nginx -t
```

#### 3. Verifică dacă portul configurat în Nginx corespunde cu cel din Gunicorn

Asigură-te că în fișierul nginx-ghidulfit365, toate liniile `proxy_pass` folosesc portul corect:

```nginx
proxy_pass http://127.0.0.1:8001;
```

Și în gunicorn.conf.py:

```python
bind = "0.0.0.0:8001"
```

## Probleme cu Baza de Date

### Problema: Erori legate de baza de date

#### 1. Verifică dacă PostgreSQL rulează

```bash
sudo systemctl status postgresql
```

#### 2. Verifică dacă utilizatorul și baza de date există

```bash
sudo -u postgres psql -c "\du"
sudo -u postgres psql -c "\l"
```

#### 3. Verifică dacă migrările au fost aplicate corect

```bash
cd /var/www/ghidulfit365
source venv/bin/activate
python manage.py showmigrations
```

## Probleme cu Permisiunile Fișierelor

### Problema: Erori de permisiuni

#### 1. Verifică permisiunile directorului proiectului

```bash
ls -la /var/www/ghidulfit365
```

#### 2. Setează permisiunile corecte

```bash
sudo chown -R www-data:www-data /var/www/ghidulfit365
sudo chmod -R 755 /var/www/ghidulfit365
```

## Probleme cu SSL/HTTPS

### Problema: Certificatul SSL nu funcționează corect

#### 1. Verifică dacă certificatul există

```bash
sudo ls -la /etc/letsencrypt/live/ghidulfit365.ro/
```

#### 2. Reînnoiește certificatul

```bash
sudo certbot renew
```

#### 3. Verifică configurația Nginx pentru SSL

```bash
sudo grep -r "ssl_certificate" /etc/nginx/sites-available/
```

## Dacă Nimic Nu Funcționează

Dacă ai încercat toate soluțiile de mai sus și tot întâmpini probleme, consideră următoarele opțiuni:

1. Reinstalează aplicația de la zero folosind scriptul deploy.sh
2. Consultă documentația Django pentru probleme specifice
3. Caută ajutor pe forumuri specializate sau Stack Overflow
