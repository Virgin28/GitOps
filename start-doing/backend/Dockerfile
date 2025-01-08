FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5001

# Use Gunicorn to serve the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]
