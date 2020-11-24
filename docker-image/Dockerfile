FROM python:3.8.5-buster

#installation OpenFisca France
RUN pip install openfisca-france \
    && pip install openfisca-core[web-api]

COPY ./gunicorn-config/gunicorn.conf.py .

COPY ./scripts/startup.sh .
RUN chmod +x startup.sh

ENTRYPOINT ./startup.sh