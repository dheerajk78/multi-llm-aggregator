FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PYTHONPATH=/

# Create working directory
WORKDIR /

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Expose the port your app runs on
EXPOSE 8080

# Use Gunicorn to run the Flask app
# "app:app" means the Flask app is exposed as `app = create_app()` in app.py
CMD ["gunicorn", "-b", "0.0.0.0:8080", "backend.app:app"]
