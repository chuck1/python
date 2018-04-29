import os
import sys
import lxml.etree as ET

dst_folder = "/media/sf_J_DRIVE/Engineering/_DESIGN/Thermal Design/Charles Rymal/Data/circuiting/CoilWC/"

def main():
    
    with open(sys.argv[1]) as f:
        raw = f.read()
    
    lines = raw.split("\n")
    
    root = ET.Element("CoilWater")
    
    ET.SubElement(root, "_M_rows").text = lines.pop(0)
    ET.SubElement(root, "_M_passes").text = lines.pop(0)
    ET.SubElement(root, "_M_columns").text = lines.pop(0)
    ET.SubElement(root, "_M_tubes_remainder").text = "0"
    ET.SubElement(root, "_M_optionTubePosition").text = "0"
    
    
    patches = ET.SubElement(root, "_patches")
    
    patch = ET.SubElement(patches, "Patch")
    patch.set(ET.QName("xsi", "type"), "PatchCWCore")
    
    feeds = ET.SubElement(patch, "_M_feed")
    
    while True:
        line0 = lines.pop(0)
        if not line0: break
        line1 = lines.pop(0)
        print(line0)
        print(line1)
    
        X = [int(x) for x in line0.split(",")]
        Y = [int(y) for y in line1.split(",")]
    
        feed = ET.SubElement(feeds, "Feed")
        coordinates = ET.SubElement(feed, "c")
        
        for x, y in zip(X, Y):
            coor = ET.SubElement(coordinates, "Coor")
            ET.SubElement(coor, "x").text = str(x)
            ET.SubElement(coor, "y").text = str(y)
    
    ET.dump(root)
    
    tree = ET.ElementTree(root)

    dst = os.path.join(dst_folder, sys.argv[1])

    if os.path.exists(dst):
        print('file {} already exists'.format(dst))
    
    tree.write(dst)
     
main()

