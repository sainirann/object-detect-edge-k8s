docker build -t objectdetect --build-arg model_url=http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v1_coco_2017_11_17.tar.gz .


Server Side:

kubectl apply -f deployment.yaml



Client Side:

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

python -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))"


git clone https://github.com/tensorflow/models

cd models/research

python3 setup.py install

cd ../../


Run Client:

python3 object_detection_tutorial.py Bicycle.jpg