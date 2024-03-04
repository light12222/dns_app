FROM python:3.6

# Set the working directory
WORKDIR /app

# Copy application files to the working directory
COPY . .

# Install Flask library
RUN pip install Flask

# Expose port
EXPOSE 53533/udp

# Start the application
CMD ["python", "run.py"]