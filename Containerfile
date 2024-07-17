# Use the official Python image from the Docker Hub
FROM --platform=linux/$ARM registry.access.redhat.com/ubi9/python-311
#FROM registry.access.redhat.com/ubi9/python-312

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask
RUN pip install Flask requests

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
