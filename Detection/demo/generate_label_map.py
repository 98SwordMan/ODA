import glob
import os
from absl import app
from absl import flags
from lxml import etree

FLAGS = flags.FLAGS
flags.DEFINE_string('xml_files', 'glob.glob(r"images/train/*.xml")', '*.xml file path')
flags.DEFINE_string('save_dir', 'annotations', 'save directory')


def convert_classes(classes, start=1):
    msg = ''
    for id, name in enumerate(classes, start=start):
        msg = msg + "item {\n"
        msg = msg + "  id: " + str(id) + "\n"
        msg = msg + "  name: '" + name + "'\n}\n\n"
    return msg[:-1]


def main(argv):
    del argv  # Unused.

    classes = []
    for xml_path in eval(FLAGS.xml_files):
        with open(xml_path, 'r') as f:
            xml_data = f.read()
        xml_data = etree.HTML(xml_data)
        name = xml_data.xpath("//name/text()")
        classes.extend(name)
    classes = set(classes)

    txt = convert_classes(classes)

    save_path = os.path.join(FLAGS.save_dir, 'label_map.pbtxt')
    with open(save_path, 'w') as f:
        f.write(txt)


if __name__ == '__main__':
    app.run(main)