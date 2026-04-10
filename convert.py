import os
import xml.etree.ElementTree as ET

# Paths
xml_dir = "annotations"
img_dir = "images"

output_img_dir = "dataset/images"
output_label_dir = "dataset/labels"

os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

classes = ["with_mask", "without_mask", "mask_weared_incorrect"]

def convert_bbox(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return x*dw, y*dh, w*dw, h*dh

for xml_file in os.listdir(xml_dir):
    tree = ET.parse(os.path.join(xml_dir, xml_file))
    root = tree.getroot()

    size = root.find("size")
    w = int(size.find("width").text)
    h = int(size.find("height").text)

    label_file = open(os.path.join(output_label_dir, xml_file.replace(".xml", ".txt")), "w")

    for obj in root.iter("object"):
        cls = obj.find("name").text

        if cls not in classes:
            continue

        cls_id = classes.index(cls)

        xmlbox = obj.find("bndbox")
        b = (
            float(xmlbox.find("xmin").text),
            float(xmlbox.find("xmax").text),
            float(xmlbox.find("ymin").text),
            float(xmlbox.find("ymax").text)
        )

        bb = convert_bbox((w, h), b)
        label_file.write(f"{cls_id} {' '.join(map(str, bb))}\n")

    label_file.close()

print("✅ Conversion Completed!")