# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc libpq-dev sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better Docker caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Copy environment variables file
COPY .env .env

# Expose Django port
EXPOSE 8000

# Default command (runs migrations and collects static at runtime)
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn jobs.wsgi:application --bind 0.0.0.0:8000"]