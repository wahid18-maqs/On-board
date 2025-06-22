# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Copy environment file
COPY .env .env

# Run migrations
RUN python manage.py migrate

# Collect static files using current settings.py
RUN python manage.py collectstatic --noinput

# Expose the port that Django will run on
EXPOSE 8000

# Run with gunicorn using the current wsgi setup
CMD ["gunicorn", "jobs.wsgi:application", "--bind", "0.0.0.0:8000"]