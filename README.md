# GhidulFit365 - Blog de Fitness și Nutriție

Un blog modern despre fitness, nutriție și stil de viață sănătos.

## Tehnologii folosite

- Django 5.2
- PostgreSQL
- Nginx
- Gunicorn
- Bootstrap 4
- Font Awesome 5

## Cerințe

- Python 3.12+
- PostgreSQL 16+
- Nginx 1.24+

## Instalare și configurare pentru dezvoltare

1. Clonează repository-ul:

```bash
git clone https://github.com/GaitanS/BlogFitness.git
cd BlogFitness
```

2. Creează și activează un mediu virtual:

```bash
python3 -m venv venv
source venv/bin/activate  # Pe Windows: venv\Scripts\activate
```

3. Instalează dependențele:

```bash
pip install -r requirements.txt
```

4. Configurează baza de date în `fitness_blog/settings.py`.

5. Aplică migrările și creează un superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Rulează serverul de dezvoltare:

```bash
python manage.py runserver
```

7. Accesează site-ul în browser la `http://localhost:8000`.

## Deployment pe VPS

Vezi [DEPLOYMENT.md](DEPLOYMENT.md) pentru instrucțiuni detaliate de deployment pe un VPS.

## Depanare probleme de autentificare

Dacă întâmpini probleme de autentificare în panoul de administrare, verifică următoarele:

1. Asigură-te că `SESSION_COOKIE_DOMAIN` și `CSRF_COOKIE_DOMAIN` sunt comentate sau setate la `None` în settings.py.
2. Setează temporar `DEBUG = True` pentru a vedea mai multe informații despre erori.
3. Dezactivează temporar setările de securitate stricte:
   ```python
   SESSION_COOKIE_SECURE = False
   CSRF_COOKIE_SECURE = False
   ```
4. Asigură-te că Nginx transmite corect headerele pentru cookie-uri.
5. Verifică jurnalele pentru erori.

## Contribuții

Contribuțiile sunt binevenite! Te rugăm să creezi un pull request cu modificările tale.

## Licență

MIT
