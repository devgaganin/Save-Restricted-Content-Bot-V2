FROM python:3.9-slim

RUN apt update && apt upgrade -y

# Install necessary packages
RUN apt-get install git curl python3-pip ffmpeg -y
RUN apt-get -y install git  # Redundant, can be removed
RUN apt-get install -y wget python3-pip curl bash neofetch ffmpeg software-properties-common

# Set the working directory
WORKDIR /app 

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Copy the start script into the container
COPY start.sh .

# Make the start script executable
RUN chmod +x start.sh

# Expose the port on which your app will run
EXPOSE 8000

# Define the entry point to run the start script
CMD ["./start.sh"]
