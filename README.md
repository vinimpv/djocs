# Djocs
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/vinimpv/djocs)

A simple ChatGPT clone with knowledge embeddings.

Built with:

- [OpenAI](https://openai.com/)
- [Django](https://www.djangoproject.com/)
- [htmx](https://htmx.org/)
- [pgvector](https://github.com/pgvector/pgvector)
- [Flowbite](https://flowbite.com/)

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
