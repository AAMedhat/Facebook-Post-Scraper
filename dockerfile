# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /home
WORKDIR /home

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    chromium \
    unzip  

# Download and install Google Chrome dependencies
RUN apt-get update \
    && apt-get install -y libcurl3-gnutls libcurl3-nss libcurl4

# Download and install Google Chrome
RUN wget -O google-chrome.deb https://www.slimjet.com/chrome/download-chrome.php?file=files%2F103.0.5060.53%2Fgoogle-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome.deb \
    && rm google-chrome.deb




# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download and install ChromeDriver
RUN wget -O chromedriver.zip https://chromedriver.storage.googleapis.com/103.0.5060.53/chromedriver_linux64.zip \
    && unzip chromedriver.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && rm chromedriver.zip

# Copy the current directory contents into the container at /home
COPY . /home

# Keep container running
CMD ["tail", "-f", "/dev/null"]
