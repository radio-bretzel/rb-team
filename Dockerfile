FROM registry.radiobretzel.org/hosting/dockerfile-store/python:flask

WORKDIR /usr/src/rb-core

COPY . .

RUN pip install .

VOLUME /usr/src/rb-core /var/run/docker.sock
EXPOSE 5000

ENV RBCORE_IS_CONTAINER True
CMD ["python", "-m", "rbcore"]
