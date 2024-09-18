# Base image with Python 3.11
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

ARG CPLUS_INCLUDE_PATH=/usr/include/gdal
ARG C_INCLUDE_PATH=/usr/include/gdal

# Set the work directory
WORKDIR /app

# Copy the requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire Django project to the container
COPY . /app/

# Set environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=transport_management.settings

# Expose port 8000 for Django development server
EXPOSE 8000

# Command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]