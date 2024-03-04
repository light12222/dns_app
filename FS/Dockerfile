FROM python:3.5-slim

# Set the working directory
WORKDIR /app

# Copy application files to the working directory
COPY . .

# Install Flask library
RUN pip install Flask

# Expose port
EXPOSE 9090

# Start the application
CMD ["python", "run.py"]