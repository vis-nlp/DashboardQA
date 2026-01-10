gcloud compute instances create vm-machine-3 \
  --enable-nested-virtualization \
  --zone=us-central1-f \
  --machine-type=n1-standard-4 \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-standard \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud