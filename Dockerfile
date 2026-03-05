FROM python:3.11-slim

# Install pygame
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
    libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev \
    && pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Run the game + streaming server
CMD ["python", "web_stream.py"]