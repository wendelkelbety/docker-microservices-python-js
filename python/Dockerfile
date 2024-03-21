FROM python:3.11.2-slim
LABEL maintaner="rasistemas.rasistemas@gmail.com"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

# install postgres dependencies inside of Docker
RUN apt-get update \
    && apt-get -y install libpq-dev gcc 
# unixODBC
RUN apt-get -y install odbc-postgresql unixodbc

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]