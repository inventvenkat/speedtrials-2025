# Start with an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt && pip install bcrypt==3.2.2

# Copy the application's code into the container at /app
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run the main script when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
