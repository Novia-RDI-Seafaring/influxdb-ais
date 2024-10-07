FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install poppler-utils -y
RUN apt-get install tesseract-ocr -y

## install conda
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 
RUN conda init

# activate base env
RUN echo ". /root/minicondsa3/etc/profile.d/conda.sh" >> ~/.bashrc
RUN . /root/miniconda3/etc/profile.d/conda.sh && conda activate base

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any additional packages specified in requirements.txt
# (if they're not already installed in the dev image)
RUN pip install --no-cache-dir -r requirements.txt

# Run client.py when the container launches
CMD ["bash", "-c", "source activate base && python client.py"]