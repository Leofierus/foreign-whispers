# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /foreign_whispers

# Copy the current directory contents into the container
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y rubberband-cli && apt-get install espeak -y && apt install ffmpeg -y
RUN pip install --upgrade pip setuptools
RUN apt-get install -y libblas-dev liblapack-dev libatlas-base-dev gfortran

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=foreign_whispers.settings

# Run Django development server when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
