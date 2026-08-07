# Use official lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your actual code into the container
COPY . .

# When the container starts, run the Telegram bot
CMD ["python", "main.py", "--worker"]
