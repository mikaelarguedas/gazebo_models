gazebo_models
==============

ar_tag models for gazebo

script allowing to generate gazebo models for all the AR tags in the images folder.

How to use
----------

.. code-block:: bash

    $ ./generate_markers_model.py -h
    usage: generate gazebo models for AR tags

    optional arguments:
      -h, --help            show this help message and exit
      -i IMAGES_DIR, --images-dir IMAGES_DIR
                            directory where the marker images are located
                            (default: $HOME/gazebo_models/ar_tags/images)
      -g GAZEBODIR, --gazebodir GAZEBODIR
                            Gazebo models directory (default:
                            $HOME/.gazebo/models)
      -s SIZE, --size SIZE  marker size in mm (default: 500)
      -v, --verbose         verbose mode (default: False)
      -w WHITE_CONTOUR_SIZE_MM, --white-contour-size-mm WHITE_CONTOUR_SIZE_MM
                            Add white contour around images, default to no contour
                            (default: 0)

.. code-block:: bash

    ./generate_markers_model.py -i IMAGE_DIRECTORY -g GAZEBO_MODELS_DIRECTORY -s SIZE_IN_MILLIMETER -w CONTOUR_SIZE_IN_MM

For example the following command will generate markers of 1m side + 0.5m white contour on each side, resulting in a 2mx2m gazebo model.

.. code-block:: bash

    ./generate_markers_model.py -i IMAGE_DIRECTORY -s 1000 -w 500

Limitations
-----------
Assumes png images, dimensions 170*170px

blender file provided to test on other image size

TODO
-----
Support other image formats
