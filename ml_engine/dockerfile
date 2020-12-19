FROM nvidia/cuda:11.0-devel-ubuntu20.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip git
RUN pip3 install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

COPY ./ /work
WORKDIR /work

RUN pip3 install -r requirements.txt
CMD mlflow ui -h 0.0.0.0:5000