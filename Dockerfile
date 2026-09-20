# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask transformers torch textblob && \
    python -m textblob.download_corpora

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]