FROM python:3.9-slim

WORKDIR /app

# Copy only the necessary files
COPY app.py requirements.txt ./
COPY templates ./templates/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

# Use Gunicorn to serve the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "app:app"]