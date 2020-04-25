FROM python:3.7.4

RUN apt-get update && apt-get install -y wget protobuf-compiler

RUN pip install --upgrade pip

RUN pip install numpy requests six pillow matplotlib tensorflow==1.15 flask

RUN git clone https://github.com/tensorflow/models && cd models/research &&\
 protoc object_detection/protos/*.proto --python_out=. && python setup.py install && cd ../..

ADD . /server

WORKDIR /server

EXPOSE 9080

CMD [ "python", "HostServer.py"]
