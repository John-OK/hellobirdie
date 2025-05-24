FROM python:3.13.1-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=development

# Set work directory
WORKDIR /app

# Install system dependencies including PostgreSQL client libraries
RUN apt-get update && apt-get install -y \
  gcc \
  postgresql-client \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/docker.txt

# Copy project
COPY . /app/

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hellobirdie.wsgi:application"]
