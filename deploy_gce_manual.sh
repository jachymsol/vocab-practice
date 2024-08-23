#!/bin/bash
set -e

VERSION=$(grep 'app_version' anvil.yaml | cut -d ' ' -f 2)

docker build -t us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION .
docker push us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION

GCLOUD_REGION=us-central1
GCLOUD_ZONE=us-central1-a

gcloud compute addresses create vocab-practice-ip \
  --region $GCLOUD_REGION

IP_ADDRESS=$(gcloud compute addresses describe vocab-practice-ip | grep address: | cut -d ' ' -f 2) 

gcloud compute disks create vocab-db \
  --size 10 \
  --type https://www.googleapis.com/compute/v1/projects/jachymsol-vocabulary-practice/zones/$GCLOUD_ZONE/diskTypes/pd-standard
  --zone $GCLOUD_ZONE

gcloud compute instances create vocab-practice-app \
    --project=jachymsol-vocabulary-practice \
    --zone=$GCLOUD_ZONE \
    --machine-type=e2-micro \
    --network-interface=address=$IP_ADDRESS,network-tier=STANDARD,stack-type=IPV4_ONLY,subnet=default \
    --public-ptr \
    --public-ptr-domain=vocab.solecky.com \
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
    --labels=goog-ec-src=vm_add-gcloud \
    --metadata=startup-script="apt-get update && apt-get install -y docker.io
usermod -aG docker solejabreck

mkdir -p /mnt/disks/anvil-db && chmod 777 /mnt/disks/anvil-db

ls -l /dev/disk/by-id | grep -o 'google-vocab-db -> ../../sd[a-z]' | tail -c 4 | xargs -I {} mount /dev/{} /mnt/disks/anvil-db

gcloud auth configure-docker us-central1-docker.pkg.dev --quiet
docker pull us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION
docker run -d --name vocab-practice-app -v /mnt/disks/anvil-db/:/anvil-db/ -p 443:443 us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION --app MainApp --origin https://vocab.solecky.com --data-dir /anvil-db --letsencrypt-storage /anvil-db/certs.json
EOF"
