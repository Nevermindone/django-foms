

#FROM --platform=linux/amd64 python:3.10-slim-bullseye

FROM ubuntu:20.04
ENV PATH /usr/local/bin:$PATH
RUN apt-get update && apt-get install -y locales

# Locale
RUN sed -i -e \
  's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
   && locale-gen

ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU:ru
ENV LC_LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN apt-get  update && apt-get install -y software-properties-common \
&& add-apt-repository ppa:deadsnakes/ppa && apt install -y python3.10 \
&& apt-get install -y  \
    python3-pip  \
    libpq-dev  \
    python-dev

RUN apt-get update && apt-get install -y p7zip-rar
RUN apt-get update \
    && apt-get install -y \
       --no-install-recommends \
       --no-install-suggests \
        p7zip-rar unrar \
    && apt-get clean
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/

#RUN ["python", "manage.py", "collectstatic", "--noinput"]