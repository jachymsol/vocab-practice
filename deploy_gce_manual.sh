VERSION=grep 'app_version' anvil.yaml | cut -d ' ' -f 2

docker build -t us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION .
docker push us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION

gcloud compute instances create-with-container vocab-practice-app \
    --project=jachymsol-vocabulary-practice \
    --zone=us-central1-f \
    --machine-type=e2-micro \
    --network-interface=address=35.208.81.151,network-tier=STANDARD,stack-type=IPV4_ONLY,subnet=default \
    --maintenance-policy=MIGRATE \
    --provisioning-model=STANDARD \
    --service-account=184798976963-compute@developer.gserviceaccount.com \
    --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/trace.append \
    --tags=http-server,https-server \
    --image=projects/cos-cloud/global/images/cos-stable-113-18244-85-24 \
    --boot-disk-size=10GB \
    --boot-disk-type=pd-standard \
    --boot-disk-device-name=vocab-practice-app \
    --disk=boot=no,device-name=vocab-db,mode=rw,name=vocab-db \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud,container-vm=cos-stable-113-18244-85-24 \
    --metadata=startup-script='#! /bin/bash
  sudo apt-get update && sudo apt-get install -y docker.io
  sudo mkdir -p /mnt/disks/anvil-db
  sudo chmod 777 /mnt/disks/anvil-db
  sudo ls -l /dev/disk/by-id | grep -o 'google-vocab-db -> ../../sd[a-z]' | tail -c 4 | xargs -I {} sudo mount /dev/{} /mnt/disks/anvil-db
  sudo docker pull us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION
  sudo docker run -d --name vocab-practice-app -v /mnt/disks/anvil-db/:/anvil-db/ -p 443:443 us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION --app MainApp --origin https://vocab.solecky.com --data-dir /anvil-db --letsencrypt-storage /anvil-db/certs.json
  EOF'