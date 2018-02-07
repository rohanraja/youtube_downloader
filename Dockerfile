FROM python:3.5-alpine

RUN apk add --no-cache redis
RUN apk add --no-cache supervisor

ENV INSTALL_PATH /root/code/youtube_downloader


RUN mkdir -p $INSTALL_PATH

RUN mkdir -p $HOME/log/youDL
WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY . .

ENV YOUDL_PATH /youdl
ENV YOUDL_REDIS algomuse.com

CMD supervisord -n -c supervisor_conf/supervisord.conf
