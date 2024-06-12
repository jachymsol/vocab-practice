install:
	python -m pip install virtualenv
	python -m virualenv venv
	source venv/bin/activate && python -m pip install -e .

test: 
	python -m pytest

deploy:
	bash deploy_gce_manual.sh

run-default:
	anvil-app-server --app MainApp --data-dir /anvil-data

run:
	anvil-app-server --app ${APP_NAME} --origin ${ORIGIN} --data-dir ${DATA_DIR}

run-https:
	anvil-app-server --app ${APP_NAME} --origin ${ORIGIN} --data-dir ${DATA_DIR} --http-redirect-port 80 --letsencrypt-storage ${LETSENCRYPT_STORAGE}

run-https-with-email:
	cp /apps/${APP_NAME}/anvil.yaml ${DATA_DIR}/anvil-template.yaml
	sed 's/ENV.EMAIL_FROM_ADDRESS/${EMAIL_FROM_ADDRESS}/g' ${DATA_DIR}/anvil-template.yaml > /apps/${APP_NAME}/anvil.yaml
	anvil-app-server --app ${APP_NAME} --origin ${ORIGIN} --data-dir ${DATA_DIR} --http-redirect-port 80 --letsencrypt-storage ${LETSENCRYPT_STORAGE} --smtp-host ${SMTP_HOST} --smtp-port ${SMTP_PORT} --smtp-encryption ${SMTP_ENCRYPTION} --smtp-username ${SMTP_USERNAME} --smtp-password ${SMTP_PASSWORD}

docker-run:
	docker run -v $(pwd):/apps/Vocabulary_Practice -p 3030:3030 anvilworks/anvil-app-server --app Vocabulary_Practice
