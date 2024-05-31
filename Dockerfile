FROM anvilworks/anvil-app-server:latest

WORKDIR /
USER root

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /apps
USER anvil

COPY . /apps/MainApp

ENTRYPOINT [ "anvil-app-server", "--data-dir", "/anvil-data"]

CMD ["--app", "MainApp"]