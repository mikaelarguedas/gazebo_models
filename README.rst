gazebo_models
==============

ar_tag models for gazebo

script allowing to generate gazebo models for all the AR tags in the images folder.

How to use
----------

.. code-block:: bash

    $ ./generate_markers_model.py -h
    Usage: generate gazebo models for AR tags

    Optional arguments:
      -h, --help            show this help message and exit
      -i IMAGES_DIR, --images-dir IMAGES_DIR
                            directory where the marker images are located
                            (default: $HOME/gazebo_models/ar_tags/images)
      -g GAZEBODIR, --gazebodir GAZEBODIR
                            Gazebo models directory (default:
                            $HOME/.gazebo/models)
      -s SIZE, --size SIZE  marker size in mm (default: 500)
      -v, --verbose         verbose mode (default: False)

.. code-block:: bash

    ./generate_markers_model.py -i IMAGE_DIRECTORY -g GAZEBO_MODELS_DIRECTORY -s SIZE_IN_MILLIMETER

Limitations
-----------
Assumes png images, dimensions 170*170px

blender file provided to test on other image size

TODO
-----
Support other image formats
