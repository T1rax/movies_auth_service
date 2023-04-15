FROM --platform=linux/amd64 python:3.11-buster

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/opt/app"
ENV PYTHONPATH "${PYTHONPATH}:/opt/app/flask_app"
ENV PYTHONPATH "${PYTHONPATH}:/opt/app/tests/functional"
ENV PYTHONPATH "${PYTHONPATH}:/opt/appflask_app/tests/functional"


COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

RUN chmod +x run.sh

ENTRYPOINT ["/opt/app/run.sh"]