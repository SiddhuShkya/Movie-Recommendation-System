# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements_app.txt .

# Install any needed packages specified in requirements_app.txt
RUN pip install --no-cache-dir -r requirements_app.txt

# Copy the necessary project files into the container at /app
COPY app.py .
COPY src/ src/
COPY config/ config/
COPY templates/ templates/
COPY artifacts/ artifacts/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["python", "app.py"]
