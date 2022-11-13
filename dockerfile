FROM python:alpine
COPY . /tmp/
WORKDIR /tmp
RUN chmod +x /tmp
RUN pip install --upgrade pip
RUN pip install pyjwt cryptography requests datadog_api_client
ENTRYPOINT ["/tmp/script.sh"]
