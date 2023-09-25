# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the maintainer label
LABEL maintainer="example@example.com"

# Set the working directory inside the container
WORKDIR /main

# Copy the current directory contents into the container at /app
COPY . /main

# Install required packages
RUN pip install --no-cache-dir fuzzywuzzy SpeechRecognition

# Command to run the script (assuming your script name is 'app.py')
CMD ["python", "main.py"]
