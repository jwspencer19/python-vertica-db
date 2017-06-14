# Use an official Python runtime as a base image
FROM python:2.7-slim

# Set the working directory to /my_python_vertica
WORKDIR /my_python_vertica

# Copy the directory contents into the container at /verticadb
ADD . /my_python_vertica

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80




