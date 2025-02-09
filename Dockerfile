# Use official Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot script to the container
COPY bot.py bot.py

# Set environment variables (optional, recommended to use a .env file)
ENV BOT_TOKEN="7482868409:AAEnZDq8GddbtQmXIPMD-K7Swkv3aNxj3DY"

# Run the bot
CMD ["python", "bot.py"]
