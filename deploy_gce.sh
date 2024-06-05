VERSION=0.0.8

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
    --container-image=us-central1-docker.pkg.dev/jachymsol-vocabulary-practice/jachymsol-docker/vocab-practice-app:$VERSION \
    --container-restart-policy=never \
    --container-command=anvil-server-app \
    --container-arg=--app \
    --container-arg=MainApp \
    --container-arg=--data-dir \
    --container-arg=/anvil-db \
    --container-arg=--letsencrypt-storage \
    --container-arg=/anvil-db/test/certs.json \
    --container-arg=--origin \
    --container-arg=https://vocab.solecky.com \
    --container-mount-disk=mode=rw,mount-path=/anvil-db,name=vocab-db,partition=0 \
    --disk=boot=no,device-name=vocab-db,mode=rw,name=vocab-db \
    --no-shielded-secure-boot \
    --shielded-vtpm \
    --shielded-integrity-monitoring \
    --labels=goog-ec-src=vm_add-gcloud,container-vm=cos-stable-113-18244-85-24 \
    --metadata=startup-script='#! /bin/bash
  echo 'net.ipv4.ip_unprivileged_port_start=0' > /etc/sysctl.d/50-unprivileged-ports.conf
  sysctl --system
  EOF'