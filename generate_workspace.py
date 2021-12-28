import os
from absl import app
from absl import flags
from shutil import copyfile

FLAGS = flags.FLAGS
flags.DEFINE_string('save_dir', None, 'workspace save dir', required=True)
flags.DEFINE_string('name', None, 'workspace name', required=True)

Base = 'CommonScripts'
Contents = [
    'preprocessing',
    'models',
]

Dirs = [
    'annotations',
    'exported-models',
    'images',
    'images/test',
    'images/train',
    'images/val',
    'models',
    'pre-trained-models',
]


def main(argv):
    del argv  # Unused.
    dir = os.path.join(FLAGS.save_dir, FLAGS.name)
    if not os.path.exists(dir):
        os.makedirs(dir)
    for d in Dirs:
        p = os.path.join(dir, d)
        if not os.path.exists(p):
            os.makedirs(p)
    for c in Contents:
        d = os.path.join(Base, c)
        for file in os.listdir(d):
            copyfile(os.path.join(d, file),
                     os.path.join(dir, file))
    copyfile(os.path.join(Base, 'start.py'),
             os.path.join(dir, 'start.py'))


if __name__ == '__main__':
    app.run(main)
