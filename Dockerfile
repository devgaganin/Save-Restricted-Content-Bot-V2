# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Create a directory for the application and set permissions
RUN mkdir /app && chmod 777 /app

# Set the working directory in the container
WORKDIR /app

# Install necessary packages
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    ffmpeg

# Copy your application code into the container
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Command to run your application (assuming bash.sh is your entry point)
CMD ["bash", "bash.sh"]
