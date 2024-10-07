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