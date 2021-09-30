FROM ubuntu:18.04
ENTRYPOINT []
RUN apt-get update && && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==2.8.1
cd . /app/
CMD chmod +x /app/start_services.sh
RUN /app/start_services.sh