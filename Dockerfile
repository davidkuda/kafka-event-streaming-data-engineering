ARG PLATFORM=linux/arm64

FROM --platform=${PLATFORM} continuumio/miniconda3

LABEL maintainer="David Kuda"

WORKDIR /home/log_queue_api
COPY . .

RUN conda config --set channel_priority strict && \
    conda env create -n log_queue_api_env -f environment.yml

# Make RUN commands use the new environment (see: https://pythonspeed.com/articles/activate-conda-dockerfile/)
SHELL ["conda", "run", "-n", "log_queue_api_env", "/bin/bash", "-c"]

RUN python setup.py install
RUN echo "conda activate log_queue_api_env" >> ~/.bashrc
RUN echo alias app=\"python3 src/cli.py\" >> ~/.bashrc

ENTRYPOINT ["bash"]
