# xml parsing utility
import xml.etree.cElementTree as ET
import pickle


def save_to_XML(instancesList, filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except:
       root = ET.Element("Players")
       
    aInstances = []
    for instance in instancesList:
        node = "".join(str(instance).split())
        for child in list(root):
            if child.tag == node:
                root.remove(child)
        aInstances.append((ET.SubElement(root, node), instance.__dict__))

    for elm, oDict in aInstances:
        for k, v in oDict.items():
            ET.SubElement(elm, k).text = str(v)

    tree = ET.ElementTree(root)
    tree.write(filename)
