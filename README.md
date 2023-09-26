# Djocs

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/vinimpv/djocs)

Built with:

- [OpenAI](https://openai.com/)
- [Django](https://www.djangoproject.com/)
- [pgvector](https://github.com/pgvector/pgvector)
- [htmx](https://htmx.org/)
- [Flowbite](https://flowbite.com/)
- [Tailwind](https://tailwindcss.com/)

And many other great open-source libraries, check the [pyproject.toml](pyproject.toml) file for more info.

## Running locally

```
git clone git@github.com:vinimpv/djocs.git
cd djocs
docker-compose up
```

Copy the .env.example file to .env and replace the OPENAI_API_KEY with the correct key
```
cp .env.example .env
```

Create the superuser to access the admin panel
```
docker-compose exec app python manage.py createsuperuser
```

Login to the admin page at http://localhost:8000/admin

Go to the [chat history page](http://localhost:8000/)
