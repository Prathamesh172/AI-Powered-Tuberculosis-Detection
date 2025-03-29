# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables to prevent Python from writing bytecode and buffering
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose the correct port for Hugging Face Spaces
EXPOSE 7860

# Command to run the app using gunicorn for better performance
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:7860", "app:app"]