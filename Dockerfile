FROM registry.radiobretzel.org/hosting/dockerfile-store/python:flask

WORKDIR /usr/src/rb-core

COPY . .

RUN pip install /usr/src/rb-core

VOLUME /usr/src/rb-core /var/run/docker.sock
EXPOSE 5000

CMD ["python", "-m", "rbcore"]
