FROM python:3.8.2-slim

RUN apt-get update \
    && apt-get install -y \
    dumb-init \
    --no-install-recommends \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
# copy and install requirements
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY ./server ./server
COPY run_server.py .
COPY server_entry_point.sh .

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
RUN ["chmod", "+x", "/usr/src/app/server_entry_point.sh"]
CMD ["/usr/src/app/server_entry_point.sh"]

