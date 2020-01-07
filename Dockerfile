FROM continuumio/miniconda:latest

ARG BASE_DIR="/code/"
ARG USE_ENV="dev"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV ${USE_ENV}
ENV DOCKER_CONTAINER 1

COPY ./environment.yml ${BASE_DIR}/environment.yml
RUN conda install python=3.7
RUN conda env update -n base --file ${BASE_DIR}/environment.yml
RUN conda env list
RUN conda list

COPY ./requirements.txt ${BASE_DIR}/requirements.txt
RUN pip install -r ${BASE_DIR}/requirements.txt

COPY . ${BASE_DIR}/

WORKDIR ${BASE_DIR}/frontend/
RUN npm install
RUN npm run-script build

WORKDIR ${BASE_DIR}/backend/

EXPOSE 8000