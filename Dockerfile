FROM registry.radiobretzel.org/python/flask

WORKDIR /usr/src/rb-core

COPY . .

RUN pip install --upgrade pip && \
   pip install .

VOLUME /usr/src/rb-core /var/run/docker.sock
EXPOSE 5000

CMD ["python", "-m", "rbcore"]
