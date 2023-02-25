FROM python:3.8-slim-bullseye

RUN apt-get update && apt-get upgrade -y
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential

RUN pip install pipenv


COPY ./Pipfile /opt
COPY ./Pipfile.lock /opt
WORKDIR /opt

RUN pipenv install --system --deploy

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



