FROM python:3.11-slim

# Install pygame
RUN apt-get update && apt-get install -y \
    libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev \
    && pip install -r requirements.txt

# Copy and install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /app
COPY . /app

# Expose the port used by Flask streaming
EXPOSE 8080

# Run the game + streaming server
CMD ["python", "web_stream.py"]