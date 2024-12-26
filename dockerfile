# Use Python 3.12 as the base image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies
RUN pip install flask requests

# Expose the port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]
