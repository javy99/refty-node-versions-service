# Base image
FROM python:3.10-slim

# Install system dependencies (including git)
RUN apt-get update && apt-get install -y git && apt-get clean

# Set work directory
WORKDIR /app

# Copy all source code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 80

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
