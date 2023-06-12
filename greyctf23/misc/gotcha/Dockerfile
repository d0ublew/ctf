FROM ubuntu:20.04

# Add Env Args for tzdata package
ARG DEBIAN_FRONTEND=noninteractive

# Install python

RUN echo "deb http://archive.ubuntu.com/ubuntu focal universe" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y tzdata python3-pip python3 wget tesseract-ocr
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

# Copy files
COPY requirements.txt .

# Install requirements
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "./solve.py"]
