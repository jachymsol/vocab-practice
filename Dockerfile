FROM --platform=linux/amd64 python:3-buster

RUN apt-get -yyy update && apt-get -yyy install software-properties-common && \
    wget -O- https://apt.corretto.aws/corretto.key | apt-key add - && \
    add-apt-repository 'deb https://apt.corretto.aws stable main'

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    (dpkg -i google-chrome-stable_current_amd64.deb || apt install -y --fix-broken) && \
    rm google-chrome-stable_current_amd64.deb 

RUN apt-get -yyy update && apt-get -yyy install java-1.8.0-amazon-corretto-jdk ghostscript

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN anvil-app-server || true

RUN mkdir /apps
WORKDIR /apps

RUN mkdir /anvil-data

RUN useradd anvil
RUN chown -R anvil:anvil /anvil-data
USER anvil

COPY server_code /apps/MainApp/server_code
COPY client_code /apps/MainApp/client_code
COPY theme /apps/MainApp/theme
COPY __init__.py /apps/MainApp/__init__.py
COPY --chown=anvil:anvil anvil.yaml /apps/MainApp/anvil.yaml
COPY Makefile /apps/Makefile

ENTRYPOINT ["make"]

CMD ["run-default"]