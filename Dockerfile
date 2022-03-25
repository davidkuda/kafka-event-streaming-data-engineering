ARG PYTHON_IMAGE_TAG=4.8.2

FROM continuumio/miniconda3:${PYTHON_IMAGE_TAG}

LABEL maintainer="David Kuda"

WORKDIR /log_queue_api
COPY . .

RUN conda config --set channel_priority strict && \
    conda env create -n log_queue_api_env -f environment.yml

# Make RUN commands use the new environment (see: https://pythonspeed.com/articles/activate-conda-dockerfile/)
SHELL ["conda", "run", "-n", "log_queue_api_env", "/bin/bash", "-c"]

RUN python setup.py install

# ENTRYPOINT doesn't use the same shell as RUN so you need the conda stuff
ENTRYPOINT ["conda", "run", "-n", "log_queue_api_env", "python", "-OO", "-m", "log_queue_api"]
