Working Directories
=================================

Typical working directory layout for a FRED simulation::

./fred.inp
./inp/
./plugin/
./out/

*fred.inp* file
    An input file is always needed. The default name is *fred.inp*.

*inp* folder
    An optional directory *inp* can contain auxiliary files (e.g. DICOM files, user-defined HU calibration curves, treatment plan files, etc.).

*out* folder
    The *out* directory is populated by output files and results produced by FRED.

*plugin* folder
    A *plugin* directory can contain user-written code in the form of a dynamically loaded plugin that expands the capability of FRED code.


All these locations can be redefined using command line options, e.g.

.. code-block:: bash

    fred -f myInputFile 
    fred -i myInputDirectory
    fred -o myOutputDirectory
    fred -plugindir myPluginDirectory

.. Caution:: The output directory is completely erased each time a simulation is run. 

