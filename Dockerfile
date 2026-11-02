FROM python:3.13-slim

# Git is required for the pinned upstream Nautilus dependency.
RUN apt-get update \
    && apt-get install --no-install-recommends -y git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --no-cache-dir pipenv \
    && pipenv verify \
    && pipenv sync --system

# Copy app files last for faster rebuilds.
COPY . /app

EXPOSE 80
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--timeout", "120", "main:app"]

