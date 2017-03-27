gazebo_models
==============

ar_tag models for gazebo

script allowing to generate gazebo models for all the AR tags in the images folder.

Parameters
-----------
-i or --input: directory where the marker images are stored (absolute path)

-g or --gazebodir: directory of the gazebo models (usually in ~/.gazebo/models) (absolute path)

-s or --size: size of the marker in millimeter

How to use
----------
copy the marker0 folder in you gazebo model directory

.. code-block:: bash

    ./generate_markers_model.py -i IMAGE_DIRECTORY -g GAZEBO_MODELS_DIRECTORY -s SIZE_IN_MILLIMETER

Limitations
-----------
Tested only on png images, dimensions 170*170px

blender file provided to test on other image size

TODO
-----
Test on other image formats

Generate sdf 1.5 files also
    
