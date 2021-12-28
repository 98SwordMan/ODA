import os
from shutil import copyfile
import argparse


def partition_dataset(source, dest, val_ratio, test_ratio, copy_xml):
    if copy_xml:
        os.system(f'python partition_dataset.py -x -i {source} -o {dest} -vr {val_ratio} -tr {test_ratio}')
    else:
        os.system(f'python partition_dataset.py -i {source} -o {dest} -vr {val_ratio} -tr {test_ratio}')

def generate_label_map():
    os.system('python generate_label_map.py')

def generate_tfrecord():
    os.system('python generate_tfrecord.py -x images/train -l annotations/label_map.pbtxt -o annotations/train.record')
    os.system('python generate_tfrecord.py -x images/val -l annotations/label_map.pbtxt -o annotations/val.record')

def training_model(model_name):
    os.system(f'python model_main_tf2.py --model_dir=models/{model_name} --pipeline_config_path=models/{model_name}/pipeline.config')

def evaluating_model(model_name):
    os.system(f'python model_main_tf2.py --model_dir=models/{model_name} --pipeline_config_path=models/{model_name}/pipeline.config --checkpoint_dir=models/{model_name}')

def exporting_model(model_name):
    os.system(f'python exporter_main_v2.py --input_type image_tensor --pipeline_config_path models/{model_name}/pipeline.config --trained_checkpoint_dir models/{model_name}/ --output_directory exported-models/{model_name}')

def test_images(model_name):
    os.system(f'python test_images.py --model_name={model_name}')

def main():
    # Initiate argument parser
    parser = argparse.ArgumentParser(description="This is the startup file of scripts",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--imageDir',
        help='Path to the folder where the image dataset is stored. If not specified, the CWD will be used.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-o', '--outputDir',
        help='Path to the output folder where the train and test dirs should be created. '
             'Defaults to the same directory as IMAGEDIR.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-vr', '--valRatio',
        help='The ratio of the number of val images over the total number of images. The default is 0.1.',
        default=0.1,
        type=float)
    parser.add_argument(
        '-tr', '--testRatio',
        help='The ratio of the number of test images over the total number of images. The default is 0.0.',
        default=0.0,
        type=float)
    parser.add_argument(
        '-x', '--xml',
        help='Set this flag if you want the xml annotation files to be processed and copied over.',
        action='store_true'
    )
    parser.add_argument(
        '-gl', '--generateLabelmap',
        help='Create label_map.pbtxt',
        type=str,
        default=None
    )
    parser.add_argument(
        '-gt', '--generateTFRecord',
        help='Convert all files in the specified folder to TFRecord files.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-t', '--trainingModel',
        help='Training model.'
             'The parameter is the name of the model.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-e', '--evaluatingModel',
        help='Evaluating model.'
             'The parameter is the name of the model.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-ex', '--exportingModel',
        help='Exporting model.'
             'The parameter is the name of the model.',
        type=str,
        default=None
    )
    parser.add_argument(
        '-ts', '--testImages',
        help='Testing images.'
             'The parameter is the name of the model.',
        type=str,
        default=None
    )
    args = parser.parse_args()
    # Now we are ready to start the script
    if args.imageDir:
        if args.outputDir is None: args.outputDir = args.imageDir
        partition_dataset(args.imageDir, args.outputDir, args.valRatio, args.testRatio, args.xml)

    if args.generateLabelmap: generate_label_map()

    if args.generateTFRecord: generate_tfrecord()

    if args.trainingModel: training_model(args.trainingModel)

    if args.evaluatingModel: evaluating_model(args.evaluatingModel)

    if args.exportingModel: exporting_model(args.exportingModel)

    if args.testImages: test_images(args.testImages)


if __name__ == '__main__':
    main()
