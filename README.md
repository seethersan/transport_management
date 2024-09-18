# Mozio API Project

This project is a Django REST API for managing service providers and service areas, allowing you to query for service areas that cover a specific latitude and longitude. The project is designed to handle geo-spatial data using **PostGIS** and supports features such as rate limiting and API documentation with Swagger.

## Project Architecture

The project is organized into two main components:

1. **Providers**: Manages transportation providers, including basic details like name, email, phone number, language, and currency.
2. **Service Areas**: Handles service area management, including the ability to define areas as polygons (GeoJSON format) and query areas by latitude/longitude.

### Key Components:

- **Django Rest Framework (DRF)**: Provides the foundation for building the REST API.
- **PostGIS**: Extends PostgreSQL to handle geo-spatial data such as polygons.
- **Redis**: Used for caching to improve performance.
- **Swagger (drf-yasg)**: Provides auto-generated API documentation.

### API Endpoints:

- `/api/providers/`: CRUD operations for providers.
- `/api/serviceareas/`: CRUD operations for service areas.
- `/api/serviceareas/latlng/?lat=<lat>&lng=<lng>`: Find service areas that contain a specific latitude/longitude.
- `/swagger/`: View Swagger documentation.
- `/redoc/`: View ReDoc documentation.

## Features

- **Geo-Spatial Queries**: The project uses PostGIS for querying service areas based on geo-spatial data.
- **Rate Limiting**: API rate limiting is implemented using `django-ratelimit` or AWS API Gateway.
- **API Documentation**: Swagger and ReDoc are integrated for interactive API documentation.
- **PostgreSQL with PostGIS**: Database support for geo-spatial queries.

## Project Structure

- **providers**: Contains the logic for managing providers.
- **service_areas**: Contains the logic for managing service areas and performing geo-spatial queries.
- **api**: Defines the DRF-based API and custom views.
- **docker-compose.yml**: Docker configuration to run the project with PostgreSQL and Redis.
- **Dockerfile**: Docker image configuration for running Django with necessary dependencies.

## Prerequisites

Ensure you have the following installed:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Running the Project with Docker

### Step 1: Clone the Repository

```bash
git clone https://github.com/seethersan/transport_management.git
cd transport_managemen
```

### Step 2: Build and Run the Project with Docker
Use Docker Compose to build and run the project, including the Django app, PostgreSQL with PostGIS, and Redis for caching.

```bash
docker-compose up --build
```

This will:

- Build the Docker image for the Django app based on the Dockerfile.
- Start the PostgreSQL database with PostGIS extensions.
- Start Redis for caching.
- Run migrations and start the Django development server.

### Step 3: Access the Application

Once the containers are running, you can access the API and Swagger documentation:

- **API Base URL**: [http://localhost:8000/api/](http://localhost:8000/api/)
- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc UI**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

### Step 4: Running Migrations and Creating a Superuser

After running the containers, you can run migrations and create a superuser to access the Django admin interface:

**Run Migrations:**

```bash
docker-compose exec web python manage.py migrate
```

**Create a Superuser:**

```bash
docker-compose exec web python manage.py createsuperuser
```

**Access the Django Admin:**

- **Admin URL**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Login with the superuser credentials you created.

### Step 5: Running Tests

To run the test suite:

```bash
docker-compose exec web python manage.py test
```

This will run all the unit tests defined for the project.
