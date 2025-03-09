# Fitness Blog

## Description

This is a fitness blog built with Django. It provides articles on nutrition, training, and lifestyle.

## Installation

1.  Clone the repository:

```bash
git clone <repository_url>
```

2.  Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3.  Install dependencies:

```bash
pip install -r requirements.txt
```

4.  Configure the database:

*   Update the `DATABASES` setting in `fitness_blog/settings.py` with your database credentials.

5.  Run migrations:

```bash
python manage.py migrate
```

## Usage

1.  Run the development server:

```bash
python manage.py runserver
```

2.  Access the website in your browser at `http://localhost:8000`.

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

## License

MIT
