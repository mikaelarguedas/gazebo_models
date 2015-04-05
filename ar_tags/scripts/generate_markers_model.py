#! /usr/bin/env python

import argparse
from xml.dom.minidom import parse, parseString
import os
import sys

parser = argparse.ArgumentParser(usage='convert offset of all dae files in a directory')
parser.add_argument('-i','--input', default="/media/Data1/mikatchou/Downloads/ARMarkers", help='inputDirectory')
parser.add_argument('-g','--gazebodir', default="/home/mikatchou/.gazebo/models/", help='GazeboNodelDirectory')
parser.add_argument('-s','--size', default="500", help='marker size in mm')
parser.add_argument('-v','--verbose', default=False, help='verbose mode')

args = parser.parse_args()
if not os.path.isdir(args.input):
    print "provided input is not a directory"
    sys.exit()



# Open every collada file
if args.verbose:
    print args.input
    
file_list = sorted(os.listdir(args.input))
for file in file_list:
    if file.endswith('.png'):
        cmd = "cp -r " + os.path.join(args.gazebodir, "marker0") + " " + os.path.join(args.gazebodir,file[0:-4].lower())
        if args.verbose:
            print cmd 
        os.system(cmd)
        cmd = "rm " + os.path.join(args.gazebodir,file[0:-4].lower(), "materials", "textures", "*")
        if args.verbose:
            print cmd
        os.system(cmd)
        cmd = "cp " + os.path.join(args.input,file) + " " + os.path.join(args.gazebodir,file[0:-4].lower(), "materials", "textures")
        if args.verbose:
            print cmd 
        os.system(cmd)
        if args.verbose:
            print os.path.join(args.gazebodir,file.lower()[0:-4].lower(), "model.config" )
        dom = parse(os.path.join(args.gazebodir,file[0:-4].lower(), "model.config" ))
        ## modify model.config
        for node in dom.getElementsByTagName('name'):
            node.firstChild.nodeValue = file[0:-4]
            if args.verbose:
                print node.firstChild.nodeValue
            break
        f = open(os.path.join(args.gazebodir,file[0:-4].lower(), "model.config" ),'w+')
        # Write the modified xml file
        f.write(dom.toxml())
        f.close()

        
        ## modify model.sdf
        if args.verbose:
            print "open model.sdf"
            print os.path.join(args.gazebodir, file[0:-4].lower(), "model.sdf" )
        dom = parse(os.path.join(args.gazebodir,file[0:-4].lower(), "model.sdf" ))
        for node in dom.getElementsByTagName('model'):
            node.attributes["name"].value = file[0:-4]
            if args.verbose:
                print "model tag found"
            break


        scaleModified = False
        scale = str(int(args.size)/1000.0)
        for node in dom.getElementsByTagName('mesh'):
            for child in node.childNodes:
                if child.nodeName == "scale":
                    child.firstChild.nodeValue = scale + " " + scale + " " + scale
                    scaleModified = True
                if child.nodeName == "uri":
                    child.firstChild.nodeValue = "model://" + os.path.join( file[0:-4].lower(), "meshes", file[0:-4] + ".dae")
                    if args.verbose:
                        print "uri tag found"
                        print node.firstChild.nodeValue
            if not scaleModified:
                if args.verbose:
                    print "creating scale tag"
                x = dom.createElement("scale")
                y = dom.createTextNode(scale + " " + scale + " " + scale)
                x.appendChild(y)
                node.appendChild(x)

        f = open(os.path.join(args.gazebodir, file[0:-4].lower(), "model.sdf" ),'w+')
        # Write the modified xml file
        f.write(dom.toxml())
        f.close()

        if args.verbose:
            print "cp " + os.path.join(args.gazebodir, file[0:-4].lower(), "model.sdf") + " " + os.path.join(args.gazebodir, file[0:-4].lower(), "model-1_4.sdf")
        os.system("cp " + os.path.join(args.gazebodir, file[0:-4].lower(), "model.sdf") + " " + os.path.join(args.gazebodir, file[0:-4].lower(), "model-1_4.sdf"))

        ## modify model-1_4.sdf
        if args.verbose:
            print "open model-1_4.sdf"
            print os.path.join(args.gazebodir, file[0:-4].lower(), "model-1_4.sdf" )
        dom = parse(os.path.join(args.gazebodir, file[0:-4].lower(), "model-1_4.sdf" ))
        for node in dom.getElementsByTagName('sdf'):
                node.attributes["version"].value = "1.4"
                break;
        f = open(os.path.join(args.gazebodir, file[0:-4].lower(), "model-1_4.sdf" ),'w+')
        # Write the modified xml file
        f.write(dom.toxml())
        f.close()
        if args.verbose:
            print os.path.join(args.gazebodir, file[0:-4].lower(), "meshes","Marker0.dae") + "  newname " + os.path.join(args.gazebodir, file[0:-4].lower(), "meshes", file[0:-4] + ".dae")
        os.rename(os.path.join(args.gazebodir, file[0:-4].lower(), "meshes","Marker0.dae"), os.path.join(args.gazebodir, file[0:-4].lower(), "meshes", file[0:-4] + ".dae"))

        ## modify ModelX.dae
        if args.verbose:
            print "open ModelX.dae"
            print os.path.join(args.gazebodir, file[0:-4].lower(), "meshes", file[0:-4] + ".dae")
        dom = parse(os.path.join(args.gazebodir, file[0:-4].lower(), "meshes", file[0:-4] + ".dae"))
        for node in dom.getElementsByTagName('init_from'):
            node.firstChild.nodeValue= file
            if args.verbose:
                print "init_from tag found"
            break

        f = open(os.path.join(args.gazebodir, file[0:-4].lower(), "meshes", file[0:-4] + ".dae"),'w+')
        # Write the modified xml file
        f.write(dom.toxml())
        f.close()
        
# Find a png file
# copy directory from ~/.gazebo/models/marker0 to ~/.gazebo/models/markerX
# empty ~/.gazebo/models/markerX/materials/textures
# copy MarkerX.png from /media/Data1/mikatchou/Downloads/ARMarkers/MarkerX.png to ~/.gazebo/models/markerX/materials/textures
#
# model.config
# modify name tag in model.config

# model.sdf
# modify model attribute name and put MarkerX
# modify uri tag and put model://markerX/meshes/Marker

# copy model.sdf in model-1_4.sdf
# modify sdf version attribute to "1.4"


