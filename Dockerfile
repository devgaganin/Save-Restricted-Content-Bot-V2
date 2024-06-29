FROM python:3.10.4-slim-buster

# Update the package lists and upgrade the existing packages
RUN apt update && apt upgrade -y

# Install necessary packages
RUN apt-get install git curl python3-pip ffmpeg -y
RUN apt-get -y install git  # Redundant, can be removed
RUN apt-get install -y wget python3-pip curl bash neofetch ffmpeg software-properties-common

# Copy the requirements file into the image
COPY requirements.txt .

# Install Python packages specified in requirements.txt
RUN pip3 install wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Set the working directory inside the container
WORKDIR /app

# Copy the entire application code into the image
COPY . .

# change port -p to 10000 if not works

# A dummy command to keep the container running
CMD flask run -h 0.0.0.0 -p 8000 & python3 -m ggn
