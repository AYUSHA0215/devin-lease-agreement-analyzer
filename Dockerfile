# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install pkg-config, libcairo2-dev, gcc, libgirepository1.0-dev, libdbus-1-dev, and other necessary packages
RUN apt-get update && apt-get install -y pkg-config libcairo2-dev gcc libgirepository1.0-dev libdbus-1-dev

# Install PyTorch
RUN pip install torch

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Download the NLTK 'punkt' resource
RUN python -m nltk.downloader punkt

# Set the NLTK data path environment variable
ENV NLTK_DATA /usr/local/share/nltk_data

# Set the OpenAI API key environment variable


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP backend.py
ENV FLASK_RUN_HOST 0.0.0.0

# Run backend.py when the container launches
CMD ["flask", "run"]
