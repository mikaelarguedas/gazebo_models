#! /usr/bin/env python
from __future__ import print_function

import argparse
from xml.dom.minidom import parse
import os
import sys

parser = argparse.ArgumentParser(usage='convert offset of all dae files in a directory')
parser.add_argument(
    '-i', '--input', default="$HOME/gazebo_models/ar_tags/images", help='inputDirectory')
parser.add_argument(
    '-g', '--gazebodir', default="$HOME/.gazebo/models", help='GazeboNodelDirectory')
parser.add_argument('-s', '--size', default="500", help='marker size in mm')
parser.add_argument(
    '-v', '--verbose', dest='verbose', action='store_true', help='verbose mode')
parser.set_defaults(verbose=False)

args = parser.parse_args()

args.gazebodir = os.path.expandvars(args.gazebodir)
args.input = os.path.expandvars(args.input)

if not os.path.isdir(args.input):
    print("provided input is not a directory")
    sys.exit()

# Open every collada file
if args.verbose:
    print(args.input)

# Copy marker0 directory into gazebo model directory
cp_marker0_cmd = "cp -r " + args.input[0:args.input.rfind("images")] + "model/marker0" + \
             " " + os.path.join(args.gazebodir, "marker0")
if args.verbose:
    print(cp_marker0_cmd)
os.system(cp_marker0_cmd)

file_list = sorted(os.listdir(args.input))
for image_file in file_list:
    if not image_file.endswith('.png'):
        continue
    # ignore marker0 as it has alredy been copied above
    if image_file.lower() == 'marker0.png':
        continue

    filename_without_ext = image_file[0:image_file.rfind('.')]
    cmd = "cp -r " + os.path.join(args.gazebodir, "marker0") + \
          " " + os.path.join(args.gazebodir, filename_without_ext.lower())
    if args.verbose:
        print(cmd)
    os.system(cmd)
    cmd = "rm " + os.path.join(
        args.gazebodir, filename_without_ext.lower(), "materials", "textures", "*")
    if args.verbose:
        print(cmd)
    os.system(cmd)
    cmd = "cp " + os.path.join(args.input, image_file) + " " + \
          os.path.join(args.gazebodir, filename_without_ext.lower(),
                       "materials", "textures")
    if args.verbose:
        print(cmd)
    os.system(cmd)
    if args.verbose:
        print(os.path.join(args.gazebodir, filename_without_ext.lower(), "model.config"))
    dom = parse(os.path.join(args.gazebodir, filename_without_ext.lower(), "model.config"))
    # modify model.config
    for node in dom.getElementsByTagName('name'):
        node.firstChild.nodeValue = filename_without_ext
        if args.verbose:
            print(node.firstChild.nodeValue)
        break
    f = open(os.path.join(
        args.gazebodir, filename_without_ext.lower(), "model.config"), 'w+')
    # Write the modified xml file
    f.write(dom.toxml())
    f.close()

    # modify model.sdf
    if args.verbose:
        print("open model.sdf")
        print(os.path.join(args.gazebodir, filename_without_ext.lower(), "model.sdf"))
    dom = parse(os.path.join(args.gazebodir, filename_without_ext.lower(), "model.sdf"))
    for node in dom.getElementsByTagName('model'):
        node.attributes["name"].value = filename_without_ext
        if args.verbose:
            print("model tag found")
        break

    scaleModified = False
    scale = str(int(args.size) / 1000.0)
    for node in dom.getElementsByTagName('mesh'):
        for child in node.childNodes:
            if child.nodeName == "scale":
                child.firstChild.nodeValue = scale + " " + scale + " " + scale
                scaleModified = True
            if child.nodeName == "uri":
                child.firstChild.nodeValue = "model://" + os.path.join(
                    filename_without_ext.lower(), "meshes", filename_without_ext + ".dae")
                if args.verbose:
                    print("uri tag found")
                    print(node.firstChild.nodeValue)
        if not scaleModified:
            if args.verbose:
                print("creating scale tag")
            x = dom.createElement("scale")
            y = dom.createTextNode(scale + " " + scale + " " + scale)
            x.appendChild(y)
            node.appendChild(x)

    f = open(os.path.join(args.gazebodir, filename_without_ext.lower(), "model.sdf"), 'w+')
    # Write the modified xml file
    f.write(dom.toxml())
    f.close()

    cmd = "cp " + os.path.join(args.gazebodir, filename_without_ext.lower(), "model.sdf") + \
          " " + os.path.join(args.gazebodir, filename_without_ext.lower(), "model-1_4.sdf")
    if args.verbose:
        print(cmd)
    os.system(cmd)

    # modify model-1_4.sdf
    if args.verbose:
        print("open model-1_4.sdf")
        print(os.path.join(args.gazebodir, filename_without_ext.lower(), "model-1_4.sdf"))
    dom = parse(os.path.join(args.gazebodir, filename_without_ext.lower(), "model-1_4.sdf"))
    for node in dom.getElementsByTagName('sdf'):
        node.attributes["version"].value = "1.4"
        break
    f = open(os.path.join(args.gazebodir, filename_without_ext.lower(), "model-1_4.sdf"), 'w+')
    # Write the modified xml file
    f.write(dom.toxml())
    f.close()

    cmd = "cp " + os.path.join(args.gazebodir, filename_without_ext.lower(), "model.sdf") + \
          " " + os.path.join(args.gazebodir, filename_without_ext.lower(), "model-1_5.sdf")
    if args.verbose:
        print(cmd)
    os.system(cmd)

    # modify model-1_5.sdf
    if args.verbose:
        print("open model-1_5.sdf")
        print(os.path.join(args.gazebodir, filename_without_ext.lower(), "model-1_5.sdf"))
    dom = parse(os.path.join(args.gazebodir, filename_without_ext.lower(), "model-1_5.sdf"))
    for node in dom.getElementsByTagName('sdf'):
        node.attributes["version"].value = "1.5"
        break
    f = open(os.path.join(args.gazebodir, filename_without_ext.lower(), "model-1_5.sdf"), 'w+')
    # Write the modified xml file
    f.write(dom.toxml())
    f.close()

    meshes_dir = os.path.join(args.gazebodir, filename_without_ext.lower(), "meshes")
    if args.verbose:
        print(os.path.join(meshes_dir, "Marker0.dae") +
              "  newname " + os.path.join(
                  meshes_dir, filename_without_ext + ".dae"))
    os.rename(
        os.path.join(meshes_dir, "Marker0.dae"),
        os.path.join(meshes_dir, filename_without_ext + ".dae"))

    # modify ModelX.dae
    if args.verbose:
        print("open ModelX.dae")
        print(os.path.join(meshes_dir, filename_without_ext + ".dae"))
    dom = parse(os.path.join(meshes_dir, filename_without_ext + ".dae"))
    for node in dom.getElementsByTagName('init_from'):
        node.firstChild.nodeValue = image_file
        if args.verbose:
            print("init_from tag found")
        break

    f = open(os.path.join(
        meshes_dir, filename_without_ext + ".dae"), 'w+')
    # Write the modified xml file
    f.write(dom.toxml())
    f.close()
