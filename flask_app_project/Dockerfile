FROM python:3.9-slim-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Flask application code and HTML templates
# Ensure these files are directly in your flask_app_project directory
COPY app.py .
COPY templates/ templates/


# Expose the port Flask runs on
EXPOSE 5000

# Set environment variables (will be populated by Fly.io secrets)
ENV MONGO_URI=""
ENV DATABASE_NAME=""
ENV COLLECTION_NAME=""
ENV FLASK_SECRET_KEY=""

# Command to run your Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]