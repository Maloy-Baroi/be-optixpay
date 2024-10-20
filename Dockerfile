# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . /app/

# Ensure the secret keys are not overwritten
RUN mkdir -p /app/static /app/media

# Copy over static and media assets
RUN python manage.py collectstatic --noinput

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the application with gunicorn for production usage
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "optixpay_backend.wsgi:application"]
