# Docker consul notifier
# Temporary replacement for registrator that works
# with Docker services

FROM frolvlad/alpine-python2

USER root
RUN apk add --update \
  && pip install virtualenv docker-py python-consul

WORKDIR /app

COPY . /app

ENTRYPOINT ["python", "consul-notifier.py"]
CMD ["-v"]
