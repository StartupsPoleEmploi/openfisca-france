FROM python:3.8.5-buster

ARG USER_NAME=openfisca
ARG USER_HOME_DIR="/home/${USER_NAME}"

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    wget \
    && apt-get -y autoremove && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN pip install openfisca-france \
    && pip install openfisca-core[web-api]

COPY gunicorn.conf.py .
COPY start.sh .
RUN chmod +x start.sh

ENTRYPOINT ./start.sh