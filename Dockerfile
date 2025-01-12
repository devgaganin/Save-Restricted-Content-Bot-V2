FROM python:3.10.4-slim-buster
RUN apt update && apt upgrade -y
RUN apt-get install git curl python3-pip ffmpeg -y
RUN apt-get -y install git
RUN apt-get install -y wget python3-pip curl bash neofetch ffmpeg software-properties-common
COPY requirements.txt .

RUN pip3 install wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt
WORKDIR /app
COPY . .
EXPOSE 5000

CMD flask run -h 0.0.0.0 -p 5000 & python3 -m devgagan