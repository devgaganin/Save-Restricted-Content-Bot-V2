FROM python:3.9-slim

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
