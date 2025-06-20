# Dockerfile

# Use a specific Python base image for stability and smaller size
FROM python:3.11-slim-buster

# Set environment variables for non-interactive commands
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements.txt first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your Django project
COPY . /app


RUN python manage.py collectstatic --noinput

# Expose the port your Gunicorn server will listen on
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "parking.wsgi:application"]