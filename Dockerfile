# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install required dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Run migrations and collect static files
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Django
# ENV DJANGO_ENV=dev

# Run the Django development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

