FROM python:3.6-alpine

ARG container_version=0.1

RUN apk add --no-cache \
        make \
        bash \
        g++ \
        vim \
        tzdata

ENV TZ=Asia/Novosibirsk
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY requirements.txt /app/requirements.test.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt -r/app/requirements.test.txt

ENV PYTHONPATH /app
ENV TERM=xterm-256color
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONENCODING=utf-8

COPY . /app

CMD ["python3", "--version"]

EXPOSE 8000
ENTRYPOINT ["/app/docker-entrypoint.sh"]
