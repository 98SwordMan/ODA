import os
# install api
if not os.path.exists('./models'):
    os.system('git clone https://github.91chi.fun//https://github.com/tensorflow/models.git')
os.system('cd models/research/')
os.system('protoc object_detection/protos/*.proto --python_out=.')
os.system('cp object_detection/packages/tf2/setup.py .')
os.system('python -m pip install . -i https://pypi.doubanio.com/simple/')
# test api
os.system('python object_detection/builders/model_builder_tf2_test.py')