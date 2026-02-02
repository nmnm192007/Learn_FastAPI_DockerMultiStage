
# Base Image
FROM python:3.11-slim

# Set Working Directory
WORKDIR /app

# Copy Dependency File first
COPY ../requirements.txt .

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Application Code
COPY app/ app/

# Expose Application Port
EXPOSE 8000

# Define Startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
