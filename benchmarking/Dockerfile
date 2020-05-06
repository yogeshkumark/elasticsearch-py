# $ docker build --file benchmarks/Dockerfile --tag elastic/elasticsearch-py .

ARG  PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}

ENV TERM xterm-256color
VOLUME ["/data"]

WORKDIR /elasticsearch-py

COPY . .

RUN python setup.py install && \
    python -m pip install -r benchmarking/requirements.txt

CMD ["/bin/bash"]
