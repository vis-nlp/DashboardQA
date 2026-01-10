gcloud compute instances create vm-machine-gpu \
  --enable-nested-virtualization \
  --zone=us-central1-a \
  --machine-type=g2-standard-4 \
  --accelerator=type=nvidia-l4,count=1 \
  --boot-disk-size=200GB \
  --boot-disk-type=pd-standard \
  --image-family=common-cu124-ubuntu-2204-py310 \
  --image-project=deeplearning-platform-release \
  --maintenance-policy=TERMINATE \
  --restart-on-failure


# gcloud compute instances create vm-machine-a100 \
#   --enable-nested-virtualization \
#   --zone=us-central1-a \
#   --machine-type=a2-highgpu-1g \
#   --boot-disk-size=200GB \
#   --boot-disk-type=pd-standard \
#   --image-family=common-cu124-ubuntu-2204-py310 \
#   --image-project=deeplearning-platform-release \
#   --maintenance-policy=TERMINATE \
#   --restart-on-failure
