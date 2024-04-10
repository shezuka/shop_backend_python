FROM debian:12.5

RUN apt update
RUN apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget pkg-config

WORKDIR /tmp
RUN wget https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz
RUN tar -xf Python-3.12.3.tgz
WORKDIR /tmp/Python-3.12.3
RUN ./configure --enable-optimizations
RUN make install
WORKDIR /tmp
RUN rm -rf Python-3.12.3 Python-3.12.3.tgz
RUN ln -s /usr/local/bin/python3 /usr/local/bin/python

RUN apt install -y curl
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -

ENV POETRY_HOME=/etc/poetry
ENV PATH $PATH:$POETRY_HOME/bin

WORKDIR /backend_python
COPY . .
RUN poetry install
CMD ["poetry", "run", "uvicorn", "backend_python:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]